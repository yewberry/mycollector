#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import multiprocessing

def main():
    try:
        from src.my_app import MyApp
        app = MyApp(redirect=True)
        app.MainLoop()
    except Exception as e:
        print e
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
