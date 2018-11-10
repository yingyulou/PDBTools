#!/bin/env python
# coding=UTF-8

'''
    PDBParser
    =========
        PDB parser function define.
'''

# Import Python Lib
import six
from os.path import splitext, basename
from re import compile
from numpy import array

# Import PDBTools
if six.PY2:
    from .StructClass_py2 import C_ProteinStruct, C_ChainStruct, C_ResidueStruct, C_AtomStruct
else:
    from .StructClass import C_ProteinStruct, C_ChainStruct, C_ResidueStruct, C_AtomStruct

# Global Variable Define
CONST_H_RE = compile(r'\d*H')

################################################################################
# Parse PDB File
################################################################################

def Load(pdbFileName, parseHBool = False):

    with open(pdbFileName) as f:

        proteinStructObj = C_ProteinStruct(splitext(basename(pdbFileName))[0])

        lastChainName     = None
        lastResName       = None
        lastResNum        = None
        lastResInsertChar = None

        for line in f:

            if line[:4] != 'ATOM':
                continue

            atomName = line[12:16].strip()

            if CONST_H_RE.match(atomName) and not parseHBool:
                continue

            atomNum           = int(line[6:11])
            residueName       = line[17:20].strip()
            chainName         = line[21].strip()
            residueNum        = int(line[22:26])
            residueInsertChar = line[26].strip()
            atomCoordArray    = array((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            atomFollowingInfo = line[54:]

            if chainName != lastChainName:

                lastChainName = chainName
                chainStructObj = C_ChainStruct(chainName, proteinStructObj)

            if lastResNum != residueNum or lastResName != residueName or lastResInsertChar != residueInsertChar:

                lastResNum, lastResName, lastResInsertChar = residueNum, residueName, residueInsertChar
                residueStructObj = C_ResidueStruct(residueName, residueNum, residueInsertChar, chainStructObj)

            C_AtomStruct(atomName, atomNum, atomCoordArray, atomFollowingInfo, residueStructObj)

    return proteinStructObj