#!/usr/bin/env python3
# coding=UTF-8

'''
    Protein
    =======
        Class Protein define.
'''

# Import PDBTools
from .NotAtom import __NotAtom

################################################################################
# Class Protein
################################################################################

class Protein(__NotAtom):

    __slots__ = ('name', 'model', 'sub')

    def __init__(self, proteinID = '', modelNum = 0):

        self.name  = proteinID
        self.model = modelNum
        self.sub   = []


    def __repr__(self):

        return '<Protein object: %s (Model: %d), at 0x%X>' % (
            self.name, self.model, id(self))


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
