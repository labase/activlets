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
from aktask.control import MainControl
from unittest.mock import MagicMock, call, patch, ANY


class IssueTest(unittest.TestCase):
    class Evento:
        x = y = 42
    EV = Evento()

    def setUp(self):
        self.caretaker = MagicMock(name="caretaker")
        keys = "number, title, body, user, labels, milestone, state, size, assignee".split(", ")
        self.façade = Facade()
        Facade().use_with_caution_empty_facade_model()

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

    def _test_facade_manage_issue(self, project="test", **kwargs):
        """insere e recupera issue"""
        proj = self.façade.insert_project(project)
        return proj, self.façade.insert_issue(project, **kwargs)

    def test_facade_manage_issue(self):
        """insere e recupera issue"""
        _, issue = self._test_facade_manage_issue("test", title="issue")
        self.assertIsInstance(issue, Issue, "%s not instance of Issue" % issue)
        issue = Facade().retrieve_issue("test", "0")
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
        mc = visitor.mock_calls
        calls = [call(project), call(issue)]
        visitor.visit.assert_has_calls(calls)

    def _mock_github(self):
        with patch("github.Github") as MockGh:
            instance = MockGh.return_value
            instance.get_user.return_value = instance.get_repo.return_value = instance
            mockissue = MagicMock("mockissue")
            mockmile = MagicMock("mockmile")
            mockmile.title = "issue.milestone"
            mockmile.return_value = True
            instance.get_issues.return_value = [mockissue]
            mockissue.labels = [{"la": "red"}, {"lb": "green"}]
            mockissue.title = "ta"
            mockissue.number = "2016"
            mockissue.body = "issue.body"
            mockissue.milestone = mockmile
            mockissue.state = "issue.state"
            return instance, mockmile

    def test_control_fill_with_data(self):
        """le do github e escreve no modelo"""
        mc = MainControl()
        self.assertIsNotNone(self.façade.retrieve_project("eica"), "MainControl failed to create eica")
        mg, mm = self._mock_github()
        mc.fill_with_data(reader=mg)
        print(mm.call_count)
        mg.get_user.assert_called_once_with("labase")
        mg.get_repo.assert_called_once_with("eica")
        issue = self.façade.retrieve_issue("eica", "2016")
        self.assertIsNotNone(issue, "Facade failed to index issue")
        self.assertEqual(issue.milestone, "issue.milestone")

    def _mock_gtk_writer(self):
        MockGh = MagicMock("MockGh")
        visitor = MagicMock("visitor")
        visitor.update = visitor
        instance = MockGh.return_value
        instance.visit.side_effect = lambda vis: vis.retrieve(visitor)
        return instance, visitor

    def test_control_render_data_to_gui(self):
        """le do modelo e escreve no gtk"""

        def Any(cls):
            class Any(cls):
                def __eq__(self, other):
                    return True

            return Any()
        mc = MainControl()
        project = self.façade.retrieve_project("eica")
        self.assertIsNotNone(project, "MainControl failed to create eica")
        mgtk, visitor = self._mock_gtk_writer()
        mc.fill_with_data(reader=self._mock_github()[0])
        mc.render_data_to_gui(writer=mgtk)
        issue = self.façade.retrieve_issue("eica", "2016")
        mgtk.visit.assert_any_call(issue)
        mgtk.visit.assert_any_call(project)
        self.assertEqual(2, mgtk.visit.call_count)
        visitor.update.assert_any_call(name="eica")
        issuedict = dict(assignee=None, body='issue.body', labels=[{'la': 'red'}, {'lb': 'green'}],
                         milestone='issue.milestone', number='2016', size=0, state='issue.state', title='ta', user='')
        # cl = visitor.call_args_list
        # assert cl[1] == issuedict, cl[1]
        visitor.update.assert_any_call(**issuedict)
        self.assertEqual(2, visitor.update.call_count)

if __name__ == '__main__':
    unittest.main()
