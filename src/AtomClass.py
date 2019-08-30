#!/bin/env python
# coding=UTF-8

'''
    AtomClass
    =========
        Class Atom define.
'''

# Import Python Lib
from numpy import array

# Import PDBTools
from .NotProteinStructInterface import __NotProteinStructInterface

################################################################################
# Class Atom
################################################################################

class Atom(__NotProteinStructInterface):

    __slots__ = ('name', 'num', 'coord', 'alt', 'occ', 'tempF', 'ele', 'chg', 'owner')

    def __init__(self, atomName = '', atomNum = 0, atomCoord = array((0., 0., 0.)),
        atomAltLoc = '', atomOccupancy = '', atomTempFactor = '', atomElement = '',
        atomCharge = '', owner = None):

        self.name  = atomName
        self.num   = atomNum
        self.coord = atomCoord
        self.alt   = atomAltLoc
        self.occ   = atomOccupancy
        self.tempF = atomTempFactor
        self.ele   = atomElement
        self.chg   = atomCharge
        self.owner = owner

        if owner != None:
            owner.sub.append(self)


    def __repr__(self):

        return '<Atom object: %d %s %s, at 0x%X>' % (
            self.num, self.name, str(self.coord), id(self))


    __str__ = __repr__


    def __sub__(self, subAtomObj):

        return Dis(self.coord, subAtomObj.coord)


    def Copy(self):

        return Atom(self.name, self.num, self.coord.copy(), self.alt, self.occ,
            self.tempF, self.ele, self.chg)


    def Dumps(self):

        ownerResObj = self.owner

        if ownerResObj != None:

            resName = ownerResObj.name
            resNum  = ownerResObj.num
            resIns  = ownerResObj.ins

            ownerChainObj = ownerResObj.owner
            chainName = ownerChainObj.name if ownerChainObj != None else ''

        else:
            resName, resNum, resIns, chainName = '', 0, '', ''

        if self.name[0].isdigit() or len(self.name) == 4:
            atomName = '%-4s' % self.name
        else:
            atomName = ' %-3s' % self.name

        return 'ATOM  %5d %s%1s%3s %1s%4d%1s   %8.3f%8.3f%8.3f%6s%6s          %2s%2s\n' % (
            self.num, atomName, self.alt, resName, chainName, resNum, resIns,
            self.coord[0], self.coord[1], self.coord[2], self.occ, self.tempF,
            self.ele, self.chg)