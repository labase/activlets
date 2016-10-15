# -*- coding: UTF8 -*-
from pybuilder.core import use_plugin, init, Author, task
import os
import sys

SRC = os.path.join(os.path.dirname(__file__), "src")
DOC = os.path.join(os.path.dirname(__file__), "docs")
sys.path.append(SRC)
from aktask import __version__

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.unittest")
# use_plugin("python.coverage")
use_plugin("python.distutils")
# use_plugin('pypi:pybuilder_header_plugin')
use_plugin("exec")

url = 'https://github.com/labase/superpython'
description = "Please visit {url}".format(url=url)
authors = [Author('Carlo Oliveira', 'carlo@ufrj.br')]
license = 'GNU General Public License v2 (GPLv2)'
summary = "GTK GUI to access github issues"
version = __version__
default_task = ['analyze', 'publish', 'buid_docs']  # , 'post_docs']


# default_task = ['analyze']  # , 'post_docs']


@init
def initialize(project):
    project.set_property('distutils_classifiers', [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Bottle',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: Portuguese (Brazilian)',
        'Topic :: Education',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'])
    header = open('header.py').read()
    project.set_property('dir_source_main_python', 'src')
    project.set_property('dir_source_unittest_python', 'src/test')
    project.set_property('unittest_module_glob', 'test_*')
    # project.set_property('pybuilder_header_plugin_expected_header', header)
    project.set_property('pybuilder_header_plugin_break_build', True)


@task
def post_docs(project, logger):
    from subprocess import call
    result = call(['curl', '-X', 'POST', 'http://readthedocs.org/build/activlets'])
    logger.info("Commit hook @ http://readthedocs.org/build/activlets: %d" % result)


@task
def buid_docs(project, logger):
    from subprocess import check_output
    result = check_output(['make', '-C', DOC, 'html'])
    logger.info(result)

