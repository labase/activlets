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
:Revision: 0.1.5
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__. 
"""
__author__  = "Carlo E. T. Oliveira (carlo@nce.ufrj.br)"
__version__ = "0.1"
__date__    = "2013/03/29"

        
import mocker
from mocker import Mocker,KWARGS, ARGS, ANY, CONTAINS, MATCH, expect
from kanban import main
import kanban

TABCOLOR = '#F9D1D1'
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
    kanban.OBID = 0
    pass

  def _expect_all_kanban(self):
    "main class expectations"
    # create colors
    expect(self.mg.div('', KWARGS, Class='color-tabs', draggable=True,
                       node='head')).result(self.ma).count(1,24)
    expect(self.mg.set_style(ANY, KWARGS, height= 16, width= 36,
      position='absolute')).count(1,24)
    expect(self.mg.set_attrs(ANY)).count(1,6)
    expect(self.mg.set_attrs(ANY, KWARGS)).count(1,24)
    # create panels
    expect(self.mg.div('', KWARGS, Class='task-panel', 
                       node='panel')).result(self.ma).count(1,4)
    expect(self.mg.div('', KWARGS, Class='board-panel', 
                       node='panel')).result(self.ma).count(1,2)
    expect(self.mg.set_style(ANY, KWARGS, top = 40, height= 420, 
      position='absolute')).count(1,5)
    expect(self.mg.set_attrs(ANY, 
            ondragover = ANY, ondrop = ANY)).count(1,5)
  def _replay_and_create_main(self,p = '.&.'):
    "create main"
    self.mock_gui.replay()
    self.app = main(self.mg, self.mg, 'head labels panel', '/studio/memit/%s')
    print('---- NOW OPERATIONS ----')
  def test_create_kanban(self):
    "create kanban"
    self._expect_all_kanban()
    self._replay_and_create_main()
  def _expect_task_creation(self, id='task_0', left =82, top=42, width=316):
    expect(self.mg.preventDefault())
    expect(self.mg.data[ANY]).result(TABCOLOR)
    expect(self.ma.deploy(ARGS))
    expect(self.ma.get_color()).result(TABCOLOR)
    expect(self.mg.div('', Class='task-div', draggable=True,
                       id=id, node=ANY)).result(self.ma)
    expect(self.mg.set_style(ANY, KWARGS,backgroundColor=TABCOLOR,
                height=64, left=ANY, position='absolute', top=ANY, width=width))
    expect(self.mg.set_attrs(ANY, ondragover=ANY, ondragstart=ANY, ondrop=ANY
                             , onmouseover=ANY, onclick = ANY))
    #: timer creation
    expect(self.mg.div('', KWARGS,Class='task-timer', draggable=False,
                        node=ANY)).result(self.ma)
    expect(self.mg.set_style(ANY, KWARGS,backgroundColor='black',
                height=16, left=ANY, position='absolute', top=ANY, width=64))
    
    expect(self.mg.set_attrs(ANY, ondragover=ANY, ondragstart=ANY, ondrop=ANY
                             , onmouseover=ANY, onclick = ANY))
    #: timernote creation
    expect(self.mg.div('', KWARGS,Class='task-note', draggable=True,
                        node=ANY)).result(self.ma)
    expect(self.mg.set_style(ANY, KWARGS,backgroundColor=TABCOLOR,
                height=46, left=ANY, position='absolute', top=ANY, width='96%'))
    
    expect(self.mg.set_attrs(ANY, ondragover=ANY, ondragstart=ANY, ondrop=ANY
                             , onmouseover=ANY, onclick = ANY))
   #expect(self.mg.cling(ARGS))
  def test_create_task(self):
    "create task"
    self._expect_all_kanban()
    self._expect_task_creation()
    self._replay_and_create_main()
    assert TABCOLOR in self.app.head_bar.colors, self.app.head_bar.colors
    #tab = self.app.head_bar.colors[0]
    self.app.task_bar.panels[0]._drop(self.mg)
    tasks = self.app.task_bar.panels[0].items
    assert tasks,tasks
  def test_create_task_and_delete(self):
    "create task and delete"
    self._expect_all_kanban()
    self._expect_task_creation()
    expect(self.mg.preventDefault())
    expect(self.mg.data[ANY]).result('task_0')
    expect(self.mg.confirmation(ANY)).result(True)
    expect(self.mg.remove(ANY, 'panel'))
    self._replay_and_create_main()
    assert TABCOLOR in self.app.head_bar.colors, self.app.head_bar.colors
    #tab = self.app.head_bar.colors[0]
    self.app.task_bar.panels[0]._drop(self.mg)
    self.app.head_bar.colors[TABCOLOR]._drop(self.mg)
    tasks = self.app.task_bar.panels[0].items
    assert not tasks,tasks
  def _expect_task_move(self, task = 'task_0',left =402, top=42, width=256):
    "move atask"
    expect(self.mg.preventDefault())
    expect(self.mg.data[ANY]).result(task)
    #expect(self.mg.set_style(ANY, backgroundColor=TABCOLOR, height=64
    #  , left=left, position='absolute', top=top, width=width))
    expect(self.mg.set_style(ANY, KWARGS,backgroundColor=TABCOLOR, height=ANY
      , left=ANY, position='absolute', top=ANY, width=ANY))
    expect(self.mg.set_style(ANY, KWARGS,backgroundColor=TABCOLOR, height=ANY
      , left=ANY, position='absolute', top=ANY, width=ANY))
    expect(self.mg.cling(ARGS))
    expect(self.mg.remove(ARGS))
  def test_create_task_and_move(self):
    "create task and move"
    self._expect_all_kanban()
    self._expect_task_creation()
    self._expect_task_move()#(task = 'task_',left =402, top=42, width=256)
    self._replay_and_create_main()
    assert TABCOLOR in self.app.head_bar.colors, self.app.head_bar.colors
    #tab = self.app.head_bar.colors[0]
    self.app.task_bar.panels[0]._drop(self.mg)
    assert 'task_0' in self.app.items, self.app.items
    self.app.task_bar.panels[1]._drop(self.mg)
    tasks = self.app.task_bar.panels[0].items
    assert not tasks,tasks
    assert  self.app.get_item('task_0'),self.app.items
  def test_create_two_task_and_move(self):
    "create two tasks and move one"
    self._expect_all_kanban()
    self._expect_task_creation()
    self._expect_task_creation(id= 'task_1', left =402, top=42, width=256)
    self._expect_task_move(top=110)#(task = 'task_',left =402, top=42, width=256)
    self._replay_and_create_main()
    assert TABCOLOR in self.app.head_bar.colors, self.app.head_bar.colors
    #tab = self.app.head_bar.colors[0]
    self.app.task_bar.panels[0]._drop(self.mg)
    assert 'task_0' in self.app.items, self.app.items
    self.app.task_bar.panels[1]._drop(self.mg)
    assert 'task_1' in self.app.items, self.app.items
    self.app.task_bar.panels[1]._drop(self.mg)
    assert 'task_1' in self.app.items, self.app.items
    tasks = self.app.task_bar.panels[0].items
    tasks1 = self.app.task_bar.panels[1].items
    task0, task1 =self.app.get_item('task_0'),self.app.get_item('task_1')
    assert not tasks,tasks
    assert len(tasks1)==2,tasks1
    assert (task0.top, task1.top) ==(1,0),(task0.top, task1.top)
if __name__ == '__main__':
    import unittest
    unittest.main()