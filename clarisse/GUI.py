"""
Clarisse

Window drawing module.
analyze the interface of a function/class.

by 1MLightyears@gmail.com

on 20201211
"""
from . import analyze
from . import page
from . import log

import sys
import os

from PySide2.QtWidgets import QMainWindow, QApplication, QLabel, QTabWidget, QWidget
from PySide2.QtCore import Signal, QCoreApplication, QMetaObject, QSize
from PySide2.QtGui import QColor, QIcon

__all__ = ["ClrsGUI"]


class Ui_MainWindow(QMainWindow, object):
    OnResize = Signal(QSize)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(
            480, 480
        )  # TODO: find a better way for this instead of set a hard value

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def resizeEvent(self, e):
        super(QMainWindow, self).resizeEvent(e)
        self.OnResize.emit(self.size())


class ClrsGUI:
    def __init__(self):
        """
        Create and set the Main_Window.
        """
        log.info("ClrsGUI init")
        self.app = QApplication(sys.argv)
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self.main_window)
        log.info(
            "main_window create size={size}".format(size=self.main_window.geometry())
        )

        self.central_widget = QWidget(self.main_window)
        self.central_widget.resize(self.main_window.size())
        self.central_widget.setObjectName("central_widget")

        self.main_window.setCentralWidget(self.central_widget)
        self.main_window.OnResize.connect(self.ReDrawAllPages)

    def Parse(
        self,
        backend,
        default_args: tuple = (),
        default_kwargs: dict = {},
        args_desc: list = [],
        args_kwdesc: dict = {},
        icon: str = "",
        *args,
        **kwargs
    ):
        """
        Parse the decorated.
        """
        self.pages = []
        self.tabs = None

        # try to load a prepared icon with backend.__name__ or a given path
        if icon == "":
            icon = backend.__name__ + ".ico"
        if os.path.exists(icon):
            log.info("load WindowIcon from path={0}".format(icon))
            self.main_window.setWindowIcon(QIcon(icon))

        # if backend is a function
        if isinstance(backend, type(lambda: 0)):
            # then args and kwargs store the default of all variables
            # one page for each function.
            self.pages.append(page.Page(backend, *args, **kwargs))
            self.pages[-1].setParent(self.central_widget)
            self.pages[-1].setObjectName("page{0}".format(str(len(self.pages) - 1)))
            self.pages[-1].call_exit.connect(self.main_window.close)

            # draw description(QLabel), the Run button, args as widgets in the current page.
            self.DrawFuncInPage(
                self.pages[0],
                backend,
                default_args,
                default_kwargs,
                args_desc,
                args_kwdesc,
            )

            self.main_window.setWindowTitle(
                "{0} - Clarisse GUI".format(backend.__name__)
            )
        elif isinstance(backend, object):
            self.tabs = QTabWidget(self.central_widget)
            # TODO:fill the codes; support classes
            # if backend is a class, decorate its __init__, make all its callable public
            # a page and organize them with self.tabs

    def DrawFuncInPage(
        self,
        page,
        func,
        default_args: tuple = (),
        default_kwargs: dict = {},
        args_desc: list = [],
        args_kwdesc: dict = {},
    ):
        """
        Draw parameters of function(func) in the main_window,
        set them with appropriate initial values.
        """
        # inspect func
        page.widget_list = analyze.AnalyzeFunc(func)
        log.info(
            "start of draw page, widget_list={0}".format(
                [i.__name__ for i in page.widget_list]
            )
        )

        # add widgets to canvas
        if page.widget_list != []:
            top = 0
            for i in range(len(page.widget_list)):
                # get label text before widget
                row_desc = page.widget_list[i].objectName()
                if len(args_desc) > 0:
                    row_desc = args_desc[0]
                    args_desc = args_desc[1:]
                if page.widget_list[i].objectName() in args_kwdesc:
                    row_desc = args_kwdesc[page.widget_list[i].objectName()]
                page.canvas_layout.addRow(QLabel(row_desc), page.widget_list[i])

                # apply arguments given to the original func as default args
                if len(default_args) > 0:
                    page.widget_list[i].setDefault(default_args[0])
                    default_args = default_args[1:]
                if page.widget_list[i].objectName() in default_kwargs:
                    page.widget_list[i].setDefault(
                        default_kwargs[page.widget_list[i].objectName()]
                    )

                log.info(
                    "add widget name={name}, geometry={geometry}, desc={desc}".format(
                        name=page.widget_list[i].objectName(),
                        geometry=page.widget_list[i].geometry(),
                        desc=row_desc,
                    )
                )

        # canvas resize to fit widgets
        page.canvas.resize(
            page.canvas.width(),
            page.widget_list[-1].size().width() + page.widget_list[-1].size().height(),
        )
        # layout resize to initial size
        page = page.Current_Layout.apply(page)
        self.main_window.setMinimumSize(
            page.Current_Layout.minimum_window_size.width(),
            page.Current_Layout.minimum_window_size.height(),
        )
        self.main_window.adjustSize()
        log.info("end of draw page")

        # modify Z-order
        page.run_button.raise_()
        page.description.raise_()

    def ReDrawAllPages(self, new_size: QSize = QSize(640, 480)):
        """
        redraw each page to fit the form's size.
        """
        # tabs should adjust size
        if self.tabs != None:
            self.tabs.resize(new_size)
        for page in self.pages:
            page = page.Current_Layout.resize(page, new_size)
            # debug info
            target = page.canvas_layout
            while not (target.objectName() == None):
                log.info(
                    "{0} reset to {1}".format(target.objectName(), target.geometry())
                )
                if target.parent() != None:
                    target = target.parent()
                else:
                    break

        log.info("resize finished")

    def getReturn(self):
        """
        Get the return value of the backend.
        """
        return self.pages[0].run_thread.ret  # TODO: change here when class is supported
