# RegexPy

Yet another playground for testing <ins>Python</ins> flavoured regular expressions.

![Screenshot](./screenshots/regexpy.gif)

Hover over matches/groups to identify their indexes.

Ctrl + T/Search button tests the regular expression on sample text. 

Alt+Right:&emsp;Next Match<br/>
Alt+Left:&emsp;&ensp;&nbsp;Previous Match<br/>
Ctrl+Alt+Right:&emsp;Next Group<br/>
Ctrl+Alt+Left:&emsp;&ensp;&nbsp;Previous Group<br/>

Escape or mouse click exit navigation mode.

Tab/Shift+Tab move focus - to enter a tab character use Ctrl+Tab.

Edit the sample [config](./regexpy.conf) file to suit, e.g. highlighting colours.

Last saved regex, last loaded/saved sample and flags are reloaded on restart.

TODO custom undo stack to preserve undos/redos before navigation. 

## Dependencies

Python >= 3.7, PySide6, Qt >= 6.4