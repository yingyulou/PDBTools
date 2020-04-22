#!/usr/bin/env python3
# coding=UTF-8

'''
    StructBase
    ==========
        Class __StructBase define.
'''

# Import Python Lib
import sys

################################################################################
# Class __StructBase
################################################################################

if sys.version_info[0] == 3:

    from abc import ABC, abstractmethod

    class __StructBase(ABC):

        @abstractmethod
        def Copy(self):

            raise NotImplementedError


        @abstractmethod
        def Dumps(self):

            raise NotImplementedError


        def Dump(self, dumpFilePath, fileMode = 'w'):

            with open(dumpFilePath, fileMode) as fo:
                fo.write(self.Dumps())

            return self

else:

    from abc import ABCMeta, abstractmethod

    class __StructBase(object):

        __metaclass__ = ABCMeta

        @abstractmethod
        def Copy(self):

            raise NotImplementedError


        @abstractmethod
        def Dumps(self):

            raise NotImplementedError


        def Dump(self, dumpFilePath, fileMode = 'w'):

            with open(dumpFilePath, fileMode) as fo:
                fo.write(self.Dumps())

            return self
