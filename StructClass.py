#!/bin/env python
# coding=UTF-8

'''
    StructClass
    ===========
        Four struct class (Protein, Chain, Residue, Atom) define.
'''

# Import Python Lib
import six
from abc import abstractmethod
from numpy import array

# Import PDBTools
if six.PY2:
    from .StructBaseClass_py2 import __StructBase
else:
    from .StructBaseClass_py3 import __StructBase

from .MathUtil import Dis, CalcRotationMatrix, CalcDihedralAngle
from .StructConst import RESIDUE_NAME_THREE_TO_ONE_DICT, _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT

################################################################################
# Not Atom Struct Class Base
################################################################################

class __NotAtomStructBase(__StructBase):

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


    @property
    def seq(self):

        return ''.join([RESIDUE_NAME_THREE_TO_ONE_DICT[resObj.name] for resObj in self.IGetResidues()])


    @property
    def fasta(self):

        return '>%s\n%s\n' % (self.name, self.seq)


    def Dumps(self):

        return ''.join([atomObj.Dumps() for atomObj in self.IGetAtoms()])


    def DumpFasta(self, dumpFileName, fileMode = 'w'):

        with open(dumpFileName, fileMode) as fo:
            fo.write(self.fasta)


    def MoveCenter(self):

        centerCoord = self.center

        for atomObj in self.IGetAtoms():
            atomObj.coord -= centerCoord


    def RenumResidues(self, startNum = 1):

        for residueObj in self.IGetResidues():
            residueObj.compNum = (startNum, '')
            startNum += 1


    def RenumAtoms(self, startNum = 1):

        for atomObj in self.IGetAtoms():
            atomObj.num = startNum
            startNum += 1


    def Append(self, *appendObjTuple):

        for appendObj in appendObjTuple:
            copyAppendObj = appendObj.Copy()
            copyAppendObj.owner = self
            self.sub.append(copyAppendObj)


    def Insert(self, idxNum, *insertObjTuple):

        copyInsertObjList = []

        for insertObj in insertObjTuple:
            copyInsertObj = insertObj.Copy()
            copyInsertObj.owner = self
            copyInsertObjList.append(copyInsertObj)

        self.sub = self.sub[:idxNum] + copyInsertObjList + self.sub[idxNum:]


    def FilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set((atomName,) + atomNameTuple)

        return [atomObj for atomObj in self.IGetAtoms() if atomObj.name in atomNameList]


    def IFilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set((atomName,) + atomNameTuple)

        for atomObj in self.IGetAtoms():
            if atomObj.name in atomNameList:
                yield atomObj


    def GetAtomsCoord(self):

        return array([atomObj.coord for atomObj in self.IGetAtoms()])


    def FilterAtomsCoord(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set((atomName,) + atomNameTuple)

        return array([atomObj.coord for atomObj in self.IGetAtoms()
            if atomObj.name in atomNameList])


################################################################################
# Not Protein Struct Class Base
################################################################################

class __NotProteinStructBase(__StructBase):

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


################################################################################
# Protein Struct Class
################################################################################

class Protein(__NotAtomStructBase):

    __slots__ = ('name', 'sub')

    def __init__(self, proteinID = ''):

        self.name = proteinID
        self.sub  = []


    def __repr__(self):

        return '<Protein object: %s, at 0x%X>' % (self.name, id(self))

    __str__ = __repr__


    @property
    def subDict(self):

        return {chainObj.name: chainObj for chainObj in self.sub}


    def Copy(self):

        copyProObj = Protein(self.name)

        for chainObj in self.sub:
            copyChainObj = chainObj.Copy()
            copyChainObj.owner = copyProObj
            copyProObj.sub.append(copyChainObj)

        return copyProObj


    def GetResidues(self):

        return [resObj for chainObj in self.sub for resObj in chainObj.sub]


    def GetAtoms(self):

        return [atomObj for chainObj in self.sub for resObj in chainObj.sub
            for atomObj in resObj.sub]


    def IGetResidues(self):

        for chainObj in self.sub:
            for resObj in chainObj.sub:
                yield resObj


    def IGetAtoms(self):

        for chainObj in self.sub:
            for resObj in chainObj.sub:
                for atomObj in resObj.sub:
                    yield atomObj


################################################################################
# Chain Struct Class
################################################################################

class Chain(__NotAtomStructBase, __NotProteinStructBase):

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

        for resObj in self.sub:
            copyResObj = resObj.Copy()
            copyResObj.owner = copyChainObj
            copyChainObj.sub.append(copyResObj)

        return copyChainObj


    def GetResidues(self):

        return list(self.sub)


    def GetAtoms(self):

        return [atomObj for resObj in self.sub for atomObj in resObj.sub]


    def IGetResidues(self):

        for resObj in self.sub:
            yield resObj


    def IGetAtoms(self):

        for resObj in self.sub:
            for atomObj in resObj.sub:
                yield atomObj


################################################################################
# Residue Struct Class
################################################################################

class Residue(__NotAtomStructBase, __NotProteinStructBase):

    __slots__ = ('name', 'num', 'ins', 'owner', 'sub')

    def __init__(self, resName = '', resNum = 0, resIns = '', owner = None):

        self.name  = resName
        self.num   = resNum
        self.ins   = resIns
        self.owner = owner
        self.sub   = []

        if owner != None:
            owner.sub.append(self)


    def __repr__(self):

        return '<Residue object: %d%s %s, at 0x%X>' % (self.num, self.ins, self.name, id(self))

    __str__ = __repr__


    @property
    def compNum(self):

        return str(self.num) + self.ins


    @compNum.setter
    def compNum(self, completeNumList):

        self.num, self.ins = completeNumList


    @property
    def subDict(self):

        return {atomObj.name: atomObj for atomObj in self.sub}


    @property
    def coordDict(self):

        return {atomObj.name: atomObj.coord for atomObj in self.sub}


    def Copy(self):

        copyResObj = Residue(self.name, self.num, self.ins)

        for atomObj in self.sub:
            copyAtomObj = atomObj.Copy()
            copyAtomObj.owner = copyResObj
            copyResObj.sub.append(copyAtomObj)

        return copyResObj


    def GetResidues(self):

        return [self]


    def GetAtoms(self):

        return list(self.sub)


    def IGetResidues(self):

        yield self


    def IGetAtoms(self):

        for atomObj in self.sub:
            yield atomObj


    def CalcBBDihedralAngle(self, dihedralSideStr):

        ownerChainObj = self.owner
        indexInOwner = ownerChainObj.sub.index(self)
        atomObjDict = {atomObj.name: atomObj for atomObj in self}

        if dihedralSideStr.lower() in {'l', 'phi'}:

            if indexInOwner == 0:
                raise IndexError

            for atomObj in ownerChainObj[indexInOwner - 1]:
                if atomObj.name == 'C':
                    leftCCoord = atomObj.coord
                    break

            bbDihedralAngle = CalcDihedralAngle(leftCCoord, atomObjDict['N'].coord,
                atomObjDict['CA'].coord, atomObjDict['C'].coord)

        else:

            for atomObj in ownerChainObj[indexInOwner + 1]:
                if atomObj.name == 'N':
                    rightNCoord = atomObj.coord
                    break

            bbDihedralAngle = CalcDihedralAngle(atomObjDict['N'].coord,
                atomObjDict['CA'].coord, atomObjDict['C'].coord, rightNCoord)

        return bbDihedralAngle


    def CalcBBRotationMatrixByDeltaAngle(self, dihedralSideStr, modifySideStr, deltaAngle):

        atomObjDict = {atomObj.name: atomObj for atomObj in self}

        if dihedralSideStr.lower() in {'l', 'phi'}:
            moveCoord    = atomObjDict['N'].coord
            rotationAxis = atomObjDict['CA'].coord - moveCoord
        else:
            moveCoord    = atomObjDict['CA'].coord
            rotationAxis = atomObjDict['C'].coord - moveCoord

        if modifySideStr.lower() in {'l', 'n'}:
            deltaAngle = -deltaAngle

        rotationMatrix = CalcRotationMatrix(rotationAxis, deltaAngle)

        return moveCoord, rotationMatrix


    def CalcBBRotationMatrixByTargetAngle(self, dihedralSideStr, modifySideStr, targetAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralSideStr, modifySideStr,
            targetAngle - self.CalcBBDihedralAngle(dihedralSideStr))

        return moveCoord, rotationMatrix


    def GetBBRotationAtomObj(self, dihedralSideStr, modifySideStr):

        rotationAtomObjList = []
        ownerChainObj = self.owner
        indexInOwner = ownerChainObj.sub.index(self)

        if modifySideStr.lower() in {'l', 'n'}:

            for resObj in ownerChainObj.sub[0:indexInOwner]:
                rotationAtomObjList.extend(resObj.sub)

            if dihedralSideStr.lower() not in {'l', 'phi'}:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name not in {'CA', 'C', 'O', 'OXT'}])

        else:

            if dihedralSideStr.lower() in {'l', 'phi'}:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name not in {'N', 'CA'}])
            else:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name in {'O', 'OXT'}])

            for resObj in ownerChainObj.sub[indexInOwner + 1:]:
                rotationAtomObjList.extend(resObj.sub)

        return rotationAtomObjList


    def RotateBBDihedralAngleByDeltaAngle(self, dihedralSideStr, modifySideStr, deltaAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralSideStr, modifySideStr, deltaAngle)

        rotationAtomObjList = self.GetBBRotationAtomObj(dihedralSideStr, modifySideStr)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


    def RotateBBDihedralAngleByTargetAngle(self, dihedralSideStr, modifySideStr, targetAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByTargetAngle(
            dihedralSideStr, modifySideStr, targetAngle)

        rotationAtomObjList = self.GetBBRotationAtomObj(dihedralSideStr, modifySideStr)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


    def CalcSCDihedralAngle(self, dihedralIdx):

        atomObjDict = {atomObj.name: atomObj for atomObj in self.sub}
        atomNameA, atomNameB, atomNameC, atomNameD = \
            _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][:4]

        scDihedralAngle = CalcDihedralAngle(
            atomObjDict[atomNameA].coord, atomObjDict[atomNameB].coord,
            atomObjDict[atomNameC].coord, atomObjDict[atomNameD].coord,
        )

        return scDihedralAngle


    def CalcSCRotationMatrixByDeltaAngle(self, dihedralIdx, deltaAngle):

        atomObjDict = {atomObj.name: atomObj for atomObj in self.sub}
        atomNameA, atomNameB = \
            _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][1:3]

        moveCoord = atomObjDict[atomNameA].coord
        rotationAxis = atomObjDict[atomNameB].coord - atomObjDict[atomNameA].coord

        rotationMatrix = CalcRotationMatrix(rotationAxis, deltaAngle)

        return moveCoord, rotationMatrix


    def CalcSCRotationMatrixByTargetAngle(self, dihedralIdx, targetAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByDeltaAngle(
            dihedralIdx, targetAngle - self.CalcSCDihedralAngle(dihedralIdx))

        return moveCoord, rotationMatrix


    def GetSCRotationAtomObj(self, dihedralIdx):

        rotationAtomNameSet = set(_RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][3:])
        rotationAtomObjList = [atomObj for atomObj in self.sub if atomObj.name in rotationAtomNameSet]

        return rotationAtomObjList


    def RotateSCDihedralAngleByDeltaAngle(self, dihedralIdx, deltaAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByDeltaAngle(dihedralIdx, deltaAngle)
        rotationAtomObjList = self.GetSCRotationAtomObj(dihedralIdx)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


    def RotateSCDihedralAngleByTargetAngle(self, dihedralIdx, targetAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByTargetAngle(dihedralIdx, targetAngle)
        rotationAtomObjList = self.GetSCRotationAtomObj(dihedralIdx)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


################################################################################
# Atom Struct Class
################################################################################

class Atom(__NotProteinStructBase):

    __slots__ = ('name', 'num', 'coord', 'alt', 'occ', 'tempF', 'ele', 'chg', 'owner')

    def __init__(self, atomName = '', atomNum = 0, atomCoord = array([0., 0., 0.]),
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