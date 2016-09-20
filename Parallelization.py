# -*- coding: utf-8 -*-
'''
Created on 2014/4/18
@author: Ivy Liu
'''

import threading
import time
from robot.libraries.BuiltIn import BuiltIn
from robot.errors import ExecutionFailed, ExecutionPassed, ExecutionFailures

_errors = []
_condition = threading.Condition()

class Parallelization:
    
    global _errors    
    _threads = []

    def run_async(self, keyword, *arg):
        """
                        產生一個新的 Thread，
                        使其執行給定的 keyword，                
                        並回傳此Thread。
                        
                        若在測試案例中需要等待此 keyword執行結束時，
                        可以使用 Wait Until及回傳的Thread進行等待的動作。
        
        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | Wait Until | ${thread1} | ${thread2} |
                        
                        若在Thread中需要數個keyword循序執行
                        則加上Run Keywords，並在keyword之間以'AND'做連接
                        
        Examples:
        | ${thread1} | Run Async | Run Keywords | My Keyword 1 | arg1 | AND | My Keyword 2 |
        | ${thread2} | Run Async | My Keyword 3 | arg3 |
        | Wait Until | ${thread1} | ${thread2} |
        """
        thread = ExecuteKeywordThread(keyword, *arg)
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
        self._threads.append(thread)
            
        return thread

    def wait_until(self, *threads):
        """
                        指定一個或多個Thread，
                        等待指定的Thread皆結束工作後，
                        才繼續做接下來的動作。

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | Wait Until | ${thread1} |

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Wait Until | ${thread1} | ${thread2} | ${thread3} |
        """
        for thread in threads :
            thread.join()
            time.sleep(1)

        if _errors:
            raise ExecutionFailures(_errors)
        
        _errors[:] = []
        self._threads[:] = []
    
    def stop_async_tasks(self, *threads):
        """
                        指定一個或多個Thread，
                        強制停止指定Thread執行中的工作。

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Stop Async Tasks | ${thread1} | ${thread2} | ${thread3} |
        """
        for thread in threads :
            thread.stop()
            time.sleep(1)
            
    def stop_all_async_tasks(self):
        """
                        強制停止所有正在執行中的Thread。

        Examples:
        | ${thread1} | Run Async | My Keyword 1 | arg1 |
        | ${thread2} | Run Async | My Keyword 2 | arg2 |
        | ${thread3} | Run Async | My Keyword 3 | arg3 |
        | Stop All Async Tasks |
        """
        for thread in self._threads :
            thread.stop()
            time.sleep(1)
            
    def is_alive(self, thread):
        """
                        指定一個Thread，檢查此Thread是否仍在執行，
                        仍在執行回傳True，反之則回傳False。

        Examples:
        | ${thread1} | Run Async | My Keyword 1 |
        | ${is_alive} | Is Alive | ${thread1} |
        """
        return thread.is_alive()

class ExecuteKeywordThread(threading.Thread):

    global _errors, _condition
    
    @property
    def _builtin_lib(self):
        return self._builtin.get_library_instance('BuiltIn')
    
    def __init__(self, keyword, *arg):
        threading.Thread.__init__(self)
        self.keyword = keyword
        self.arg = arg
        self._builtin = BuiltIn()
        self._stop = threading.Event()
        
    def run(self):
        try:
            self._builtin_lib.run_keyword(self.keyword, *self.arg)

        except ExecutionPassed, err:
            err.set_earlier_failures(_errors)
            raise err
        except ExecutionFailed, err:
            if _condition.acquire():
                _errors.extend(err.get_errors())
                _condition.notify()
                _condition.release()
            else :
                _condition.wait()
                _errors.extend(err.get_errors())
                _condition.notify()
        
    def stop(self):
        self._stop.set()
        self._Thread__stop()