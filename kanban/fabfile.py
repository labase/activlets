# -*- coding: utf-8 -*-
"""
############################################################
Kuarup - Fabric deployment
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/03/03  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2013, `GPL <http://is.gd/3Udt>__. 
"""
__author__  = "Carlo E. T. Oliveira (cetoli@yahoo.com.br) $Author: cetoli $"
__version__ = "1.1 $Revision$"[10:-1]
__date__    = "2013/03/03 $Date$"
from BeautifulSoup import BeautifulSoup as soup
from fabric.api import local, settings, cd, run, lcd
from base64 import b64decode as b6d
import mechanize as mcz
from tempfile import mkdtemp
KG_ORIGIN = '/home/carlo/Dropbox/Android/git/activlets/kanban'
KG_DEST = '/home/carlo/Dropbox/Public/labase/kwarwp'
SOURCES = '*.py'
KSOURCES = 'kuarup.py tchuk.py kuarupfest.py tkinter_factory.py'
KG_IMAGES = KG_ORIGIN + '/src/public/image'
PARTS = '/src/*.py'.split()
DESTS = '/src'.split()
PLAT = 'https://activufrj.nce.ufrj.br/'
WEBPATH = 'file/%sactivlets'
WEBFILES = 'kanban.py'.split()
#WEBFILES = 'main.html kanban.py'.split()
#PLAT = 'http://localhost:8888/'

def __actinit(mech, paswd):
    mech.open(PLAT)
    
    mech.select_form(nr=0)
    mech["user"] = "carlo"
    mech["passwd"] = b6d(paswd)
    results = mech.submit().read()
    soup(results)
    print (PLAT+WEBPATH%'')
def __actup(mech, filename, folder = WEBPATH, orig = '/src/', single = ''):
    avs = mech.open(PLAT+folder%'').read()
    #filename = 'cavalier.py'
    if filename in avs:
        mech.open(PLAT+folder%'delete/'+ '/' + filename).read()
    avs = mech.open(PLAT+folder%'').read()
    mech.select_form(nr=0)
    mech.add_file(open(KG_ORIGIN + orig + (single or filename)), 'text/plain', filename)
    results = mech.submit().read()
def __actdep(paswd):
    mech = mcz.Browser()
    __actinit(mech, paswd)
    for filename in WEBFILES:
        __actup(mech, filename)
def actdep(paswd="bGFiYXNlNGN0MXY="):
    ktest()
    kdoc()
    __actdep(paswd)
def ktest():
    local("nosetests")
def kdoc():
    local("cd docs;make html; cd -")

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
