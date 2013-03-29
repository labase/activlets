#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kanban - Agile Workflow - Test Gui
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/03/29
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br)"
__version__ = "0.1"
__date__    = "2013/03/29"

        
import mocker
from mocker import Mocker,KWARGS, ARGS, ANY, CONTAINS, MATCH, expect
from kanban import GUI

class TestMain(mocker.MockerTestCase):
  """Testes unitários para o Kanban"""

  def setUp(self):
    self.mock_gui = Mocker()
    self.mock_avt = Mocker()
    self.mg = self.mock_gui.mock()
    self.ma = self.mock_gui.mock()

  def tearDown(self):
    self.mock_gui.restore()
    self.mock_avt.restore()
    self.mock_avt.verify()
    self.mock_avt = None
    self.app = None
    pass

  def _expect_all_kanban(self):
    "main class expectations"
    # create colors
    expect(self.mg.DIV('', KWARGS, Class='rounded-corners', draggable=True,
                       )).result(self.ma)#.count(1,16)
    expect(self.mg['head'].__le__(ANY))#.count(1,16)
    #expect(self.mg.set_attrs(ANY, ondragstart = ANY,onmouseover = ANY,
    #        ondragover = ANY, ondrop = ANY)).count(1,16)
    #expect(self.mg.handler(ARGS)).count(1,7)
    #expect(self.mg.image(ARGS,KWARGS)).count(1)
    #expect(self.mg.rect(ARGS,KWARGS)).count(1,2).result(self.mg)
    #expect(self.mg.dialog(ARGS,KWARGS)).count(1,2).result(self.mg)
    #expect(self.mg.hide()).count(0,2).result(self.mg)
    #expect(self.mg.text(ARGS,KWARGS)).result(self.mg).count(1,6)
    #expect(self.ma.move(ARGS))
    #expect(self.mg.textarea(ARGS))
    #expect(self.mg(ARGS)).count(1,96).result(self.ma)
    ##expect(self.mg.textContent = ANY).count(0,6)
  def _replay_and_create_main(self,p = '.&.'):
    "create main"
    self.mock_gui.replay()
    self.app = GUI(self.mg, self.mg)
    print('---- NOW OPERATIONS ----')
  def test_create_gui(self):
    "create gui"
    self._expect_all_kanban()
    self._replay_and_create_main()
  def test_create_div(self):
    "create div"
    self._expect_all_kanban()
    self._replay_and_create_main()
    div = self.app.div('','head', draggable=True, id='div_id')
  def test_set_attr(self):
    "create set attr"
    self._expect_all_kanban()
    expect(setattr( self.ma, 'top' , 10))#.count(1,16)
    self._replay_and_create_main()
    div = self.app.div('','head', draggable=True, id='div_id')
    self.app.set_attrs(div, top=10)
  def test_set_style(self):
    "create set style"
    self._expect_all_kanban()
    expect(setattr( self.ma, 'style' , {'top': 10}))#.count(1,16)
    self._replay_and_create_main()
    div = self.app.div('','head', draggable=True, id='div_id')
    self.app.set_style(div, top=10)
if __name__ == '__main__':
    import unittest
    unittest.main()