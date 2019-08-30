#!/bin/env python
# coding=UTF-8

'''
    NotProteinStructInterface
    =========================
        Class __NotProteinStructInterface define.
'''

# Import PDBTools
from .StructBaseInterface import __StructBaseInterface

################################################################################
# Not Protein Struct Interface
################################################################################

class __NotProteinStructInterface(__StructBaseInterface):

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