"""
############################################################
Quarto - Principal - Base
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/06/16
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from visual import Visual


class Kanban:
    """Base do jogo com tabuleiro e duas maos.
    """
    def __init__(self, gui):
        """Constroi as partes do Jogo. """
        self.kanban = self.build_pending(gui)
        self.kanban = self.build_running(gui)
        #self.monta_mao(gui)
        #self.monta_tabuleiro(gui)

    def build_pending(self, gui):
        """Monta a casa que fica na base. """
        self.section = gui.build_section()
        self.base = gui.build_task()

    def build_running(self, gui):
        """Monta a casa que fica na base. """
        self.section = gui.build_section()
        self.base = gui.build_task()
        self.base = gui.build_task()


def main(doc,gui):
    print('Kanban 0.1.0')
    Kanban(Visual(doc,gui))
