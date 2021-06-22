#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： XHao
# datetime： 2021/6/4 2:43 
# ide： PyCharm

from PyQt5.QtCore import pyqtSignal,QThread
import numpy as np
class Thread(QThread):
    signal = pyqtSignal(np.ndarray)
    def __init__(self,func):
        super(Thread, self).__init__()
        self.func = func

    def run(self):
        self.func()