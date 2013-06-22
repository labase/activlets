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
        #self.monta_base(gui)
        #self.monta_mao(gui)
        #self.monta_tabuleiro(gui)

    def monta_base(self, gui):
        """Monta a casa que fica na base. """
        self.base = gui.monta_base()

    def monta_tabuleiro(self, gui):
        """Monta o tabuleiro onde se joga as pecas. """
        self.tabuleiro = Tabuleiro(gui)

    def monta_mao(self, gui):
        """Monta o espaco onde ficam as pecas no inicio. """
        self.mao = Mao(gui)


def main(doc,gui):
    print('Kanban 0.1.0')
    Kanban(Visual(doc,gui))
