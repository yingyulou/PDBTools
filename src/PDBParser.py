#!/usr/bin/env python3
# coding=UTF-8

'''
    PDBParser
    =========
        PDB parser function define.
'''

# Import Python Lib
from os.path import splitext, basename
from numpy import array

# Import PDBTools
from .Protein import Protein
from .Chain import Chain
from .Residue import Residue
from .Atom import Atom
from .StructUtil import IsH

################################################################################
# Parse PDB File
################################################################################

def Load(pdbFilePath, parseHBool = False):

    proObj = Protein(splitext(basename(pdbFilePath))[0])

    lastChainName = None
    lastResName   = None
    lastResNum    = None
    lastResIns    = None

    with open(pdbFilePath) as f:

        for line in f:

            if line[:4] != 'ATOM':
                continue

            atomName = line[12:16].strip()

            if IsH(atomName) and not parseHBool:
                continue

            atomNum        = int(line[6:11])
            atomAltLoc     = line[16].strip()
            resName        = line[17:20].strip()
            chainName      = line[21].strip()
            resNum         = int(line[22:26])
            resIns         = line[26].strip()
            atomCoord      = array((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            atomOccupancy  = line[54:60].strip()
            atomTempFactor = line[60:66].strip()
            atomElement    = line[76:78].strip()
            atomCharge     = line[78:80].strip()

            if chainName != lastChainName:

                lastChainName = chainName
                chainObj = Chain(chainName, proObj)

            if lastResNum != resNum or lastResName != resName or lastResIns != resIns:

                lastResNum, lastResName, lastResIns = resNum, resName, resIns
                resObj = Residue(resName, resNum, resIns, chainObj)

            Atom(atomName, atomNum, atomCoord, atomAltLoc, atomOccupancy,
                atomTempFactor, atomElement, atomCharge, resObj)

    return proObj


################################################################################
# Parse PDB File With Model
################################################################################

def LoadModel(pdbFilePath, parseHBool = False):

    pdbIdStr   = splitext(basename(pdbFilePath))[0]
    proObj     = Protein(pdbIdStr)
    proObjList = [proObj]

    lastChainName = None
    lastResName   = None
    lastResNum    = None
    lastResIns    = None

    with open(pdbFilePath) as f:

        for line in f:

            if line[:5] == 'MODEL':

                proObj = Protein(pdbIdStr)
                proObjList.append(proObj)

                lastChainName = None
                lastResName   = None
                lastResNum    = None
                lastResIns    = None

                continue

            elif line[:4] != 'ATOM':
                continue

            atomName = line[12:16].strip()

            if __H_RE.match(atomName) and not parseHBool:
                continue

            atomNum        = int(line[6:11])
            atomAltLoc     = line[16].strip()
            resName        = line[17:20].strip()
            chainName      = line[21].strip()
            resNum         = int(line[22:26])
            resIns         = line[26].strip()
            atomCoord      = array((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            atomOccupancy  = line[54:60].strip()
            atomTempFactor = line[60:66].strip()
            atomElement    = line[76:78].strip()
            atomCharge     = line[78:80].strip()

            if chainName != lastChainName:

                lastChainName = chainName
                chainObj = Chain(chainName, proObj)

            if lastResNum != resNum or lastResName != resName or lastResIns != resIns:

                lastResNum, lastResName, lastResIns = resNum, resName, resIns
                resObj = Residue(resName, resNum, resIns, chainObj)

            Atom(atomName, atomNum, atomCoord, atomAltLoc, atomOccupancy,
                atomTempFactor, atomElement, atomCharge, resObj)

    if not proObjList[0]:
        proObjList.pop(0)

    return proObjList
