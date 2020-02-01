#!/usr/bin/env python
"""pyazo manage.py"""
import os
import sys

import pymysql

pymysql.install_as_MySQLdb()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyazo.root.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
