#!/usr/bin/env python3
# coding=UTF-8

'''
    ResidueClass
    ============
        Class Residue define.
'''

# Import PDBTools
from .NotAtomStructInterface import __NotAtomStructInterface
from .NotProteinStructInterface import __NotProteinStructInterface
from .StructConst import DIH, SIDE, _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT
from .MathUtil import CalcVectorAngle, CalcRotationMatrix, CalcDihedralAngle

################################################################################
# Residue Struct Class
################################################################################

class Residue(__NotAtomStructInterface, __NotProteinStructInterface):

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

        return {atomObj.name: atomObj for atomObj in self}


    @property
    def coordDict(self):

        return {atomObj.name: atomObj.coord for atomObj in self}


    def Copy(self):

        copyResObj = Residue(self.name, self.num, self.ins)

        for atomObj in self:
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

        for atomObj in self:
            yield atomObj


    def CalcBBDihedralAngle(self, dihedralEnum):

        coordDict = self.coordDict

        if dihedralEnum == DIH.L:
            dihedralAngle = CalcDihedralAngle(
                self.pre.coordDict['C'], coordDict['N'], coordDict['CA'], coordDict['C'])
        elif dihedralEnum == DIH.R:
            dihedralAngle = CalcDihedralAngle(
                coordDict['N'], coordDict['CA'], coordDict['C'], self.next.coordDict['N'])
        else:
            raise ValueError("Argument 'dihedralEnum' must be DIH.(PHI/PSI/L/R)")

        return dihedralAngle


    def CalcBBRotationMatrixByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle):

        coordDict = self.coordDict

        if dihedralEnum == DIH.L:
            moveCoord    = coordDict['N']
            rotationAxis = coordDict['CA'] - moveCoord
        elif dihedralEnum == DIH.R:
            moveCoord    = coordDict['CA']
            rotationAxis = coordDict['C'] - moveCoord
        else:
            raise ValueError("Argument 'dihedralEnum' must be DIH.(PHI/PSI/L/R)")

        if sideEnum == SIDE.L:
            deltaAngle = -deltaAngle
        elif sideEnum != SIDE.R:
            raise ValueError("Argument 'sideEnum' must be SIDE.(N/C/L/R)")

        rotationMatrix = CalcRotationMatrix(rotationAxis, deltaAngle)

        return moveCoord, rotationMatrix


    def CalcBBRotationMatrixByTargetAngle(self, dihedralEnum, sideEnum, targetAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralEnum, sideEnum, targetAngle - self.CalcBBDihedralAngle(dihedralEnum))

        return moveCoord, rotationMatrix


    def GetBBRotationAtomObj(self, dihedralEnum, sideEnum):

        rotationAtomObjList = []

        if sideEnum == SIDE.L:

            for resObj in self.owner.sub[:self.idx]:
                rotationAtomObjList.extend(resObj.sub)

            if dihedralEnum == DIH.R:
                rotationAtomObjList.extend([atomObj for atomObj in self
                    if atomObj.name not in {'CA', 'C', 'O', 'OXT'}])
            elif dihedralEnum != DIH.L:
                raise ValueError("Argument 'dihedralEnum' must be DIH.(PHI/PSI/L/R)")

        elif sideEnum == SIDE.R:

            if dihedralEnum == DIH.L:
                rotationAtomObjList.extend([atomObj for atomObj in self
                    if atomObj.name not in {'N', 'CA'}])
            elif dihedralEnum == DIH.R:
                rotationAtomObjList.extend([atomObj for atomObj in self
                    if atomObj.name in {'O', 'OXT'}])
            else:
                raise ValueError("Argument 'dihedralEnum' must be DIH.(PHI/PSI/L/R)")

            for resObj in self.owner.sub[self.idx + 1:]:
                rotationAtomObjList.extend(resObj.sub)

        else:
            raise ValueError("Argument 'sideEnum' must be SIDE.(N/C/L/R)")

        return rotationAtomObjList


    def RotateBBDihedralAngleByDeltaAngle(self, dihedralEnum, sideEnum, deltaAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByDeltaAngle(
            dihedralEnum, sideEnum, deltaAngle)

        rotationAtomObjList = self.GetBBRotationAtomObj(dihedralEnum, sideEnum)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord

        return self


    def RotateBBDihedralAngleByTargetAngle(self, dihedralEnum, sideEnum, targetAngle):

        moveCoord, rotationMatrix = self.CalcBBRotationMatrixByTargetAngle(
            dihedralEnum, sideEnum, targetAngle)

        rotationAtomObjList = self.GetBBRotationAtomObj(dihedralEnum, sideEnum)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord

        return self


    def CalcSCDihedralAngle(self, dihedralIdx):

        coordDict = self.coordDict
        atomNameA, atomNameB, atomNameC, atomNameD = \
            _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][:4]

        scDihedralAngle = CalcDihedralAngle(
            coordDict[atomNameA], coordDict[atomNameB],
            coordDict[atomNameC], coordDict[atomNameD],
        )

        return scDihedralAngle


    def CalcSCRotationMatrixByDeltaAngle(self, dihedralIdx, deltaAngle):

        coordDict = self.coordDict
        atomNameA, atomNameB = \
            _RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][1:3]

        moveCoord = coordDict[atomNameA]
        rotationAxis = coordDict[atomNameB] - coordDict[atomNameA]

        rotationMatrix = CalcRotationMatrix(rotationAxis, deltaAngle)

        return moveCoord, rotationMatrix


    def CalcSCRotationMatrixByTargetAngle(self, dihedralIdx, targetAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByDeltaAngle(
            dihedralIdx, targetAngle - self.CalcSCDihedralAngle(dihedralIdx))

        return moveCoord, rotationMatrix


    def GetSCRotationAtomObj(self, dihedralIdx):

        rotationAtomNameSet = set(_RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT[self.name][dihedralIdx][3:])
        rotationAtomObjList = [atomObj for atomObj in self if atomObj.name in rotationAtomNameSet]

        return rotationAtomObjList


    def RotateSCDihedralAngleByDeltaAngle(self, dihedralIdx, deltaAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByDeltaAngle(dihedralIdx, deltaAngle)
        rotationAtomObjList = self.GetSCRotationAtomObj(dihedralIdx)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord

        return self


    def RotateSCDihedralAngleByTargetAngle(self, dihedralIdx, targetAngle):

        moveCoord, rotationMatrix = self.CalcSCRotationMatrixByTargetAngle(dihedralIdx, targetAngle)
        rotationAtomObjList = self.GetSCRotationAtomObj(dihedralIdx)

        for atomObj in rotationAtomObjList:
            atomObj.coord = (atomObj.coord - moveCoord).dot(rotationMatrix) + moveCoord

        return self