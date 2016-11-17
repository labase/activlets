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
import gi
import sys
from enum import Enum
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Handler:
    def __init__(self, builder):

        self.statusbar = builder.get_object("statusbar1")
        self.image = builder.get_object("image1")
        self.pixbuf = self.image.get_pixbuf()
        self.pixarray = self.pixbuf.get_pixels()

        class Offset:
            y = self.pixbuf.get_rowstride()
            x = self.pixbuf.get_n_channels()
        self.offset = Offset
        self.context_id = self.statusbar.get_context_id("example")

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        sys.exit(0)

    def onButtonPressed(self, button):
        print("Hello World!")

    def image_click(self, event, view=None):
        pass

    def on_image_click(self, target, event, view=None):
        pixel = self.pixarray[int(event.x * self.offset.x + event.y * self.offset.y)]
        pixelg = self.pixarray[int(event.x * self.offset.x + 1 + event.y * self.offset.y)]
        pixelb = self.pixarray[int(event.x * self.offset.x + 2+ event.y * self.offset.y)]
        self.statusbar.push(self.context_id, "x: %d, y: %d, pixel: %s, pixel: %s, pixel: %s"
                            % (event.x, event.y, pixel, pixelg, pixelb))


def update_image(image_area, data=None):
    return

    # remove the previous image
    for child in image_area.get_children():
        image_area.remove(child)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file("abudabi.jpg")
    image = Gtk.Image.new_from_pixbuf(pixbuf)
    # add a new image
    # image = Gtk.Image()
    # image.set_from_file("abudabi.jpg")
    image_area.add(image)
    image_area.show_all()


def main():
    builder = Gtk.Builder()
    builder.add_from_file("track.glade")
    builder.connect_signals(Handler(builder))
    window = builder.get_object("applicationwindow1")
    viewport = builder.get_object("viewport1")
    viewport.connect("draw", update_image)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
