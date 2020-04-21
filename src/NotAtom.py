#!/usr/bin/env python3
# coding=UTF-8

'''
    NotAtom
    =======
        Class __NotAtom define.
'''

# Import Python Lib
from abc import abstractmethod
from numpy import array

# Import PDBTools
from .StructBase import __StructBase
from .Constants import RESIDUE_NAME_THREE_TO_ONE_DICT

################################################################################
# Class __NotAtom
################################################################################

class __NotAtom(__StructBase):

    @abstractmethod
    def GetResidues(self):

        raise NotImplementedError


    @abstractmethod
    def IGetResidues(self):

        raise NotImplementedError


    @abstractmethod
    def GetAtoms(self):

        raise NotImplementedError


    @abstractmethod
    def IGetAtoms(self):

        raise NotImplementedError


    def FilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameSet = set((atomName,) + atomNameTuple)

        return [atomObj for atomObj in self.IGetAtoms() if atomObj.name in atomNameSet]


    def IFilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameSet = set((atomName,) + atomNameTuple)

        for atomObj in self.IGetAtoms():
            if atomObj.name in atomNameSet:
                yield atomObj


    def GetAtomsCoord(self):

        return array([atomObj.coord for atomObj in self.IGetAtoms()])


    def IGetAtomsCoord(self):

        for atomObj in self.IGetAtoms():
            yield atomObj.coord


    def FilterAtomsCoord(self, atomName = 'CA', *atomNameTuple):

        atomNameSet = set((atomName,) + atomNameTuple)

        return array([atomObj.coord for atomObj in self.IGetAtoms()
            if atomObj.name in atomNameSet])


    def IFilterAtomsCoord(self, atomName = 'CA', *atomNameTuple):

        atomNameSet = set((atomName,) + atomNameTuple)

        for atomObj in self.IGetAtoms():
            if atomObj.name in atomNameSet:
                yield atomObj.coord


    def Dumps(self):

        return ''.join([atomObj.Dumps() for atomObj in self.IGetAtoms()])


    def __iter__(self):

        return iter(self.sub)


    def __len__(self):

        return len(self.sub)


    def __getitem__(self, sliceObj):

        return self.sub[sliceObj]


    def __setitem__(self, sliceObj, setValue):

        self.sub[sliceObj] = setValue


    @property
    def center(self):

        return self.GetAtomsCoord().mean(0)


    def MoveCenter(self):

        centerCoord = self.center

        for atomObj in self.IGetAtoms():
            atomObj.coord -= centerCoord

        return self


    @property
    def seq(self):

        return ''.join([RESIDUE_NAME_THREE_TO_ONE_DICT[resObj.name]
            for resObj in self.IGetResidues()])


    @property
    def fasta(self):

        return '>%s\n%s\n' % (self.name, self.seq)


    def DumpFasta(self, dumpFilePath, fileMode = 'w'):

        with open(dumpFilePath, fileMode) as fo:
            fo.write(self.fasta)

        return self


    def RenumResidues(self, startNum = 1):

        for residueObj in self.IGetResidues():
            residueObj.compNum = (startNum, '')
            startNum += 1

        return self


    def RenumAtoms(self, startNum = 1):

        for atomObj in self.IGetAtoms():
            atomObj.num = startNum
            startNum += 1

        return self


    def Append(self, *subObjTuple):

        for appendObj in subObjTuple:
            copyAppendObj = appendObj.Copy()
            copyAppendObj.owner = self
            self.sub.append(copyAppendObj)

        return self


    def Insert(self, insertIdx, *subObjTuple):

        copyInsertObjList = []

        for insertObj in subObjTuple:
            copyInsertObj = insertObj.Copy()
            copyInsertObj.owner = self
            copyInsertObjList.append(copyInsertObj)

        self.sub = self.sub[:insertIdx] + copyInsertObjList + self.sub[insertIdx:]

        return self


    def RemoveAlt(self):

        for atomObj in self.GetAtoms():
            if atomObj.alt == 'A':
                atomObj.alt = ''
            elif atomObj.alt:
                atomObj.Remove()

        return self