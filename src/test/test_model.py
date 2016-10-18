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
from aktask.model import Issue, Facade, Project
from unittest.mock import MagicMock, call  # , patch, ANY


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
        self.assertIsInstance(self.app, Issue, "Issue of __instance not created")

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

    def test_facade_singleton(self):
        """verifica se facade é singleton"""
        self.assertIs(Facade(), Facade())

    def test_facade_manage_project(self):
        """insere e recupera projeto"""
        project = Facade().insert_project("test")
        self.assertIsInstance(project, Project, "%s not instance of Project" % project)
        project = Facade().retrieve_project("test")
        self.assertIsInstance(project, Project, "%s not instance of Project" % project)

    @staticmethod
    def _test_facade_manage_issue(project="test", **kwargs):
        """insere e recupera issue"""
        proj = Facade().insert_project(project)
        return proj, Facade().insert_issue(project, **kwargs)

    def test_facade_manage_issue(self):
        """insere e recupera issue"""
        _, issue = self._test_facade_manage_issue("test", title="issue")
        self.assertIsInstance(issue, Issue, "%s not instance of Issue" % issue)
        issue = Facade().retrieve_issue("test", 0)
        self.assertIsInstance(issue, Issue, "%s not instance of Issue" % issue)
        self.assertEqual(issue.title, "issue", "Issue title is not issue, else is %s" % issue.title)

    def test_facade_visit_issue(self):
        """visita issue"""
        project, issue = self._test_facade_manage_issue("test", title="issue")
        visitor = MagicMock("visitor")
        visitor.visit = MagicMock("visit")
        self.assertIsInstance(issue, Issue, "%s not instance of Issue" % issue)
        Facade().accept(visitor)
        self.assertEqual(visitor.visit.call_count, 2)
        calls = [call(project), call(issue)]
        visitor.visit.assert_has_calls(calls)

    def test_facade_visit_effect_issue(self):
        """visita issue com efeito"""
        names = [dict(name="part"), dict(title="issue0")]
        project, issue = self._test_facade_manage_issue("test", title="issue")
        visitor = MagicMock("visitor")
        visitor.visit = MagicMock("visit")
        visitor.visit.side_effect = lambda p: p.update(**names.pop(0))
        # visitor.visit.side_effect = [lambda p: p.update(name="project0"), lambda i: i.update(title="issue0")]
        Facade().accept(visitor)
        self.assertEqual(visitor.visit.call_count, 2)
        calls = [call(project), call(issue)]
        visitor.visit.assert_has_calls(calls)
        self.assertEqual(project.name, "part")
        self.assertEqual(issue.title, "issue0")

if __name__ == '__main__':
    unittest.main()
