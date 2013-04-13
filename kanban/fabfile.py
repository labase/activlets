# -*- coding: utf-8 -*-
"""
############################################################
Kanban - Fabric deployment
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/04/13  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2013, `GPL <http://is.gd/3Udt>__. 
"""
#from BeautifulSoup import BeautifulSoup as soup
from fabric.api import local, settings, cd, run, lcd
from base64 import b64decode as b6d
import mechanize as mcz
from tempfile import mkdtemp
KG_ORIGIN = '.'
KG_DEST = '../../../deploy/kanban'
SOURCES = '*.py'
PARTS = '/src/main.html /src/*.py'.split()
DESTS = '/ /'.split()
PLAT = 'https://activufrj.nce.ufrj.br/'
#PLAT = 'http://localhost:8888/'
def __actdep(paswd):
    _k_copy()
def __actinit(mech,paswd):
    mech.open(PLAT)
    
    mech.select_form(nr=0)
    mech["user"] = "carlo"
    mech["passwd"] = b6d(paswd)
    results = mech.submit().read()
def __actup(mech, filename, folder = 'file/%sactivlets', orig = '/src/', single = None):
    avs = mech.open(PLAT+folder%'').read()
    if filename in avs:
        mech.open(PLAT+folder%'delete/'+ '/' + filename).read()
    print(PLAT+folder%'')
    avs = mech.open(PLAT+folder%'').read()
    mech.select_form(nr=0)
    mech.add_file(open(KG_ORIGIN + orig + (single or filename)), 'text/plain', filename)
    results = mech.submit().read()
def actdep(paswd):
    mech = mcz.Browser()
    paswd = paswd.replace('_','=')
    __actinit(mech,paswd)
    files = [f for f in local('ls src', capture=True).split()
             if f.split('.')[-1] in 'pyhtml']
    local('echo %s'%files)
    for filename in files:
        __actup(mech, filename)
def ktest():
    local("nosetests")

def _do_copy(source,targ):
    local ("mkdir -p %s"%targ)
    local("cp -u %s -t %s"%(source,targ))

def _k_copy():
    for part, dest in zip(PARTS, DESTS):
        targ, source = KG_DEST + dest, KG_ORIGIN +part
        _do_copy(source, targ)

def kgdep():
    ktest()
    _k_copy()
    #kzip()
