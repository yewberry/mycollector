#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    try:
        from src.my_app import MyApp
        app = MyApp(redirect=True)
        app.MainLoop()
    except Exception as e:
        print e

if __name__ == '__main__':
    main()
