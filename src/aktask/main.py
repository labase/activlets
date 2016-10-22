#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Activlets
# Copyright 2013-2015 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
#
# Activlets é um software livre; você pode redistribuí-lo e/ou
# modificá-lo dentro dos termos da Licença Pública Geral GNU como
# publicada pela Fundação do Software Livre (FSF); na versão 2 da
# Licença.
#
# Este programa é distribuído na esperança de que possa ser útil,
# mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
# a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
# Licença Pública Geral GNU para maiores detalhes.
#
# Você deve ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa, se não, veja em <http://www.gnu.org/licenses/>

"""
O módulo aktask propõe um modelo de acesso a atividades ligadas a issues do github.

"""

from github import Github
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Activ Tasks")
        self.set_size_request(800, 400)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hbox, False, False, 0)

        vboxl = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vboxl, False, False, 0)

        self.listbox = Gtk.ListBox()
        vboxl.pack_start(self.listbox, True, True, 0)

        self.stack = Gtk.Stack(homogeneous=False)
        hbox.pack_start(self.stack, True, True, 0)

        self.fill_with_data()

        self.add(vbox)
        self.connect("destroy", Gtk.main_quit)

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
            print(str(os.getenv("AKTASK")))
            g = Github("cetoli", str(os.getenv("AKTASK")))
            issues = g.get_user("labase").get_repo("eica").get_issues()
            # Then play with your Github objects:
            for issue in issues:
                lbl = GtkIssue(":".join(l.name for l in issue.labels) + ": %s - %d" % (issue.title, issue.number))
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


class GtkIssue(Gtk.Box):
    def __init__(self, text="", i=0):
        super(GtkIssue, self).__init__(orientation=Gtk.Orientation.VERTICAL, border_width=3)
        # self.header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, border_width=50, spacing=5)
        # hdr = Gtk.Label("eica issue", xalign=0.0)
        # self.pack_start(self.header, False, False, 0)
        # self.header.pack_start(hdr, False, False, 0)
        lbl = Gtk.Label("%s - %d" % (text, i), xalign=0.0)
        self.pack_start(lbl, False, False, 0)
        self.progress = Gtk.ProgressBar()
        self.pack_start(self.progress, False, False, 0)


class Visitor:
    def __init__(self, gtk_builder):
        self.gtk_builder = gtk_builder

    def build_project(self, name=""):
        self.gtk_builder.build_list_item(name)

    def build_issue(self, name=""):
        self.gtk_builder.build_issue(name)

    def visit(self, model):
        class Caretaker:
            def update(self, **kwargs):
                return self.build_project(**kwargs) if len(kwargs) == 1 else self.build_issue(**kwargs)
        model.retriev(caretaker)

win = MainWindow()
win.show_all()
Gtk.main()
