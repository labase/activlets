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
        self.object_being_built = self
        self.build_stack = []
        self.stack_layer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, border_width=50, spacing=5)

        self.stack = Gtk.Stack(homogeneous=False)
        self.listbox = Gtk.ListBox()
        self.build_window()

    def build(self, part=""):
        self.object_being_built.add(part)
        self.object_being_built = self.build_stack.pop() if self.build_stack else self.object_being_built

    def build_window(self, name=""):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.pack_start(hbox, False, False, 0)

        vboxl = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vboxl, False, False, 0)

        vboxl.pack_start(self.listbox, True, True, 0)

        hbox.pack_start(self.stack, True, True, 0)

        self.add(vbox)
        self.connect("destroy", Gtk.main_quit)
        self.build_stack.append(self.listbox)

    def build_issue(self, **kwargs):
        lbl = GtkIssue(**kwargs)
        self.stack_layer.pack_start(lbl, False, False, 0)
        self.build_stack.append(self.stack)

    def build_list(self, name=""):
        lbl = Gtk.Label(name, xalign=0.0)
        row = Gtk.ListBoxRow()
        row.add(lbl)
        self.listbox.add(row)
        self.stack.add_named(self.stack_layer, name)
        self.build_stack.append(self.stack)


class GtkIssue(Gtk.Box):
    def __init__(self, title="", number=0, **kwargs):
        super(GtkIssue, self).__init__(orientation=Gtk.Orientation.VERTICAL, border_width=3)
        lbl = Gtk.Label("%s - %d" % (title, number), xalign=0.0)
        self.pack_start(lbl, False, False, 0)
        self.progress = Gtk.ProgressBar()
        self.pack_start(self.progress, False, False, 0)


class Visitor:
    def __init__(self, gtk_builder):
        self.gtk_builder = gtk_builder

    def build_project(self, name=""):
        self.gtk_builder.build_list(name)

    def build_issue(self, **kwargs):
        self.gtk_builder.build_issue(**kwargs)

    def update(self, **kwargs):
        return self.build_project(**kwargs) if len(kwargs) == 1 else self.build_issue(**kwargs)

    def visit(self, model):
        model.retrieve(self)

if __name__ == '__main__':
    from aktask.control import MainControl
    control = MainControl()
    control.fill_with_data()
    win = MainWindow()
    control.render_data_to_gui(writer=Visitor(gtk_builder=win))
    win.show_all()
    Gtk.main()
