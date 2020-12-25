"""
Clarisse

page module.
Define class Page, the canvas of type in types_supported.py.

by 1MLightyears@gmail.com

on 20201211
"""

from PySide2.QtWidgets import QPushButton,QScrollArea,QLineEdit,QLabel,QWidget,QFormLayout
from PySide2.QtCore import QThread, Signal, QSize, Qt

from . import output_dialog
from . import layouts
from . import log

import sys
import io
import re

__all__=["Page"]

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
    call_exit = Signal(str) # arg is function name (self.func.__name__) for each page in pages

    def __init__(self,
            func=None,
            func_args=[],
            func_kwargs={},
            margin=30,
            vert_spacing=10,
            current_layout="TopBottomLayout",
            description="",
            single_pass:bool=False,
            *args, **kwargs
        ):
        super().__init__()

        # static definitions
        self.func = func
        self.args = func_args
        self.kwargs = func_kwargs
        self.widget_list = []
        self.margin = margin
        self.vert_spacing = vert_spacing
        self.single_pass = single_pass
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.Current_Layout = layouts.Layout_Dict["TopBottomLayout"]
        if current_layout in layouts.Layout_Dict:
            self.Current_Layout = layouts.Layout_Dict[current_layout](self)
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
        self.canvas_layout.setRowWrapPolicy(self.canvas_layout.WrapAllRows)

        # default description is func.__doc__
        self.description = QLabel(self.getDescription(description)) # doesn't need to scroll
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

    def getDescription(self, pre_defined_desc: str = ""):
        """
        returns the description of current page.
        """
        if pre_defined_desc.strip(" \r\n") != "":
            return pre_defined_desc
        if self.func == None:
            log.error("No backend function found")
            return ""
        docstring = self.func.__doc__.strip(" \r\n\t")
        if docstring == "":
            log.warning("Bad docstring for function {0}".format(self.func.__name__))
            return "function {0}".format(self.func.__name__)

        # suppose "------" is the splitor between function description and arguments description
        # in numpy-style docstring, "------" has "Parameter" before it.
        # match it with "[a-zA-Z_]*?[\n\r]*?".
        desc_part = re.match(r"([\S\s\n\r]+?)[a-z_]*?[\n\r\s]*?------", docstring, re.M|re.I)
        if desc_part == None:
            log.info("whole description:\n{0}".format(docstring))
            return docstring
        log.info("recognized description:\n{0}".format(desc_part.group(1)))
        return desc_part.group(1)


    ### slot functions
    def Run(self):
        """
        Run the function(self.func) in another thread(self.run_thread).
        """
        # load args
        for i in self.widget_list:
            self.kwargs.update({i.objectName(): i.getValue()})

        # redirect standard output
        self.output_dialog = output_dialog.OutputDialog(self.func.__name__,parent=self)
        sys.stdout = self.output_dialog
        sys.stderr = self.output_dialog

        # avoid multiple clicks
        self.run_button.setText("Running...")
        self.run_button.setEnabled(False)
        self.run_thread.start()
        log.info("func \"{0}\" started".format(self.func.__name__))

        self.output_dialog.exec_()

    def Done(self):
        """
        Done is called when the function is finished(i.e. self.run_thread.finished is omitted)
        Restore the run button.
        """
        log.info("func \"{0}\" ended".format(self.func.__name__))
        self.output_dialog.setWindowTitle(
            "Output of {0} - returns {1}".format(
                self.func.__name__,
                self.run_thread.ret
            )
        )
        self.output_dialog.revive()
        self.run_button.setText("Run")
        self.run_button.setEnabled(True)
        if self.single_pass:
            self.call_exit.emit(self.func.__name__)