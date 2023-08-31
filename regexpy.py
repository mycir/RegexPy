import configparser
import os
import re
from dataclasses import dataclass
from time import strftime
from traceback import print_exc

from PySide6.QtCore import (
    QByteArray,
    QEvent,
    QFile,
    QPoint,
    QPointF,
    Qt,
    QTextStream,
)
from PySide6.QtGui import QColor, QKeyEvent, QTextCharFormat, QTextCursor
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QMenu,
    QToolButton,
    QWidget,
)
from regexpy_ui import Ui_Form


@dataclass
class Colours:
    def __init__(
        self,
        regex_valid=QColor(Qt.darkGreen),
        regex_invalid=QColor(Qt.red),
        match_foreground=QColor(Qt.black),
        match_background=QColor(Qt.yellow),
        group_foreground=QColor(Qt.white),
        group_background=QColor(Qt.red),
    ):
        colours = {
            "regex_valid": regex_valid,
            "regex_invalid": regex_invalid,
            "match_foreground": match_foreground,
            "match_background": match_background,
            "group_foreground": group_foreground,
            "group_background": group_background,
        }

        self.colours = colours
        self.defaults = self.__init__.__defaults__
        for i, c in enumerate(colours):
            self.assign_colour(c, colours[c], i)

    def assign_colour(self, name, colour, index):
        if type(colour) is QColor:
            c = colour
        elif type(colour) is str:
            c = QColor.fromString(colour)
            if not QColor.isValid(c):
                c = self.defaults[index]
        setattr(self, name, c)


class SvgButton(QToolButton):
    def __init__(self, svg, parent=None):
        super().__init__(parent)
        svg_widget = QSvgWidget()
        svg_widget.load(QByteArray(svg))
        svg_widget.setFixedSize(18, 18)
        self.setFixedSize(20, 20)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(svg_widget, 0, Qt.AlignHCenter | Qt.AlignVCenter)

    def set_menu(self, menu):
        self.setMenu(menu)
        self.clicked.connect(self.show_menu)

    def show_menu(self):
        pos = self.mapToGlobal(QPointF(0, 0)).toPoint()
        s = self.menu().sizeHint().toTuple()
        p = QPoint(s[0] - self.width(), s[1] + 5)
        pos -= p
        self.menu().popup(pos)


class Expression:
    @dataclass
    class PatternGroup:
        level: int
        start: int
        end: int
        capturing: bool
        name: str

        def __init__(
            self, level=None, start=None, end=None, capturing=False, name=None
        ):
            self.level = level
            self.start = start
            self.end = end
            self.capturing = capturing
            self.name = name

    def __init__(self, pattern):
        self.pattern = pattern
        self.groups = self.find_groups(pattern.pattern)
        self.capturing = [g for g in self.groups if g.capturing]

    def find_groups(self, pattern):
        groups = []
        level_indexes = []
        index, level = (0, 0)
        for i, c in enumerate(pattern):
            if c == "(":
                if (pattern[i + 1]) != "?":
                    cap = True
                    name = None
                elif pattern[i + 2] == "P":
                    m = re.search(r"<(.*)>", pattern[i + 3 :])  # noqa: E203
                    if m:
                        cap = True
                        name = m[1]
                    else:
                        cap = False
                        name = None
                else:
                    cap = False
                    name = None
                groups.append(
                    self.PatternGroup(level, i, capturing=cap, name=name)
                )
                level_indexes.append(index)
                index += 1
                level += 1
            elif c == ")":
                groups[level_indexes.pop()].end = i
                level -= 1
        return groups


