Android Keyword Library
=============

# RF uiautomator #

## Get Info ##

Possible result：

	{
	 u'displayRotation': 0,
	 u'displaySizeDpY': 640,
	 u'displaySizeDpX': 360,
	 u'currentPackageName': u'com.android.launcher',
	 u'productName': u'vbox86p',
	 u'displayWidth': 1080,
	 u'sdkInt': 19,
	 u'displayHeight': 1776,
	 u'naturalOrientation': True
	}

## Get Object ##

Selector supports below parameters：

- `text`, `textContains`, `textMatches`, `textStartsWith`
- `className`, `classNameMatches`
- `description`, `descriptionContains`, `descriptionMatches`, `descriptionStartsWith`
- `checkable`, `checked`, `clickable`, `longClickable`
- `scrollable`, `enabled`,`focusable`, `focused`, `selected`
- `packageName`, `packageNameMatches`
- `resourceId`, `resourceIdMatches`
- `index`, `instance`

ex：

<table>
<tbody>
<tr>
<td>Get Object</td>
<td>text=Setting</td>
<td>index=1</td>
</tr>
</tbody>
</table>

## Get Info Of Object ##

Possible result：

	{
	 u'contentDescription': u'',
	 u'checked': False,
	 u'scrollable': True,
	 u'text': u'',
	 u'packageName': u'com.android.launcher',
	 u'selected': False,
	 u'enabled': True,
	 u'bounds':
	           {
	            u'top': 231,
	            u'left': 0,
	            u'right': 1080,
	            u'bottom': 1776
	           },
	 u'className': u'android.view.View',
	 u'focusable': False,
	 u'focused': False,
	 u'clickable': False,
	 u'checkable': False,
	 u'chileCount': 1,
	 u'longClickable': False,
	 u'visibleBounds':
	                  {
	                   u'top': 231,
	                   u'left': 0,
	                   u'right': 1080,
	                   u'bottom': 1776
	                  }
	}

# Acknowledgement

This library was supported partially by the Ministry of Science and Technology, Taiwan, under contract number MOST 104-2221-E-027-007 -
