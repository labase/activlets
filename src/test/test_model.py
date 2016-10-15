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
O testa o modelo de aktask.

"""
import unittest
from aktask.model import Issue
from unittest.mock import MagicMock  # , patch, ANY


class IssueTest(unittest.TestCase):
    class Evento:
        x = y = 42
    EV = Evento()

    def setUp(self):
        self.caretaker = MagicMock(name="caretaker")
        keys = "number, title, body, user, labels, milestone, state, size, assignee".split(", ")

        self.issue0 = {key: key+"0" for key in keys}
        self.issue1 = {key: key+"1" for key in keys}

        self.app = Issue(**self.issue0)

    def test_create(self):
        """cria um issue"""
        self.assertIsInstance(self.app, Issue, "Issue of instance not created")

    def test_update(self):
        """atualiza um issue"""
        attr_in_issue0 = all(True for attr in self.issue0 if getattr(self.app, attr) in self.issue0.values())
        self.assertTrue(attr_in_issue0, "Issue mismatch contents with issue 0 %s" % self.issue0.values())
        self.app.update(**self.issue1)
        attr_in_issue1 = all(True for attr in self.issue0 if getattr(self.app, attr) in self.issue1.values())
        self.assertTrue(attr_in_issue1, "Issue mismatch contents with issue 1 %s" % self.issue1.values())

    def test_retrieve(self):
        """recupera valores de um issue"""
        self.app.retrieve(self.caretaker)
        self.caretaker.update.assert_called_with(**self.issue0)
