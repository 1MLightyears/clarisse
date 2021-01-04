"""
Clarisse

output module.
The output module defines a dialog that capture all the output sended to stdout & stderr,
and show them in an QtWidgets.QTextEdit.

by 1MLightyears@gmail.com

on 20201221
"""

from PySide2.QtWidgets import QDialog, QTextEdit
from PySide2.QtCore import Qt

import sys

__all__ = ["OutputDialog"]


class OutputDialog(QDialog):
    def __init__(self, func_name: str = "", s: str = "", *args, **kwargs):
        super(OutputDialog, self).__init__(*args, **kwargs)
        self.resize(400, 300)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle("Output of {0}".format(func_name))

        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.output_text = QTextEdit(self)
        self.output_text.setText(s)
        self.output_text.setGeometry(0, 0, self.width(), self.height())
        self.output_text.setReadOnly(True)

    def __del__(self):
        self.revive()

    def revive(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def resizeEvent(self, event):
        super(OutputDialog, self).resizeEvent(event)
        self.output_text.resize(self.size())

    def write(self, info: str = ""):
        self.output_text.insertPlainText(info)
