#! /home/marcram/Documents/Python/virt
# encoding:utf-8

from flask import Flask

from appli import app
import config

print('hello')

if __name__ == '__main__':
    app.run('0.0.0.0', 7000, debug=True)
    