"""
Clarisse

page module.
Define class Page, the canvas of type in types_supported.py.

by 1MLightyears@gmail.com

on 20201211
"""
import log

### Layouts
# TopBottom is the default layout
def TopBottomLayout(page, page_size):
    """
    set an top-bottom layout for page.
    """
    page.resize(page_size)

    # description should be placed on the top
    page.description.move(page.x()+page.margin,page.y()+page.margin)
    page.description.adjustSize()

    # run_button should be placed below description
    page.run_button.setGeometry(
        page.margin,
        page.description.y()+page.description.height()+page.margin,
        page_size.width() - 2*page.margin,
        page.run_button.height()
    )

    # canvas should be placed below run_button
    page.canvas.setGeometry(
        page.x(),
        page.run_button.y()+page.run_button.height(),
        page_size.width()-page.margin, # scroll has width
        page.canvas.height()
    )

    # widget_scroll should be placed between the end of page and run_button
    page.widget_scroll.setGeometry(
        page.x(),
        page.run_button.y()+page.run_button.height(),
        page_size.width(),
        page_size.height()-page.run_button.y()-page.run_button.height())

    return page

def LeftRightLayout(page, page_size):
    """
    set an left-right layout for page.
    """
    page.resize(page_size)
    log.info("page geometry={0}".format(page.geometry()))

    # run_button should be placed below description
    page.run_button.setGeometry(
        page.x()+page.margin,
        page_size.height()-page.margin-page.run_button.height(),
        page.description.width() - page.margin,
        page.run_button.height()
    )
    log.info("run_button geometry={0}".format(page.run_button.geometry()))

    # description should be placed on the left half of page
    page.description.move(page.x()+page.margin,page.y()+page.margin)
    page.description.adjustSize()
    page.description.resize(
        page.description.width(),
        page_size.height() - 2*page.margin - page.vert_spacing - page.run_button.height()
    )
    log.info("description geometry={0}".format(page.description.geometry()))

    # widget_scroll should be placed between the end of page and run_button
    page.widget_scroll.setGeometry(
        page.description.x()+page.description.width()+page.margin,
        page.y(),
        page_size.width()-page.description.width()-page.description.y(),
        page_size.height())
    log.info("widget_scroll geometry={0}".format(page.widget_scroll.geometry()))
    page.form_layout.setGeometry(page.widget_scroll.geometry())
    log.info("form_layout geometry={0}".format(page.form_layout.geometry()))

    # canvas should be placed on the right of description
    page.canvas.setGeometry(
        page.description.x()+page.description.width()+2*page.margin,
        page.y(),
        page_size.width()-page.description.width()-page.description.y()-page.margin, # scroll has width
        page_size.height()
    )
    log.info("canvas geometry={0}".format(page.canvas.geometry()))

    return page

### interface
Layout_Dict = {
    "TopBottomLayout": TopBottomLayout,
    "LeftRightLayout": LeftRightLayout
}
