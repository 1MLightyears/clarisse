"""
Clarisse

page module.
Define class Page, the canvas of type in types_supported.py.

by 1MLightyears@gmail.com

on 20201211
"""
from PySide2.QtCore import QSize

import log

### Layouts
# BaseLayout is not used, only to save code for __init__() and bind()
class BaseLayout:
    def __init__(self, page=None):
        self.page = page
        self.minimum_window_size = QSize(480, 480)  # a default size for window
        # TODO: it is not a good way to define a default size by using minimun_window_size
        # need a better idea by sensing widgets size and define default size for a layout

    def bind(self, page=None):
        page = page or self.page
        # bind parentship
        # main_window -> central_widget -> page ->  widget_scroll -> canvas -> layout
        page.widget_scroll.setWidget(page.canvas)
        page.canvas.setLayout(page.canvas_layout)

        return page

# TopBottom is the default layout
class TopBottomLayout(BaseLayout):
    """
    set an top-bottom layout for page.
    """
    def apply(self, page=None):
        page = self.bind(page or self.page)

        # description should be placed on the top
        page.description.move(page.margin, page.margin)
        page.description.adjustSize()

        # run_button should be placed below description
        page.run_button.setGeometry(
            page.margin,
            page.description.y()+page.description.height()+page.margin,
            page.width() - 2*page.margin,
            page.run_button.height()
        )

        # widget_scroll should be placed between the end of page and run_button
        page.widget_scroll.setGeometry(
            0,
            page.run_button.y()+page.run_button.height() + page.margin,
            page.width(),
            page.height() - page.run_button.y() - page.run_button.height()-page.margin
        )

        # canvas should be placed in widget_scroll with a margin = page.margin
        page.canvas.setGeometry(
            page.margin,
            page.margin,
            page.widget_scroll.width() - page.margin,
            page.canvas.height()
        )
        page.canvas_layout.setGeometry(page.canvas.geometry())

        self.minimum_window_size=QSize(320,480)
        return page

    def resize(self, page, page_size):
        page=page or self.page
        page.resize(page_size)

        # run_button should be always placed below description
        page.run_button.setGeometry(
            page.margin,
            page.description.y()+page.description.height()+page.margin,
            page_size.width() - 2*page.margin,
            page.run_button.height()
        )

        # widgets should be placed below run_button
        page.widget_scroll.resize(
            page.width(),
            page.height() - page.run_button.y() - page.run_button.height()-page.margin
        )
        page.canvas.resize(
            page.widget_scroll.width() - page.margin,
            page.canvas.height()
        )

        return page

class LeftRightLayout(BaseLayout):
    """
    set an left-right layout for page.
    """
    def apply(self, page=None):
        page = self.bind(page or self.page)

        # description should be placed on the top-left part of page
        page.description.move(page.margin,page.margin)
        page.description.adjustSize()

        # run_button should be placed at the bottom-left part of page
        page.run_button.setGeometry(
            page.margin,
            page.height()-page.run_button.height()-page.margin,
            page.description.width(),
            page.run_button.height()
        )

        # widget_scroll should be placed on the rest right place of the page
        page.widget_scroll.setGeometry(
            page.description.x()+page.description.width() + page.margin,
            0,
            page.width() - page.description.width() - page.margin,
            page.height() - page.margin
        )

        # canvas should be placed in widget_scroll with a margin = page.margin
        page.canvas.setGeometry(
            page.margin,
            page.margin,
            page.widget_scroll.width() - page.margin,
            page.canvas.height()
        )
        page.canvas_layout.setGeometry(page.canvas.geometry())

        self.minimum_window_size = QSize(640, 320)
        return page

    def resize(self, page, page_size):
        page=page or self.page
        page.resize(page_size)

        # run_button should be always placed at the left-bottom of the page
        page.run_button.move(page.margin,page.height()-page.run_button.height()-page.margin)

        # widgets should be placed on the right of the page
        page.widget_scroll.resize(
            page.width()-page.description.width()-page.margin,
            page.height()
        )
        page.canvas.resize(
            page.widget_scroll.width() - page.margin,
            page.canvas.height()
        )

        return page

### interface
Layout_Dict = {
    "TopBottomLayout": TopBottomLayout,
    "LeftRightLayout": LeftRightLayout
}
