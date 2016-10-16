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
from model import Facade


class MainControl:
    def __init__(self):
        self.model = Facade().insert_project("eica")

    def fill_with_data(self):
        def _list_repos():
            print(str(os.getenv("AKTASK")))
            g = Github("cetoli", str(os.getenv("AKTASK")))
            issues = g.get_user("labase").get_repo("eica").get_issues()
            # Then play with your Github objects:
            for issue in issues:
                label = ":".join(l.name for l in issue.labels) + ": %s - %d" % (issue.title, issue.number)
                self.model.insert_issue("eica", title=label)
        _list_repos()
