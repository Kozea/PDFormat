#!/usr/bin/env python

import sys
import collections

from gi.repository import Gtk


class Rectangle(collections.namedtuple('x1', 'x2', 'y1', 'y2')):
    """Horizontal rectangle between ``(x1, y1)`` and ``(x2, y2)``."""


class Source(object):
    def __init__(self, filename, page_number):
        self.filename = filename
        self.page_number = page_number


class Page(Gtk.ToolItemGroup):
    """Document page."""
    def __init__(self, source=None, rectangle=None):
        super(Page, self).__init__()
        self.source = source
        self.rectangle = rectangle


class Document(Gtk.Window):
    def __init__(self):
        super(Document, self).__init__()

        self.size = None
        self.orientation = None
        self.default_width = None
        self.default_height = None

        self.pages = Gtk.ListStore(object, str)

        self._draw()

        self.image_view.set_sensitive(False)

        Gtk.main()

    def add_page(self, tree):
        """Add a new page in ``tree``."""
        page = Page()
        page_length = self.pages.iter_n_children(None)
        self.pages.insert(page_length, (page, 'Page %i' % (page_length + 1)))
        tree.set_cursor(Gtk.TreePath('%i' % page_length), None, False)

    def selected_page(self, tree):
        """Called when a page is selected."""
        print(tree.get_cursor()[0].get_indices()[0])
        self.image_view.set_sensitive(True)

    def _draw(self):
        """Draw the window."""
        self.set_title('PDFormat')

        self.connect('destroy', lambda window: sys.exit())

        pane = Gtk.HPaned()
        self.add(pane)

        # View
        self.image_view = Gtk.VBox()
        pane.add1(self.image_view)

        toolbar = Gtk.Toolbar()

        change_document_button = Gtk.ToolButton()
        change_document_button.set_label('Change Document')
        change_document_button.set_icon_name('document-open')

        zoom_in_button = Gtk.ToolButton()
        zoom_in_button.set_label('Zoom In')
        zoom_in_button.set_icon_name('zoom-in')

        zoom_out_button = Gtk.ToolButton()
        zoom_out_button.set_label('Zoom Out')
        zoom_out_button.set_icon_name('zoom-out')

        select_all_button = Gtk.ToolButton()
        select_all_button.set_label('Select All')
        select_all_button.set_icon_name('edit-select-all')

        toolbar.insert(change_document_button, 0)
        toolbar.insert(zoom_in_button, 1)
        toolbar.insert(zoom_out_button, 2)
        toolbar.insert(select_all_button, 3)

        self.image_view.pack_start(toolbar, False, True, 0)

        scroll = Gtk.ScrolledWindow()
        self.image_view.pack_start(scroll, True, True, 1)

        # Pages
        self.page_view = Gtk.VBox()
        pane.add2(self.page_view)

        pages_tree = Gtk.TreeView()
        pages_tree.set_model(self.pages)
        pages_tree.set_reorderable(True)
        pages_tree.connect('cursor-changed', self.selected_page)

        name_column = Gtk.TreeViewColumn("Page")
        name_cell = Gtk.CellRendererText()
        name_column.pack_start(name_cell, True)
        name_column.add_attribute(name_cell, "text", 1)
        pages_tree.append_column(name_column)

        self.page_view.pack_start(pages_tree, True, True, 0)

        toolbar = Gtk.Toolbar()
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_INLINE_TOOLBAR)
        toolbar.set_icon_size(1)

        add_button = Gtk.ToolButton()
        add_button.connect(
            'clicked', lambda button: self.add_page(pages_tree))
        add_button.set_label('Add')
        add_button.set_icon_name('list-add-symbolic')

        remove_button = Gtk.ToolButton()
        remove_button.set_label('Remove')
        remove_button.set_icon_name('list-remove-symbolic')

        copy_button = Gtk.ToolButton()
        copy_button.set_label('Copy')
        copy_button.set_icon_name('edit-copy-symbolic')

        save_button = Gtk.ToolButton()
        save_button.set_label('Save')
        save_button.set_icon_name('document-save-symbolic')

        toolbar.insert(add_button, 0)
        toolbar.insert(remove_button, 1)
        toolbar.insert(copy_button, 2)
        toolbar.insert(save_button, 3)

        self.page_view.pack_start(toolbar, False, True, 1)

        self.show_all()

if __name__ == '__main__':
    Document()
