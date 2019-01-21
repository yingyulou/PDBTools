#!/bin/env python
# coding=UTF-8

'''
    PDBParser
    =========
        PDB parser function define.
'''

# Import Python Lib
from os.path import splitext, basename
from re import compile
from numpy import array

# Import PDBTools
from .StructClass import Protein, Chain, Residue, Atom

# Global Variable Define
CONST_H_RE = compile(r'\d*H')

################################################################################
# Parse PDB File
################################################################################

def Load(pdbFileName, parseHBool = False):

    proObj = Protein(splitext(basename(pdbFileName))[0])

    lastChainName = None
    lastResName   = None
    lastResNum    = None
    lastResIns    = None

    with open(pdbFileName) as f:

        for line in f:

            if line[:4] != 'ATOM':
                continue

            atomName = line[12:16].strip()

            if CONST_H_RE.match(atomName) and not parseHBool:
                continue

            atomNum        = int(line[6:11])
            atomIns        = line[16].strip()
            resName        = line[17:20].strip()
            chainName      = line[21].strip()
            resNum         = int(line[22:26])
            resIns         = line[26].strip()
            atomCoord      = array((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            atomOccupancy  = float(line[54:60])
            atomTempFactor = float(line[60:66])
            atomElement    = line[76:78].strip()
            atomCharge     = line[78:80].strip()

            if chainName != lastChainName:

                lastChainName = chainName
                chainObj = Chain(chainName, proObj)

            if lastResNum != resNum or lastResName != resName or lastResIns != resIns:

                lastResNum, lastResName, lastResIns = resNum, resName, resIns
                resObj = Residue(resName, resNum, resIns, chainObj)

            Atom(atomName, atomNum, atomCoord, atomIns, atomOccupancy, atomTempFactor,
                atomElement, atomCharge, resObj)

    return proObj


################################################################################
# Parse PDB File With Model
################################################################################

def LoadModel(pdbFileName, parseHBool = False):

    pdbIdStr   = splitext(basename(pdbFileName))[0]
    proObj     = Protein('%s_model_0' % pdbIdStr)
    proObjList = [proObj]

    lastChainName = None
    lastResName   = None
    lastResNum    = None
    lastResIns    = None

    with open(pdbFileName) as f:

        for line in f:

            if line[:5] == 'MODEL':

                proObj = Protein('%s_model_%s' % (pdbIdStr, line.split()[1]))
                proObjList.append(proObj)

                lastChainName = None
                lastResName   = None
                lastResNum    = None
                lastResIns    = None

                continue

            elif line[:4] != 'ATOM':
                continue

            atomName = line[12:16].strip()

            if CONST_H_RE.match(atomName) and not parseHBool:
                continue

            atomNum        = int(line[6:11])
            atomIns        = line[16].strip()
            resName        = line[17:20].strip()
            chainName      = line[21].strip()
            resNum         = int(line[22:26])
            resIns         = line[26].strip()
            atomCoord      = array((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            atomOccupancy  = float(line[54:60])
            atomTempFactor = float(line[60:66])
            atomElement    = line[76:78].strip()
            atomCharge     = line[78:80].strip()

            if chainName != lastChainName:

                lastChainName = chainName
                chainObj = Chain(chainName, proObj)

            if lastResNum != resNum or lastResName != resName or lastResIns != resIns:

                lastResNum, lastResName, lastResIns = resNum, resName, resIns
                resObj = Residue(resName, resNum, resIns, chainObj)

            Atom(atomName, atomNum, atomCoord, atomIns, atomOccupancy, atomTempFactor,
                atomElement, atomCharge, resObj)

    if not proObjList[0]:
        proObjList.pop(0)

    return proObjList