class RegexPy(QWidget):
    colours = Colours()
    option_flags = {
        "checkBoxAscii": re.ASCII,
        "checkBoxIgnoreCase": re.IGNORECASE,
        "checkBoxMultiline": re.MULTILINE,
        "checkBoxDotAll": re.DOTALL,
        "checkBoxVerbose": re.VERBOSE,
    }
    sample_selection = False

    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.splitter.setSizes([40, 30, 490])
        self.ui.splitter.setCollapsible(0, False)
        self.ui.splitter.setCollapsible(1, False)
        self.ui.splitter.setCollapsible(2, False)
        self.ui.labelMatch.hide()
        self.ui.labelGroups.hide()
        self.ui.labelGroupsIndex.hide()
        self.add_buttons()
        self.ui.checkBoxAscii.clicked.connect(self.clear_formatting)
        self.ui.checkBoxIgnoreCase.clicked.connect(self.clear_formatting)
        self.ui.checkBoxMultiline.clicked.connect(self.clear_formatting)
        self.ui.checkBoxDotAll.clicked.connect(self.clear_formatting)
        self.ui.checkBoxVerbose.clicked.connect(self.clear_formatting)
        self.ui.plainTextEditRegex.document().contentsChange.connect(
            self.validate
        )
        self.ui.plainTextEditSample.document().contentsChange.connect(
            self.on_sample_changed
        )
        self.ui.plainTextEditSample.copyAvailable.connect(
            lambda s: setattr(self, "sample_selection", s)
        )
        self.ui.plainTextEditRegex.installEventFilter(self)
        self.ui.plainTextEditSample.installEventFilter(self)
        self.load_config()
        if self.ui.plainTextEditRegex.toPlainText() > "":
            self.validate()

    def get_icon_colour(self):
        button = QToolButton()
        button.setFixedSize(24, 24)
        img = button.grab().toImage()
        button.deleteLater()
        cx = button.width() / 2
        cy = button.height() / 2
        colour = img.pixelColor(cx, cy)
        colour_black = colour.blackF()
        if colour_black < 0.666:
            return colour.darker(250).name()
        else:
            return colour.lighter(250).name()

    def add_buttons(self):
        buttons_layout = QHBoxLayout(self.ui.frameButtons)
        buttons_layout.setSpacing(12)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        icon_colour = self.get_icon_colour()
        svg_flag = f"""
            <svg width="128" height="128"
            viewBox="0 0 128 128"><path style="fill:{icon_colour};"
            d="M 67.390 21.159 C 55.455 27.423, 51.205 27.919,
            45.667 23.695 C 43.644 22.152, 41.541 21.166,
            40.994 21.504 C 40.401 21.870, 40 28.667, 40 38.337 C 40 56.074,
            40.417 57.613, 46.011 60.506 C 51.383 63.284, 56.516 62.432,
            66.410 57.119 C 71.410 54.434, 76.916 51.934,
            78.646 51.562 C 82.138 50.812, 87.655 52.672,
            89.872 55.345 C 90.627 56.255, 91.865 57, 92.622 57 C 93.740 57,
            94 53.724, 94 39.674 C 94 22.981, 93.918 22.274,
            91.750 20.299 C 85.147 14.285, 80.154 14.461,
            67.390 21.159 M 34.701 20.632 C 34.316 21.018,
            34 41.765, 34 66.736 L 34 112.139 36.250 111.820
            L 38.500 111.500 38.500 66.014 C 38.500 25.740, 38.323 20.493,
            36.951 20.229 C 36.099 20.065, 35.087 20.246, 34.701 20.632"/></svg>
        """
        svg_search = f"""
            <svg width="128" height="128" viewBox="0 0 128 128" fill="none">
            <circle cx="58" cy="48" r="28"
            stroke="{icon_colour}" stroke-width="10"/>
            <path d="M110 100L80 70" stroke="{icon_colour}" stroke-width="10"
            stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        """
        svg_hamburger = f"""
            <svg viewBox="0 0 128 128"
            width="128" height="128" fill="{icon_colour}">
            <rect x="14" y="27" rx="5" ry="5" width="100" height="10"></rect>
            <rect x="14" y="57" rx="5" ry="5" width="100" height="10"></rect>
            <rect x="14" y="87" rx="5" ry="5" width="100" height="10"></rect>
            </svg>
        """
        flag_btn = SvgButton(svg_flag)
        flag_btn.setToolTip("Show/hide options flags")
        flag_btn.setCheckable(True)
        flag_btn.setChecked(True)
        flag_btn.clicked.connect(
            lambda: self.ui.frameOptions.setVisible(
                not self.ui.frameOptions.isVisible()
            )
        )
        buttons_layout.addWidget(flag_btn, 0, Qt.AlignRight | Qt.AlignVCenter)
        search_btn = SvgButton(svg_search)
        search_btn.setToolTip("Search sample text for RE matches")
        search_btn.setShortcut("Ctrl+T")
        search_btn.clicked.connect(self.test_pattern)
        buttons_layout.addWidget(search_btn, 0, Qt.AlignRight | Qt.AlignVCenter)
        hamburger_btn = SvgButton(svg_hamburger)
        hamburger_btn.setToolTip("Menu: Load sample, load RE")
        hamburger_btn.setStyleSheet(
            "QToolButton::menu-indicator { image: none; }"
        )
        self.menu = QMenu(hamburger_btn)
        self.menu.addAction("Load RE", self.load_file, "Ctrl+O")
        self.menu.addAction("Load sample", self.load_file, "Ctrl+Shift+O")
        self.menu.addSeparator()
        self.menu.addAction("Save RE", self.save_regex, "Ctrl+S")
        self.menu.addAction("Save sample", self.save_sample, "Ctrl+Shift+S")
        hamburger_btn.set_menu(self.menu)
        buttons_layout.addWidget(
            hamburger_btn, 0, Qt.AlignRight | Qt.AlignVCenter
        )

    def set_skeleton_config(self, configparser):
        if not configparser.has_section("Flags"):
            configparser.add_section("Flags")
        if not configparser.has_section("RegexFile"):
            configparser.add_section("RegexFile")
        if not configparser.has_section("SampleFile"):
            configparser.add_section("SampleFile")

    def load_config(self):
        cp = configparser.ConfigParser(interpolation=None)
        cp.optionxform = str
        self.set_skeleton_config(cp)
        self.configparser = cp
        dir = os.path.realpath(os.path.dirname(__file__))
        try:
            cp.read_file(open(f"{dir}/regexpy.conf"))
            if cp.has_section("Colours"):
                colours = cp.items("Colours")
                for k, v in colours:
                    self.colours.assign_colour(
                        k,
                        v,
                        list(self.colours.colours).index(k),
                    )
            if cp.has_section("Flags"):
                checks = {}
                for c in self.ui.frameOptions.findChildren(QCheckBox):
                    checks[c.objectName().removeprefix("checkBox").lower()] = c
                flags = cp.options("Flags")
                for o in flags:
                    if o in checks:
                        checks[o].setChecked(cp.getboolean("Flags", o))
            if cp.has_option("RegexFile", "filename"):
                fn = cp.get("RegexFile", "filename")
                if fn:
                    try:
                        self.load_file(fn, self.ui.plainTextEditRegex)
                        self.validate()
                    except Exception:
                        print_exc
            if cp.has_option("SampleFile", "filename"):
                fn = cp.get("SampleFile", "filename")
                if fn:
                    try:
                        self.load_file(fn, self.ui.plainTextEditSample)
                    except Exception:
                        print_exc()
        except Exception:
            print_exc()

    def load_file(self, filename=None, widget=None):
        if not filename:
            if self.sender().text() == "Load sample":
                widget = self.ui.plainTextEditSample
                type = "sample"
            elif self.sender().text() == "Load RE":
                widget = self.ui.plainTextEditRegex
                type = "regex"
            fd = QFileDialog(caption=f"RegexPy - choose {type} file")
            fd.setMimeTypeFilters(["text/plain", "application/octet-stream"])
            fd.setFileMode(QFileDialog.FileMode.ExistingFile)
            fd.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
            if not fd.exec():
                return
            else:
                filename = fd.selectedFiles()[0]
                if type == "sample":
                    self.configparser.set('SampleFile', 'filename', filename)
                elif type == "regex":
                    self.configparser.set('RegexFile', 'filename', filename)
        f = QFile(filename)
        if f.open(QFile.OpenModeFlag.ReadOnly):
            # 'QTextStream is locale aware, and will automatically
            # decode standard input using the correct encoding'
            ts = QTextStream(f)
            txt = ts.readAll()
            f.close()
            widget.setPlainText(txt)
            self.set_position(widget)
            widget.setFocus()
            if widget is self.ui.plainTextEditRegex:
                self.validate()

    def save_regex(self):
        name = strftime("regex_%Y%m%d_%H%M%S.txt")
        fn = QFileDialog.getSaveFileName(
            self, "RegexPy - save regular expression", name
        )[0]
        if fn > "":
            with open(fn, mode="w") as f:
                f.write(self.ui.plainTextEditRegex.toPlainText())
            self.configparser.set('RegexFile', 'filename', fn)

    def save_sample(self):
        name = strftime("sample_%Y%m%d_%H%M%S.txt")
        fn = QFileDialog.getSaveFileName(
            self, "RegexPy - save sample", name
        )[0]
        if fn > "":
            with open(fn, mode="w") as f:
                f.write(self.ui.plainTextEditSample.toPlainText())
            self.configparser.set('SampleFile', 'filename', fn)

    def closeEvent(self, event):
        dir = os.path.realpath(os.path.dirname(__file__))
        self.save_flags()
        self.configparser.write(open(f"{dir}/regexpy.conf", mode="w"))

    def validate(self):
        p = self.ui.plainTextEditRegex.toPlainText()
        if p != "":
            try:
                self.pattern = re.compile(p)
                is_valid = True
            except re.error:
                is_valid = False
        else:
            is_valid = False
        if is_valid:
            self.colour_text(
                self.ui.plainTextEditRegex, self.colours.regex_valid
            )
            self.expression = Expression(self.pattern)
            self.clear_formatting()
            self.ui.labelMatchesCount.setText("0")
            self.menu.actions()[3].setEnabled(True)
        else:
            self.colour_text(
                self.ui.plainTextEditRegex, self.colours.regex_invalid
            )
            self.menu.actions()[3].setEnabled(False)

    def get_flags(self):
        flags = 0
        for i, cb in enumerate(self.ui.frameOptions.findChildren(QCheckBox)):
            if cb.isChecked():
                name = cb.objectName()
                f = self.option_flags[name]
                flags |= f
        return flags

    def save_flags(self):
        for i, cb in enumerate(self.ui.frameOptions.findChildren(QCheckBox)):
            on = cb.objectName()
            opt = self.option_flags[on].name.lower()
            if not self.configparser.has_section("Flags"):
                self.configparser.add_section("Flags")
            self.configparser.set('Flags', opt, str(int(cb.isChecked())))

    def set_position(self, edit, pos=0):
        edit = self.ui.plainTextEditSample
        cursor = edit.textCursor()
        cursor.setPosition(pos, QTextCursor.MoveMode.MoveAnchor)
        edit.setTextCursor(cursor)

    def clear_formatting(self, save_cursor=True):
        cursor = self.ui.plainTextEditSample.textCursor()
        pos = cursor.position()
        cursor.select(QTextCursor.Document)
        cf = QTextCharFormat()
        cursor.setCharFormat(cf)
        cursor.clearSelection()
        if save_cursor:
            cursor.setPosition(pos, QTextCursor.MoveMode.MoveAnchor)
        self.ui.plainTextEditSample.setTextCursor(cursor)
        self.ui.labelMatchesCount.setText("0")
        self.ui.labelMatch.hide()
        self.ui.labelGroups.hide()
        self.ui.labelGroupsIndex.hide()

    def clear_regex_selection(self):
        tc = self.ui.plainTextEditRegex.textCursor()
        tc.clearSelection()
        self.ui.plainTextEditRegex.setTextCursor(tc)

    def colour_text(self, edit, foreground, background=None, span=None):
        cursor = edit.textCursor()
        cf = QTextCharFormat()
        cf.setForeground(foreground)
        if span:
            cursor.setPosition(span[0], QTextCursor.MoveMode.MoveAnchor)
            bgc = cursor.charFormat().background().color()
            if background:
                if bgc == background:
                    background = background.darker(150)
                cf.setBackground(background)
            cursor.setPosition(span[1], QTextCursor.MoveMode.KeepAnchor)
        else:
            cursor.select(QTextCursor.Document)
            cursor.setCharFormat(cf)
            cursor.clearSelection()
        cursor.setCharFormat(cf)

    def colour_matches(self, matches):
        for m in matches:
            self.colour_text(
                self.ui.plainTextEditSample,
                self.colours.match_foreground,
                self.colours.match_background,
                m[0],
            )
            gbc = self.colours.group_background
            for g in m[1]:
                if g[0][1] - g[0][0] > 0:
                    self.colour_text(
                        self.ui.plainTextEditSample,
                        self.colours.group_foreground,
                        gbc,
                        g[0],
                    )

    def find_match(self, p):
        gi = -1
        for mi, m in enumerate(self.matches):
            len_groups = len(m[1])
            if len_groups:
                for i in range(len_groups - 1, -1, -1):
                    g = m[1][i]
                    start = g[0][0]
                    end = g[0][1]
                    if start == end:
                        continue
                    elif p > start and p <= end:
                        gi = i
                        return (mi, gi)
            if p >= m[0][0] and p <= m[0][1]:
                return (mi, gi)
        return (-1, -1)

    def select_group(self, g):
        cursor = self.ui.plainTextEditRegex.textCursor()
        cursor.setPosition(g.start, QTextCursor.MoveMode.MoveAnchor)
        cursor.setPosition(g.end + 1, QTextCursor.MoveMode.KeepAnchor)
        self.ui.plainTextEditRegex.setTextCursor(cursor)

    def eventFilter(self, widget, event):
        if event.type() is QKeyEvent.KeyPress:
            if widget in (
                self.ui.plainTextEditRegex,
                self.ui.plainTextEditSample,
            ):
                if (
                    event.key() == Qt.Key_Tab
                    and event.modifiers() == Qt.KeyboardModifier.ControlModifier
                ):
                    widget.insertPlainText("\t")
                    return True
        elif widget is self.ui.plainTextEditSample:
            if event.type() is QEvent.ToolTip:
                cfp = self.ui.plainTextEditSample.cursorForPosition(event.pos())
                bgc = cfp.charFormat().background().color()
                if cfp.atEnd() or bgc.black() == 255:
                    self.ui.labelMatch.hide()
                    self.ui.labelGroups.hide()
                    self.ui.labelGroupsIndex.hide()
                    self.clear_regex_selection()
                else:
                    mi, gi = self.find_match(cfp.position())
                    if mi >= 0:
                        self.ui.labelMatch.setText(f"[{mi + 1}]")
                        self.ui.labelMatch.show()
                        if gi >= 0:
                            self.ui.labelGroups.show()
                            self.ui.labelGroupsIndex.show()
                            cap = self.expression.capturing[gi]
                            self.select_group(cap)
                            self.ui.labelGroupsIndex.setText(
                                cap.name if cap.name else str(gi + 1)
                            )
                        else:
                            self.ui.labelGroups.hide()
                            self.ui.labelGroupsIndex.hide()
                            self.clear_regex_selection()
        return False

    def jiggle_position(self, widget, pos, direction):
        # called several times, scrolls pos into view
        cursor = widget.textCursor()
        cursor.setPosition(pos)
        cursor.movePosition(direction, QTextCursor.MoveAnchor, 15)
        widget.setTextCursor(cursor)
        widget.ensureCursorVisible()

    def test_pattern(self):
        self.clear_formatting()
        self.ui.labelMatchesCount.setText("0")
        self.pattern = re.compile(
            self.ui.plainTextEditRegex.toPlainText(),
            self.get_flags(),
        )
        res = self.pattern.finditer(self.ui.plainTextEditSample.toPlainText())
        matches = []
        for m in res:
            groups = []
            span = m.span()
            g_len = len(m.groups())
            for i in range(1, g_len + 1):
                groups.append([m.span(i), i])
            matches.append([span, groups])
        self.colour_matches(matches)
        pos = matches[0][0][0]
        self.jiggle_position(self.ui.plainTextEditSample, pos, QTextCursor.Up)
        self.jiggle_position(self.ui.plainTextEditSample, pos, QTextCursor.Down)
        self.ui.labelMatchesCount.setText(str(len(matches)))
        self.matches = matches

    def on_sample_changed(self, _, removed, added):
        if added != removed or self.sample_selection:
            self.clear_formatting()
        self.sample_selection = False
        if self.ui.plainTextEditSample.toPlainText() > "":
            self.menu.actions()[4].setEnabled(True)
        else:
            self.menu.actions()[4].setEnabled(False)


if __name__ == "__main__":
    app = QApplication()
    regexpy = RegexPy()
    regexpy.show()
    app.exec()
