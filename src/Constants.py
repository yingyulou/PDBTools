#!/usr/bin/env python3
# coding=UTF-8

'''
    Constants
    =========
        Constants define.
'''

# Import Python Lib
from re import compile
from enum import Enum

################################################################################
# H Atom Regex
################################################################################

__H_RE = compile(r'\d*H')


################################################################################
# CompNum Regex
################################################################################

__COMP_NUM_RE = compile(r'(\d+)([A-Za-z]?)')


################################################################################
# Backbone Dihedral Enum
################################################################################

class DIH(Enum):

    PHI = 0
    L   = 0
    PSI = 1
    R   = 1


################################################################################
# Backbone Modify Side Enum
################################################################################

class SIDE(Enum):

    N = 0
    L = 0
    C = 1
    R = 1


################################################################################
# Dict: Transform Residue Name From 3 Words => 1 Word
################################################################################

RESIDUE_NAME_THREE_TO_ONE_DICT = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLN': 'Q',
    'GLU': 'E',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V',
    'UNK': 'X',
}


################################################################################
# Dict: Transform Residue Name From 1 Word => 3 Words
################################################################################

RESIDUE_NAME_ONE_TO_THREE_DICT = {
    'A': 'ALA',
    'R': 'ARG',
    'N': 'ASN',
    'D': 'ASP',
    'C': 'CYS',
    'Q': 'GLN',
    'E': 'GLU',
    'G': 'GLY',
    'H': 'HIS',
    'I': 'ILE',
    'L': 'LEU',
    'K': 'LYS',
    'M': 'MET',
    'F': 'PHE',
    'P': 'PRO',
    'S': 'SER',
    'T': 'THR',
    'W': 'TRP',
    'Y': 'TYR',
    'V': 'VAL',
    'X': 'UNK',
}


################################################################################
# Dict: Residue Name => Sidechain Rotation Atoms Name
################################################################################

_RESIDUE_SIDECHAIN_ROTATION_ATOMS_NAME_DICT = {

    'ALA': (),

    'ARG': (
        ('N', 'CA', 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'),
        ('CA', 'CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'),
        ('CB', 'CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'),
        ('CG', 'CD', 'NE', 'CZ', 'NH1', 'NH2'),
    ),

    'ASN': (
        ('N', 'CA', 'CB', 'CG', 'OD1', 'ND2'),
        ('CA', 'CB', 'CG', 'OD1', 'ND2'),
    ),

    'ASP': (
        ('N', 'CA', 'CB', 'CG', 'OD1', 'OD2'),
        ('CA', 'CB', 'CG', 'OD1', 'OD2'),
    ),

    'CYS': (
        ('N', 'CA', 'CB', 'SG'),
    ),

    'GLN': (
        ('N', 'CA', 'CB', 'CG', 'CD', 'OE1', 'NE2'),
        ('CA', 'CB', 'CG', 'CD', 'OE1', 'NE2'),
        ('CB', 'CG', 'CD', 'OE1', 'NE2'),
    ),

    'GLU': (
        ('N', 'CA', 'CB', 'CG', 'CD', 'OE1', 'OE2'),
        ('CA', 'CB', 'CG', 'CD', 'OE1', 'OE2'),
        ('CB', 'CG', 'CD', 'OE1', 'OE2'),
    ),

    'GLY': (),

    'HIS': (
        ('N', 'CA', 'CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2'),
        ('CA', 'CB', 'CG', 'ND1', 'CD2', 'CE1', 'NE2'),
    ),

    'ILE': (
        ('N', 'CA', 'CB', 'CG1', 'CG2', 'CD1'),
        ('CA', 'CB', 'CG1', 'CD1'),
    ),

    'LEU': (
        ('N', 'CA', 'CB', 'CG', 'CD1', 'CD2'),
        ('CA', 'CB', 'CG', 'CD1', 'CD2'),
    ),

    'LYS': (
        ('N', 'CA', 'CB', 'CG', 'CD', 'CE', 'NZ'),
        ('CA', 'CB', 'CG', 'CD', 'CE', 'NZ'),
        ('CB', 'CG', 'CD', 'CE', 'NZ'),
        ('CG', 'CD', 'CE', 'NZ'),
    ),

    'MET': (
        ('N', 'CA', 'CB', 'CG', 'SD', 'CE'),
        ('CA', 'CB', 'CG', 'SD', 'CE'),
        ('CB', 'CG', 'SD', 'CE'),
    ),

    'PHE': (
        ('N', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'),
        ('CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'),
    ),

    'PRO': (
        ('N', 'CA', 'CB', 'CG', 'CD'),
        ('CA', 'CB', 'CG', 'CD'),
    ),

    'SER': (
        ('N', 'CA', 'CB', 'OG'),
    ),

    'THR': (
        ('N', 'CA', 'CB', 'OG1', 'CG2'),
    ),

    'TRP': (
        ('N', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'),
        ('CA', 'CB', 'CG', 'CD1', 'CD2', 'NE1', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'),
    ),

    'TYR': (
        ('N', 'CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'),
        ('CA', 'CB', 'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ', 'OH'),
    ),

    'VAL': (
        ('N', 'CA', 'CB', 'CG1', 'CG2'),
    ),
}
