# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:55:57 2023

deal with the molecules that are to be used in the simulations 

@author: py21capb
"""


import box_gen
import ff_gen
import ante_gen
import os 
import sys

class Molecule:
    def __init__(self, mol_name, abr_mol_name, smiles):
        self.mol_name = mol_name
        self.abr_mol_name = abr_mol_name 
        self.smiles = smiles 

rm734 = Molecule("rm734", "rm7", "CCCCCCOCOCOCO")
dio = Molecule("DIO", "DIO", "CCCCOCOCOCO")

def mk_dirs(mols):
    """
    create a folder to out the acpype stuff for each molecule

    Parameters
    ----------
    mol_name : string
        name of the directory to be created.

    Returns
    -------
    None.

    """
    for x in mols:
        if not os.path.exists(x):
            os.mkdir(x) 
            
    if not os.path.exists("mix"):
        os.mkdir("mix")


if __name__ == "__main__":

    mols = [sys.argv[1], sys.argv[2]]
    
    mk_dirs(mols)
    ante_gen.create_structs(mols[0], "but")
    ante_gen.create_structs(mols[1], "eth") 
    nmolA, nmolB = ff_gen.ff_gen(75, 25, 100)
    box_gen.box_gen_bash(mols[0], mols[1], nmolA, nmolB)





    
