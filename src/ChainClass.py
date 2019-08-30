#!/bin/env python
# coding=UTF-8

'''
    ChainClass
    ==========
        Class Chain define.
'''

# Import PDBTools
from .NotAtomStructInterface import __NotAtomStructInterface
from .NotProteinStructInterface import __NotProteinStructInterface

################################################################################
# Chain Struct Class
################################################################################

class Chain(__NotAtomStructInterface, __NotProteinStructInterface):

    __slots__ = ('name', 'owner', 'sub')

    def __init__(self, chainName = '', owner = None):

        self.name  = chainName
        self.owner = owner
        self.sub   = []

        if owner != None:
            owner.sub.append(self)


    def __repr__(self):

        return '<Chain object: %s, at 0x%X>' % (self.name, id(self))


    __str__ = __repr__


    def Copy(self):

        copyChainObj = Chain(self.name)

        for resObj in self:
            copyResObj = resObj.Copy()
            copyResObj.owner = copyChainObj
            copyChainObj.sub.append(copyResObj)

        return copyChainObj


    def GetResidues(self):

        return list(self.sub)


    def GetAtoms(self):

        return [atomObj for resObj in self for atomObj in resObj]


    def IGetResidues(self):

        for resObj in self:
            yield resObj


    def IGetAtoms(self):

        for resObj in self:
            for atomObj in resObj:
                yield atomObj