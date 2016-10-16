from github import Github
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Window")
        self.set_size_request(800, 400)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.header = Gtk.HeaderBar()
        vbox.pack_start(self.header, False, False, 0)

        icon = Gtk.Image()
        icon.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.BUTTON)
        self.button = Gtk.ToggleButton()
        self.button.add(icon)
        self.button.connect("toggled", self._on_transition)
        self.header.pack_start(self.button)
        # label = Gtk.Label("This is a Label")
        # header.pack_end(label)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hbox, False, False, 0)

        vboxl = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vboxl, False, False, 0)

        self.revealer = Gtk.Revealer()
        self.entry = Gtk.SearchEntry(
            placeholder_text="Search Projects")
        self.entry.props.margin_left = 15
        self.entry.props.margin_right = 15
        self.entry.props.margin_top = 5
        self.entry.props.margin_bottom = 5
        self.entry.connect("search-changed", self._on_search)
        self.revealer.add(self.entry)
        vboxl.pack_start(self.revealer, False, False, 0)
        self.listbox = Gtk.ListBox()
        self.listbox.connect("row-selected", self._on_select_row)
        self.listbox.set_filter_func(self._list_filter_func, None)
        vboxl.pack_start(self.listbox, True, True, 0)

        self.stack = Gtk.Stack(homogeneous=False)
        hbox.pack_start(self.stack, True, True, 0)

        self.fill_with_data()

        self.add(vbox)
        self.connect("key-press-event", self._on_key_press)
        self.connect("destroy", Gtk.main_quit)

    def _on_search(self, _):
        self.listbox.invalidate_filter()

    def _list_filter_func(self, lista, _):
        text = self.entry.get_text()
        if not text:
            return lista
        lbl = lista.get_child()
        if text.lower() in lbl.get_text().lower():
            return lista

    def _on_transition(self, btn):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            self.entry.set_text("")
            btn.grab_focus()
        else:
            self.revealer.set_reveal_child(True)
            self.entry.grab_focus()

    def _on_key_press(self, _, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == 'Escape':
            self.button.set_active(False)
        if event.state and Gdk.ModifierType.CONTROL_MASK:
            if keyname == 'f':
                self.button.set_active(True)

    def fill_with_data(self):

        def _items_box(text):
            lbl = Gtk.Label(text, xalign=0.0)
            row = Gtk.ListBoxRow()
            row.add(lbl)
            return row

        def _list_repos(text):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                          border_width=50,
                          spacing=5)
            g = Github("cetoli", "labase.g1thub")
            issues = g.get_user("labase").get_repo("eica").get_issues()
            # Then play with your Github objects:
            for issue in issues:
                lbl = Gtk.Label(":".join(l.name for l in issue.labels) + ": %s - %d" % (issue.title, issue.number), xalign=0.0)
                box.pack_start(lbl, False, False, 0)
            self.stack.add_named(box, text)

        def _lots_of_labels(text):
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                          border_width=50,
                          spacing=5)
            for i in range(15):
                lbl = Gtk.Label("%s - %d" % (text, i), xalign=0.0)
                box.pack_start(lbl, False, False, 0)
            self.stack.add_named(box, text)

        text = ["Github"]
        for cat in text:
            btn = _items_box(cat)
            self.listbox.add(btn)
            if cat == "Github":
                _list_repos(cat)
            else:
                _lots_of_labels(cat)

        widget = self.listbox.get_row_at_index(0)
        self.listbox.select_row(widget)

    def _on_select_row(self, listbox, row):
        group = row.get_child().get_text()
        self.stack.set_visible_child_name(group)
        self.header.set_title(group)


class GtkIssue(Gtk.Box):
    def __init__(self, text, i):
        super(GtkIssue, self).__init__(orientation=Gtk.Orientation.VERTICAL)
        self.header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, border_width=50, spacing=5)
        self.pack_start(self.header, False, False, 0)
        lbl = Gtk.Label("%s - %d" % (text, i), xalign=0.0)
        self.pack_start(lbl, False, False, 0)
        self.progress = Gtk.ProgressBar()
        self.pack_start(self.progress, False, False, 0)

win = MainWindow()
win.show_all()
Gtk.main()
