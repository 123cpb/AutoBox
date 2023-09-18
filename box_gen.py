# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:45:43 2023

create a bash script that will produce a simulation box of desired parameters 

@author: py21capb
"""

import sys

script_templates = "script_templates/"
out = "mix/"

def construct_box(nmolA):
    """
    construct a box of the molecule a 

    Parameters
    ----------
    nmolA : int
        total number of molecule a in the simulation.

    Returns
    -------
    
    """
    factors = []
    dimensions = []
    for i in range(1, nmolA+1):
        if nmolA % i == 0:
            factors.append(i)
            
    for i in factors:
        for j in factors: 
            for k in factors:
                if i*j*k == nmolA: 
                    dimensions.append([i,j,k])
    
    summed = sum(dimensions[0])
    
    for i in dimensions: 
        j = sum(i)
        if j < summed:
            summed = j 
            dimension = i 
        
    return dimension
    
def box_gen_bash(mol1, mol2, nmolA, nmolB):
    """
    generate a box of molecules 

    Parameters
    ----------
    mol1 : string
        name of the first molecule
    mol2 : string
        name of the second molecule
    x : int
        dimensions of the box of the first molecule
    y : int
        number of the second molecule being inserted

    Returns
    -------
    None.

    """
    
    # number of sides of the box of molA
    x = construct_box(nmolA)
    
    # replace the template script with the desired values
    find = ["MOLECULE1", "MOLECULE2", "X", "Y", "Z", "nmolB"]
    replace = [mol1, mol2, str(x[0]), str(x[1]), str(x[2]), str(nmolB)]
    
    with open(script_templates+"exp_box_gen_bash.sh", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
    
    # write a new bash script         
    with open(out+"box_gen.sh", 'w') as file:
        file.write(data)
        
if __name__ == "__main__":
    box_gen_bash(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))