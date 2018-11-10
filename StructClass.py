#!/bin/env python
# coding=UTF-8

'''
    StructClass
    ===========
        Four struct class (Protein, Chain, Residue, Atom) define in Python 3.
'''

# Import Python Lib
from abc import ABC, abstractmethod
from numpy import array
import logging

# Import PDBTools
from .MathUtil import Dis, CalcRotationMatrix, CalcDihedralAngle
from .StructConst import RES_NAME_THREE_TO_ONE_DICT

################################################################################
# Struct Class Base
################################################################################

class __C_StructBase(ABC):

    @abstractmethod
    def Copy(self):

        raise NotImplementedError


    def __bool__(self):

        return True


    def Dump(self, dumpFileName, fileMode = 'w'):

        with open(dumpFileName, fileMode) as fo:
            fo.write(self.Dumps())


################################################################################
# Not Atom Struct Class Base
################################################################################

class __C_NotAtomStructBase(__C_StructBase):

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

        return array([atomObj.coord for atomObj in self.IGetAtoms()]).mean(0)


    @property
    def seq(self):

        return ''.join([RES_NAME_THREE_TO_ONE_DICT[resObj.name] for resObj in self.IGetResidues()])


    def Append(self, *addObjTuple):

        for addObj in addObjTuple:
            copyAddObj = addObj.Copy()
            copyAddObj.owner = self
            self.sub.append(copyAddObj)


    def Insert(self, idxNum, *insertObjTuple):

        copyInsertObjList = []

        for insertObj in insertObjTuple:
            copyInsertObj = insertObj.Copy()
            copyInsertObj.owner = self
            copyInsertObjList.append(copyInsertObj)

        self.sub = self.sub[:idxNum] + copyInsertObjList + self.sub[idxNum:]


    def FilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set([atomName] + list(atomNameTuple))

        return [atomObj for atomObj in self.IGetAtoms() if atomObj.name in atomNameList]


    def IFilterAtoms(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set([atomName] + list(atomNameTuple))

        for atomObj in self.IGetAtoms():
            if atomObj.name in atomNameList:
                yield atomObj


    def GetAtomsCoord(self):

        return array([atomObj.coord for atomObj in self.IGetAtoms()])


    def FilterAtomsCoord(self, atomName = 'CA', *atomNameTuple):

        atomNameList = set([atomName] + list(atomNameTuple))

        return array([atomObj.coord for atomObj in self.IGetAtoms()
            if atomObj.name in atomNameList])


    def Dumps(self):

        return ''.join([subStructObj.Dumps() for subStructObj in self.sub])


    def MoveCenter(self):

        centerCoord = array([atomObj.coord for atomObj in self.IGetAtoms()]).mean(0)

        for atomObj in self.IGetAtoms():
            atomObj.coord -= centerCoord

        return self


################################################################################
# Not Protein Struct Class Base
################################################################################

class __C_NotProteinStructBase(__C_StructBase):

    @property
    def idx(self):

        return self.owner.sub.index(self)


    def Remove(self):

        self.owner.sub.remove(self)


################################################################################
# Protein Struct Class
################################################################################

class C_ProteinStruct(__C_NotAtomStructBase):

    __slots__ = ('name', 'sub')

    def __init__(self, proteinID = ''):

        self.name = proteinID
        self.sub = []


    def __repr__(self):

        return '<Protein object: %s, at 0x%X>' % (self.name, id(self))

    __str__ = __repr__


    def Copy(self):

        copyProteinObj = C_ProteinStruct(self.name)

        for chainObj in self.sub:
            copyChainObj = chainObj.Copy()
            copyChainObj.owner = copyProteinObj
            copyProteinObj.sub.append(copyChainObj)

        return copyProteinObj


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

class C_ChainStruct(__C_NotAtomStructBase, __C_NotProteinStructBase):

    __slots__ = ('name', 'owner', 'sub')

    def __init__(self, chainName = '', owner = None):

        self.name = chainName
        self.owner = owner
        self.sub = []

        if owner:
            owner.sub.append(self)


    def __repr__(self):

        return '<Chain object: %s, at 0x%X>' % (self.name, id(self))

    __str__ = __repr__


    def Copy(self):

        copyChainObj = C_ChainStruct(self.name)

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

class C_ResidueStruct(__C_NotAtomStructBase, __C_NotProteinStructBase):

    __slots__ = ('name', 'num', 'ins', 'owner', 'sub')

    def __init__(self, residueName = '', residueNum = 0, residueInsertChar = '', owner = None):

        self.name = residueName
        self.num = residueNum
        self.ins = residueInsertChar
        self.owner = owner
        self.sub = []

        if owner:
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
    def seq(self):

        return RES_NAME_THREE_TO_ONE_DICT[self.name]


    def Copy(self):

        copyResObj = C_ResidueStruct(self.name, self.num, self.ins)

        for atomObj in self.sub:
            copyAtomObj = atomObj.Copy()
            copyAtomObj.owner = copyResObj
            copyResObj.sub.append(copyAtomObj)

        return copyResObj


    def GetAtoms(self):

        return list(self.sub)


    def IGetAtoms(self):

        for atomObj in self.sub:
            yield atomObj


    def CalcBBDihedralAngle(self, dihedralSideStr):

        ownerChainObj = self.owner
        indexInOwner = ownerChainObj.sub.index(self)
        resCoordDict = {atomObj.name: atomObj.coord for atomObj in self}

        if dihedralSideStr.lower() in ['l', 'phi']:

            if indexInOwner == 0:
                logging.warning('First residue of the chain can not calc left dihedral. Will return None.')
                return None

            for atomObj in ownerChainObj[indexInOwner - 1]:
                if atomObj.name == 'C':
                    leftCCoord = atomObj.coord
                    break

            return CalcDihedralAngle(leftCCoord, resCoordDict['N'], resCoordDict['CA'], resCoordDict['C'])

        else:

            if self == ownerChainObj[-1]:
                logging.warning('Last residue of the chain can not calc right dihedral. Will return None.')
                return None

            for atomObj in ownerChainObj[indexInOwner + 1]:
                if atomObj.name == 'N':
                    rightNCoord = atomObj.coord
                    break

            return CalcDihedralAngle(resCoordDict['N'], resCoordDict['CA'], resCoordDict['C'], rightNCoord)


    def CalcBBRotationMatrixByDeltaAngle(self, dihedralSideStr, modifySideStr, rotationAngle):

        atomCoordDict = {atomObj.name: atomObj.coord for atomObj in self}

        if dihedralSideStr.lower() in ['l', 'phi']:
            moveCoord    = atomCoordDict['N']
            rotationAxis = atomCoordDict['CA'] - moveCoord
        else:
            moveCoord    = atomCoordDict['CA']
            rotationAxis = atomCoordDict['C'] - moveCoord

        if modifySideStr.lower() in ['l', 'n']:
            rotationAngle = -rotationAngle

        rotationMatrix = CalcRotationMatrix(rotationAxis, rotationAngle)

        return moveCoord, rotationMatrix


    def CalcBBRotationMatrix(self, dihedralSideStr, modifySideStr, targetAngle):

        sourceAngle = self.CalcBBDihedralAngle(dihedralSideStr)

        if sourceAngle == None:
            logging.warning('Can not calc rotation matrix becase the backbone dihedral is None. Will return None.')
            return None

        rotationAngle = targetAngle - sourceAngle

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralSideStr, modifySideStr, rotationAngle)

        return moveCoord, rotationMatrix


    def GetRotationAtomObj(self, dihedralSideStr, modifySideStr):

        rotationAtomObjList = []
        ownerChainObj = self.owner
        indexInOwner = ownerChainObj.sub.index(self)

        if modifySideStr.lower() in ['l', 'n']:

            for resObj in ownerChainObj.sub[0:indexInOwner]:
                rotationAtomObjList.extend(resObj.sub)

            if dihedralSideStr.lower() not in ['l', 'phi']:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name not in ['CA', 'C', 'O', 'OXT']])

        else:

            if dihedralSideStr.lower() in ['l', 'phi']:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name not in ['N', 'CA']])
            else:
                rotationAtomObjList.extend([atomObj
                    for atomObj in self if atomObj.name in ['O', 'OXT']])

            for resObj in ownerChainObj.sub[indexInOwner + 1:]:
                rotationAtomObjList.extend(resObj.sub)

        return rotationAtomObjList


    def ModifyBBDihedralAngleByDeltaAngle(self, dihedralSideStr, modifySideStr, rotationAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralSideStr, modifySideStr, rotationAngle)

        rotationAtomObjList = self.GetRotationAtomObj(dihedralSideStr, modifySideStr)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


    def ModifyBBDihedralAngle(self, dihedralSideStr, modifySideStr, targetAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrix(
            dihedralSideStr, modifySideStr, targetAngle)

        rotationAtomObjList = self.GetRotationAtomObj(dihedralSideStr, modifySideStr)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord


################################################################################
# Atom Struct Class
################################################################################

class C_AtomStruct(__C_NotProteinStructBase):

    __slots__ = ('name', 'num', 'coord', 'following', 'owner')

    def __init__(self, atomName = '', atomNum = 0, atomCoordArray = array([0., 0., 0.]),
        atomFollowingInfo = '', owner = None):

        self.name = atomName
        self.num = atomNum
        self.coord = atomCoordArray
        self.following = atomFollowingInfo
        self.owner = owner

        if owner:
            owner.sub.append(self)


    def __repr__(self):

        return '<Atom object: %d %s %s, at 0x%X>' % (
            self.num, self.name, str(self.coord), id(self))

    __str__ = __repr__


    def __sub__(self, subAtomObj):

        return Dis(self.coord, subAtomObj.coord)


    def Copy(self):

        return C_AtomStruct(self.name, self.num, self.coord.copy(), self.following)


    def Dumps(self):

        ownerResidueObj = self.owner

        if ownerResidueObj:

            residueName = ownerResidueObj.name
            residueNum  = ownerResidueObj.num
            residueInsertChar = ownerResidueObj.ins

            ownerChainObj = ownerResidueObj.owner
            chainName = ownerChainObj.name if ownerChainObj else ''

        else:
            residueName, residueNum, residueInsertChar, chainName = '', 0, '', ''

        if self.name[0].isdigit() or len(self.name) == 4:
            atomName = '%-4s' % self.name
        else:
            atomName = ' %-3s' % self.name

        return 'ATOM  %5d %s %3s %1s%4d%1s   %8.3f%8.3f%8.3f%-26s\n' % (
            self.num, atomName, residueName, chainName, residueNum, residueInsertChar,
            self.coord[0], self.coord[1], self.coord[2],
            self.following.rstrip('\n'))