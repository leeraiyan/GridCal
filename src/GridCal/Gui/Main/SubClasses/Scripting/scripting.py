# GridCal
# Copyright (C) 2015 - 2023 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import datetime as dtelib
from PySide6.QtGui import QFont, QFontMetrics
from GridCal.Gui.Main.SubClasses.io import IoMain
from GridCal.Gui.Main.SubClasses.Scripting.python_highlighter import PythonHighlighter

from GridCal.Gui.GuiFunctions import CustomFileSystemModel
from GridCal.Gui.messages import error_msg, yes_no_question


class ScriptingMain(IoMain):
    """
    Diagrams Main
    """

    def __init__(self, parent=None):
        """

        @param parent:
        """

        # create main window
        IoMain.__init__(self, parent)



        # Source code text ---------------------------------------------------------------------------------------------
        # Set the font for your widget
        font = QFont("Consolas", 10)  # Replace "Consolas" with your preferred monospaced font
        self.ui.sourceCodeTextEdit.setFont(font)

        # Set tab width to 4 spaces
        font_metrics = QFontMetrics(font)
        tab_stop_width = font_metrics.horizontalAdvance(' ' * 4)  # Width of 4 spaces in the selected font
        self.ui.sourceCodeTextEdit.setTabStopDistance(tab_stop_width)

        self.ui.sourceCodeTextEdit.highlighter = PythonHighlighter(self.ui.sourceCodeTextEdit.document())

        # tree view
        root_path = self.scripts_path()
        self.python_fs_model = CustomFileSystemModel(root_path=self.scripts_path(), ext_filter=['*.py'])
        self.ui.sourceCodeTreeView.setModel(self.python_fs_model)
        self.ui.sourceCodeTreeView.setRootIndex(self.python_fs_model.index(root_path))

        # actions ------------------------------------------------------------------------------------------------------
        self.ui.actionReset_console.triggered.connect(self.create_console)

        # buttonclicks -------------------------------------------------------------------------------------------------
        self.ui.runSourceCodeButton.clicked.connect(self.run_source_code)
        self.ui.saveSourceCodeButton.clicked.connect(self.save_source_code)
        self.ui.deleteSourceCodeFileButton.clicked.connect(self.delete_source_code)

        # double clicked -----------------------------------------------------------------------------------------------
        self.ui.sourceCodeTreeView.doubleClicked.connect(self.source_code_tree_clicked)

    def console_msg(self, *msg_):
        """
        Print some message in the console.

        Arguments:

            **msg_** (str): Message

        """
        dte = dtelib.datetime.now().strftime("%b %d %Y %H:%M:%S")

        txt = self.ui.outputTextEdit.toPlainText()

        for e in msg_:
            if isinstance(e, list):
                txt += '\n' + dte + '->\n'
                for elm in e:
                    txt += str(elm) + "\n"
            else:
                txt += '\n' + dte + '->'
                txt += " " + str(e)

        self.ui.outputTextEdit.setPlainText(txt)

    def run_source_code(self):
        """
        Run the source code in the IPython console
        """
        code = self.ui.sourceCodeTextEdit.toPlainText()

        if code[-1] != '\n':
            code += "\n"

        self.console.execute_command(code)

    def source_code_tree_clicked(self, index):
        """
        On double click on a source code tree item, load the source code
        """
        pth = self.python_fs_model.filePath(index)

        if os.path.exists(pth):
            with open(pth, 'r') as f:
                txt = "\n".join(line.rstrip() for line in f)
                self.ui.sourceCodeTextEdit.setPlainText(txt)

            name = os.path.basename(pth)
            self.ui.sourceCodeNameLineEdit.setText(name.replace('.py', ''))
        else:
            error_msg(pth + ' does not exists :/', 'Open script')

    def save_source_code(self):
        """
        Save the source code
        """
        name = self.ui.sourceCodeNameLineEdit.text().strip()

        if name != '':
            fname = name + '.py'
            pth = os.path.join(self.scripts_path(), fname)
            with open(pth, 'w') as f:
                f.write(self.ui.sourceCodeTextEdit.toPlainText())
        else:
            error_msg("Please enter a name for the script", title="Save script")

    def delete_source_code(self):
        """
        Delete the selected file
        """
        index = self.ui.sourceCodeTreeView.currentIndex()
        pth = self.python_fs_model.filePath(index)
        if os.path.exists(pth):
            ok = yes_no_question(text="Do you want to delete {}?".format(pth), title="Delete source code file")

            if ok:
                os.remove(pth)
        else:
            error_msg(pth + ' does not exists :/', "Delete source code file")