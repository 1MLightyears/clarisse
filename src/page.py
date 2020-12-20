"""
Clarisse

page module.
Define class Page, the canvas of type in types_supported.py.

by 1MLightyears@gmail.com

on 20201211
"""

from PySide2.QtWidgets import QPushButton,QScrollArea,QLineEdit,QLabel,QWidget,QFormLayout
from PySide2.QtCore import QThread, Signal, QSize, Qt

from output_dialog import show_output
from layouts import Layout_Dict

import log
import sys
import io

__all__=["Page","PageCanvas"]

class RedirectIO():
    def __init__(self, s: str = ""):
        self.content = s
    def write(self, s):
        self.content+=str(s)
    def read(self):
        return self.content.strip(" \n")

class RunThread(QThread):
    """
    The real function-executor.
    """
    def __init__(self,func,func_args:tuple=(),func_kwargs:dict={},parent=None, *args, **kwargs):
        super().__init__(parent=None, *args, **kwargs)
        self.func = func
        self.args = func_args
        self.kwargs = func_kwargs
        self.ret=None

    def run(self):
        log.info("run func with args={0},kwargs={1}".format(self.args,self.kwargs))
        self.ret = self.func(*self.args, **self.kwargs)
        log.info("func returns {0}".format(self.ret))
        return self.ret

class Page(QWidget):
    def __init__(self,
            func=None,
            func_args=[],
            func_kwargs={},
            margin=30,
            vert_spacing=10,
            current_layout="TopBottomLayout",
            description="",
            *args, **kwargs
        ):
        super().__init__()

        # static definitions
        self.func = func
        self.args = func_args
        self.kwargs = func_kwargs
        self.widget_list = []
        self.margin = margin
        self.vert_spacing =vert_spacing
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.Current_Layout = Layout_Dict["TopBottomLayout"]
        if current_layout in Layout_Dict:
            self.Current_Layout=Layout_Dict[current_layout](self)

        # Initiallize
        self.canvas = QWidget()
        self.canvas.setObjectName("canvas")

        # create a scroll bar
        self.widget_scroll = QScrollArea(self)
        self.widget_scroll.setObjectName("widget_scroll")

        # use a QFormLayout to place widgets
        self.canvas_layout = QFormLayout()
        self.canvas_layout.setObjectName("canvas_layout")

        # set canvas_layout
        self.canvas_layout.setMargin(self.margin)
        self.canvas_layout.setSpacing(self.vert_spacing)
        self.canvas_layout.setRowWrapPolicy(self.canvas_layout.WrapLongRows)

        # default description is func.__doc__
        description = self.func.__doc__ if description=="" else description
        self.description = QLabel(description) # doesn't need to scroll
        self.description.setParent(self)
        self.description.setWordWrap(True)
        self.description.setTextFormat(Qt.MarkdownText)
        self.description.setOpenExternalLinks(True)

        # create a Run button to excute the function
        self.run_button = QPushButton("&Run", self)
        self.run_button.clicked.connect(self.Run)
        self.run_button.adjustSize()

        # allow the user to run the func multiple times to test output
        # but only the last return is delivered (as a confirmed run)
        self.run_thread = RunThread(self.func, self.args, self.kwargs)
        self.run_thread.finished.connect(self.Done)

    ### slot functions
    def Run(self):
        """
        Run self.func in another thread.
        """
        for i in self.widget_list:
            self.kwargs.update({i.objectName(): i.getValue()})

        # redirect standard output
        self.redirect_IO = RedirectIO()
        sys.stdout = self.redirect_IO
        sys.stderr = self.redirect_IO

        # avoid multiple clicks
        self.run_button.setText("Running...")
        self.run_button.setEnabled(False)
        self.run_thread.start()

    def Done(self):
        """
        Restore run_button.
        """
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        show_output(self.redirect_IO.read(),self.func.__name__,self.run_thread.ret)
        self.run_button.setText("Run")
        self.run_button.setEnabled(True)