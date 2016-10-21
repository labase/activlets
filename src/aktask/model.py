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


class Project:
    def __init__(self, name=None):
        self.name = name
        self.issue = []

    def retieve_issue(self, index):
        return self.issue[index]

    def insert_issue(self, **kwargs):
        issue = Issue(**kwargs)
        self.issue.append(issue)
        return issue

    def update(self, name=None):
        """
        Atividade programada para um projeto.

        :param name: Nome do projeto
        """
        self.name = name or self.name

    def accept(self, visitor):
        """
        Recebe um visitante.

        :param visitor: visitante
        :return:
        """
        visitor.visit(self)
        [issue.accept(visitor) for issue in self.issue]


class Issue:
    def __init__(self, number=0, title="", body="", user="", labels="", milestone="", state=0, size=0, assignee=None):
        """
        Atividade programada para um projeto.

        :param number: Número da atividade
        :param title: Descrição sucinta
        :param body: Descrição detalhada
        :param user: Criador da atividade
        :param labels: Rótulos associados à atividade
        :param milestone: Descrição da versão a que pertence
        :param state: Condição atual da atividade
        :param size: Tamanho em unidades de tempo
        :param assignee: Responsáveis pela execução
        """
        self.body = body
        self.number, self.title, self.user, self.labels, self.milestone, self.state, self.size, self.assignee =\
            number, title, user, labels, milestone, state, size, assignee

    def update(self, number=0, title="", body="", user="", labels="", milestone="", state=0, size=0, assignee=None):
        """
        Atividade programada para um projeto.

        :param number: Número da atividade
        :param title: Descrição sucinta
        :param body: Descrição detalhada
        :param user: Criador da atividade
        :param labels: Rótulos associados à atividade
        :param milestone: Descrição da versão a que pertence
        :param state: Condição atual da atividade
        :param size: Tamanho em unidades de tempo
        :param assignee: Responsáveis pela execução
        """
        self.body = body
        self.number, self.title, self.user, self.labels, self.milestone, self.state, self.size, self.assignee =\
            number or self.number, title or self.title, user or self.user, labels or self.labels, \
            milestone or self.milestone, state or self.state, size or self.size, assignee or self.assignee

    def retrieve(self, caretaker):
        """
        Transfere o memento para outro meio.
        :param caretaker: Recebedor do memento
        :return:
        """
        keys = "number, title, body, user, labels, milestone, state, size, assignee".split(", ")
        memento = {key: getattr(self, key) for key in keys}
        caretaker.update(**memento)

    def accept(self, visitor):
        """
        Recebe um visitante.

        :param visitor: visitante
        :return:
        """
        visitor.visit(self)


class Facade:
    class __FacadeSingleton:
        def __init__(self):
            self.model = {}

        def insert_project(self, name):
            self.model[name] = project = Project(name)
            return project

        def retrieve_project(self, name):
            return self.model[name] if name in self.model else None

        def insert_issue(self, name, **kwargs):
            return self.model[name].insert_issue(**kwargs)

        def retrieve_issue(self, name, index):
            return self.model[name].retieve_issue(index)

        def accept(self, visitor):
            [model.accept(visitor) for model in self.model.values()]
    __instance = None

    @classmethod
    def __instantiate(cls):  # __new__ always a classmethod
        Facade.__instance = Facade.__FacadeSingleton()
        Facade.__instantiate = lambda lcls=0: Facade.__instance
        return Facade.__instance

    def __new__(cls):  # __new__ always a classmethod
        return Facade.__instantiate()

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def __setattr__(self, name, value):
        return setattr(self.__instance, name, value)
