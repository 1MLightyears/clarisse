"""
Clarisse

A light-weighted GUI framework for Python programs.

by 1MLightyears@gmail.com

on 20201208
"""
from __future__ import absolute_import

import os
import sys
from functools import wraps

from GUI import ClrsGUI

#from .analyze import AnalyzeFunc # TODO: uncomment the import before release


__all__ = ["Clarisse", "version"]

version="v0.0.3"

def Clarisse(*args, **kwargs):
    def middle(func):
        if isinstance(func,type(lambda :0)):
            @wraps(func)
            def gui_func(*default_args, **default_kwargs):
                nonlocal func,args,kwargs
                w=ClrsGUI()
                w.Parse(func,default_args,default_kwargs,*args,**kwargs)
                w.main_window.show()
                w.app.exec_()
                return w.pages[0].run_thread.ret
            return gui_func
    return middle

###
@Clarisse()
def f(arg1: int, arg2: float, arg3: str):
    """
    dummy\\
    docstring.
    """
    import time
    for i in range(arg1):
        print(i, 2 * i, sep=arg3)
        assert i<10, "an error!"
        time.sleep(arg2)
    return 0

print(f(arg1=5,arg2=0.8))
