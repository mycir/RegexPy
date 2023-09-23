# RegexPy

Yet another playground for testing <ins>Python</ins> flavoured regular expressions.<br />
[Releases](https://github.com/mycir/RegexPy/releases) are available for Linux, Windows and MacOS.

![Screenshot](./screenshots/regexpy.gif)

### Shortcuts and behaviour

| Linux & Windows | MacOS | Button | Action |
| --- | --- | --- | --- |
| Ctrl+O | Command+O | | Load sample text |
| Ctrl+S | Command+S | | Save sample text |
| Ctrl+Shift+O | Command+Shift+O | | Load regex |
| Ctrl+Shift+S | Command+Shift+S | | Save regex |
| Alt+F | Option+F | Flag | Hide/Show regex flag options |
| Alt+T | Option+T | Search | Test the regular expression on sample text |
| Ctrl+M | Command+M | Marker | Toggle scrollbar match position markers |
| Alt+M | Option+M | Menu | Activate load/save menu |
| Ctrl+Right | Option+Right | | Next Match |
| Ctrl+Left | Option+Left | | Previous Match |
| Right | Right | | Next Group |
| Left | Left | | Previous Group |
| Alt+A | Option+A | | Return to anchor<br />(after hovering over another match/group) |
| Escape/mouse click | Escape/mouse click |  | Exit navigation mode |
| Tab/Shift+Tab | Tab/Shift+Tab | | Move focus |
| Ctrl+Tab | Option+Tab | | Type a tab character in regex or sample |

Hover over matches/groups to identify their indexes.

Last saved regex, last loaded/saved sample and flags are reloaded on restart.

Edit the sample [config](./regexpy.conf) file to suit, e.g. highlighting colours.

### Highlighting

![Screenshot](./screenshots/highlighting.png)

(Colours can be changed in regexpy.conf but adjacent matches or groups<br/>are automatically rendered darker or lighter to suit theme.)

## Dependencies

Python >= 3.7, PySide6, Qt >= 6.4

(Only required when run as a Python script, see release notes below.)

## Releases

These are standalone 'executables' that include all necessary libraries. Furthermore, they do not require Python to be installed.

Note: They are [pyinstaller](https://github.com/pyinstaller/pyinstaller) generated self extracting archives. By default they launch from a terminal window,<br />to suppress this use the --noconsole option.
