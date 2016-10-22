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
import os
from aktask.model import Facade


class MainControl:
    def __init__(self):
        self.model = Facade().insert_project("eica")

    def render_data_to_gui(self, writer=None):
        Facade().accept(writer)
        pass

    def fill_with_data(self, reader=None):
        # print(str(os.getenv("AKTASK")))
        g = reader or Github("cetoli", str(os.getenv("AKTASK")))
        issues = g.get_user("labase").get_repo("eica").get_issues()

        for issue in issues:
            Facade().insert_issue("eica", number=issue.number, title=issue.title, body=issue.body,
                                  labels=issue.labels,
                                  milestone=issue.milestone.title if issue.milestone is not None else "",
                                  state=issue.state, size=0)
