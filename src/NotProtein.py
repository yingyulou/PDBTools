#!/usr/bin/env python3
# coding=UTF-8

'''
    NotProtein
    ==========
        Class __NotProtein define.
'''

# Import PDBTools
from .StructBase import __StructBase

################################################################################
# Class __NotProtein
################################################################################

class __NotProtein(__StructBase):

    @property
    def idx(self):

        return self.owner.sub.index(self)


    @property
    def pre(self):

        subObjList = self.owner.sub
        selfIdx = subObjList.index(self)

        if selfIdx == 0:
            raise IndexError
        else:
            return subObjList[selfIdx - 1]


    @property
    def next(self):

        subObjList = self.owner.sub

        return subObjList[subObjList.index(self) + 1]


    def Remove(self):

        self.owner.sub.remove(self)
