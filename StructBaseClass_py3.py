#!/bin/env python
# coding=UTF-8

'''
    StructBaseClass
    ===============
        Struct base class definem (in Python 3).
'''

# Import Python Lib
from abc import ABC, abstractmethod

################################################################################
# Struct Class Base (Python 3)
################################################################################

class __StructBase(ABC):

    @abstractmethod
    def Copy(self):

        raise NotImplementedError


    @abstractmethod
    def Dumps(self):

        raise NotImplementedError


    def __bool__(self):

        return True


    def Dump(self, dumpFileName, fileMode = 'w'):

        with open(dumpFileName, fileMode) as fo:
            fo.write(self.Dumps())