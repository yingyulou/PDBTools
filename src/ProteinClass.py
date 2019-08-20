#!/bin/env python
# coding=UTF-8

'''
    ProteinClass
    ============
        Class Protein define.
'''

# Import PDBTools
from NotAtomStructInterface import __NotAtomStructInterface

################################################################################
# Protein Struct Class
################################################################################

class Protein(__NotAtomStructInterface):

    __slots__ = ('name', 'sub')

    def __init__(self, proteinID = ''):

        self.name = proteinID
        self.sub  = []


    def __repr__(self):

        return '<Protein object: %s, at 0x%X>' % (self.name, id(self))


    __str__ = __repr__


    @property
    def subDict(self):

        return {chainObj.name: chainObj for chainObj in self}


    def Copy(self):

        copyProObj = Protein(self.name)

        for chainObj in self:
            copyChainObj = chainObj.Copy()
            copyChainObj.owner = copyProObj
            copyProObj.sub.append(copyChainObj)

        return copyProObj


    def GetResidues(self):

        return [resObj for chainObj in self for resObj in chainObj]


    def GetAtoms(self):

        return [atomObj for chainObj in self for resObj in chainObj
            for atomObj in resObj]


    def IGetResidues(self):

        for chainObj in self:
            for resObj in chainObj:
                yield resObj


    def IGetAtoms(self):

        for chainObj in self:
            for resObj in chainObj:
                for atomObj in resObj:
                    yield atomObj