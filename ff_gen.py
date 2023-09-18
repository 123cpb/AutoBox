# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:47:18 2023

edit the topologies and itp files so that they will work with simulations

@author: py21capb
"""

import re
import sys 

script_templates = "script_templates/"

out = "mix/"

mol1 = "butanol"
mol2 = "methanol"



def binary_mixtures(a, b, nmol):
    """
    Work out how many molecules are needed for the percentage ratios     

    Parameters
    ----------
    a : int
        percentage of mol1
    b : int
        percentage of mol2
    nmol : int
        total number of molecules

    Returns
    -------
    number of molecules, a and b 

    """
    
    # calculate mixture composition percentages  
    nmol_a = int((a / 100) * nmol)
    nmol_b = int((b / 100) * nmol) 
    
    return nmol_a, nmol_b

def create_itp(mol_name):
    """
    create an itp file from the generated top file. removes the [molecule type]
    [system] and [molecules] tags

    Parameters
    ----------
    mol_name : string
        the name of the topology file to turn into an itp file

    Returns
    -------
    an itp file

    """
        
    with open(mol_name + "/"+ mol_name + ".top", 'r') as f:
        data = f.read()
        split_data = re.split('\n\n', data)      
    
    # defaults for use in mixture topology file
    defaults = split_data[1]
    
    # get the desired sections of the old topology file 
    new_file = split_data[2:9]
    
    # write them to a new itp file
    with open(mol_name + "/" + mol_name + '.itp', 'w') as f: 
        for x in new_file: 
            f.write(x + '\n\n')
            
    return defaults 

def create_top(nmol_A, nmol_B, defaults):
    # what to replace in the example topology script 
    find = ["mol1", "mol2", "X", "Y"]
    replace = [mol1, mol2, str(nmol_A), str(nmol_B)]
    
    # open the example topology file and read its contents
    with open(script_templates+"exp_top.top", 'r') as f:
        data = f.read()
    
    # replace the placeholder text    
    for x in range(len(find)):
        data = data.replace(find[x], replace[x])
    
    # create the mixture topology file 
    with open(out+"mix.top", 'w') as f: 
        f.write(defaults)
        f.write(data)
    
def merge_atomtypes(mol1, mol2):
    """
    merge the atom types into the first mol file and delete it from the second

    Parameters
    ----------
    mol1 : string
        name of the first molecule
    mol2 : string
        name of the second molecule

    Returns
    -------
    None.

    """
    
    # dictionaries to store the atom types and their details 
    mol1_atomtypes = {}
    mol2_atomtypes = {}
    
    # open the new itp file for mol1 and split into sections
    with open(mol1+"/"+mol1 + ".itp", 'r') as f:
        data1 = f.read()
        split_data1 = re.split('\n\n', data1)
    
    # open the new itp file for mol2 and split into sections
    with open(mol2+"/"+mol2 + ".itp", 'r') as f:
        data2 = f.read()
        split_data2 = re.split('\n\n', data2)
        
    # select the atom types section
    atom_types_1 = split_data1[0]
    atom_types_2 = split_data2[0]
    
    # split the atom tpyes section into a list of lines
    atom_types_1 = re.split('\n', atom_types_1)
    atom_types_2 = re.split('\n', atom_types_2)
    
    # split each element of the list based on white space and select the atom 
    # type     
    for x in atom_types_1[2:]:
        split = x.split(" ")
        mol1_atomtypes[split[1]] = x
        
    for x in atom_types_2[2:]:
        split = x.split(" ")
        mol2_atomtypes[split[1]] = x
        
    # this dictionary will be written to the mol1 itp file
    new_dict = mol1_atomtypes    
        
    # if a key of the mol2 dictionary is not in the mol1 dictionary add it to
    # it
    for x in mol2_atomtypes:
        if x not in mol1_atomtypes:
            new_dict[x] = mol2_atomtypes[x]
            
    # write a new mol1 itp file with the update dictionary 
    with open(out+mol1 + ".itp", 'w') as f:
        
        f.write("[ atomtypes ]")
        f.write('\n')
        
        for x in new_dict:
            f.write(new_dict[x])
            f.write('\n')
        
        f.write('\n')
            
        for x in split_data1[1:]:
            f.write(x)
            f.write('\n\n')
    
    # write a new mol2 itpp25  without the atom types section 
    with open(out+mol2 + ".itp", 'w') as f: 
        for x in split_data2[1:]:
            f.write(x)
            f.write('\n\n')

def ff_gen(percentA, percentB, nmol):
    """
    generate the itp and topologies for the outputs of two acpype runs

    Parameters
    ----------
    percentA : int
        desired composition percentage of mol1
    percentB : int
        desired composition percentage of mol2 
    nmol : int
        total number of molecules in a simulation 

    Returns
    -------
    None.

    """
    
    # calculate number of molecules for the desired composition 
    nMolA, nMolB = binary_mixtures(percentA, percentB, nmol)
    
    # create itp files from the generated topology files
    defaults = create_itp(mol1)
    create_itp(mol2)
    
    # create a mixture topology file 
    create_top(nMolA, nMolB, defaults)
    
    # merge the atom types from the itp files into mol1.itp 
    merge_atomtypes(mol1, mol2)
    
    return nMolA, nMolB

if __name__ == "__main__":
    ff_gen(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    