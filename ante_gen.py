# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 17:14:27 2023

write a bash script that will automate the conversion of a gaussian output
to a mol2 file 

automate the acpype production of molecule topologies 


REWRITE THIS TO USE A TEMPLATE

@author: py21capb
"""

import sys 

out = "mix/"


def ante_bash(mol_name):
    """
    write an amber script to generate an antechamber script for converting
    gaussian outputs to mol2 and then producing structures and topologies
    
    """
    with open (mol_name+"/"+mol_name + "Antechamber.sh", 'w') as f: 
        f.write("#! /bin/bash\n\n")
        f.write("module add amber\n")
        f.write("antechamber -i " + mol_name + ".log -fi gout -o " + mol_name
                 + ".mol2 -fo mol2 -c resp -rn " + mol_name + "\n")
        f.write("parmchk2 -i " + mol_name + ".mol2 -f mol2 -o "  + mol_name + 
                ".frcmod\n")
        f.write("tleap -f " + mol_name + ".in\n")
        f.write("module add anaconda\n")
        f.write("source activate md\n")
        f.write("acpype -x " + mol_name + ".inpcrd -p " + 
                mol_name + ".prmtop -c user\n")
        f.write("conda deactivate")

def tleap_file(mol_name, mol):
    """
    write a tleap.in script for producing 
    """
    with open(mol_name+"/"+mol_name + ".in", 'w') as f:
        f.write("source oldff/leaprc.ff99SB\n")
        f.write("source leaprc.gaff\n")
        f.write(mol + " = loadmol2 "+ mol_name + ".mol2\n")
        f.write("loadamberparams " + mol_name + ".frcmod\n")
        f.write("saveoff " + mol + " " + mol + ".lib\n")
        f.write("saveamberparm " + mol + " " + mol_name + ".prmtop " +
                mol_name + ".inpcrd\n")
        f.write("quit")
        
def create_structs(mol_name, mol):
    """
    create gromac structures and topology files for the molecules 

    Parameters
    ----------
    mol_name : string
        name of the molecule
    mol : string
        abbreivated molecule name (3 letters)

    Returns
    -------
    None.

    """
    tleap_file(mol_name, mol)
    ante_bash(mol_name)
    
if __name__ == "__main__":
    create_structs(sys.argv[1], sys.argv[2])