#!/bin/env python
# coding=UTF-8

'''
    StructBaseClass
    ===============
        Struct base class definem (in Python 2).
'''

# Import Python Lib
from abc import ABCMeta, abstractmethod

################################################################################
# Struct Class Base (Python 2)
################################################################################

class __StructBase(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def Copy(self):

        raise NotImplementedError


    @abstractmethod
    def Dumps(self):

        raise NotImplementedError


    def __nonzero__(self):

        return True


    def Dump(self, dumpFileName, fileMode = 'w'):

        with open(dumpFileName, fileMode) as fo:
            fo.write(self.Dumps())