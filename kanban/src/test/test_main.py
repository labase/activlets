#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Kanban - Agile Workflow - Main Test
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
from kanban import main

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
    expect(self.mg.div('', KWARGS, Class='color-tabs', draggable=True,
                       node='head')).result(self.ma).count(1,16)
    expect(self.mg.set_style(ANY, KWARGS, top = 10, height= 16, width= 16,
      position='absolute')).count(1,16)
    expect(self.mg.set_attrs(ANY, ondragstart = ANY,onmouseover = ANY,
            ondragover = ANY, ondrop = ANY)).count(1,16)
    # create panels
    expect(self.mg.div('', KWARGS, Class='task-panel', 
                       node='panel')).result(self.ma).count(1,4)
    expect(self.mg.set_style(ANY, KWARGS, top = 40, height= 400, 
      position='absolute')).count(1,4)
    expect(self.mg.set_attrs(ANY, 
            ondragover = ANY, ondrop = ANY)).count(1,4)
  def _replay_and_create_main(self,p = '.&.'):
    "create main"
    self.mock_gui.replay()
    self.app = main(self.mg, self.mg, 'head labels panel', '/studio/memit/%s')
    print('---- NOW OPERATIONS ----')
  def test_create_kanban(self):
    "create kanban"
    self._expect_all_kanban()
    self._replay_and_create_main()
  def test_crete_task(self):
    "create task"
    self._expect_all_kanban()
    expect(self.mg.preventDefault())
    expect(self.mg.data[ANY]).result('#CCFF66')
    expect(self.ma.deploy(ARGS))
    expect(self.ma.get_color()).result('#CCFF66')
    expect(self.mg.div('', Class='task-note', draggable=True,
                       id='color_CCFF66', node='panel')).result(self.ma)
    expect(self.mg.set_style(ANY, backgroundColor='#CCFF66',
                height=64, left=82, position='absolute', top=42, width=316))
    expect(self.mg.set_attrs(ANY, ondragover=ANY, ondragstart=ANY, ondrop=ANY, onmouseover=ANY))
    self._replay_and_create_main()
    expect
    assert '#CCFF66' in self.app.head_bar.colors, self.app.head_bar.colors
    #tab = self.app.head_bar.colors[0]
    self.panel = self.app.task_bar.panels[0]._drop(self.mg)
    tasks = self.app.task_bar.panels[0].tasks
    assert tasks,tasks

if __name__ == '__main__':
    import unittest
    unittest.main()