# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 17:45:43 2023

create a bash script that will produce a simulation box of desired parameters 

@author: py21capb
"""

import sys
import os
import pathlib
import re

script_templates = "data/script_templates/"
out = "data/out/"

def ante_bash(mol_name):
    """
    write an amber script to generate an antechamber script for converting
    gaussian outputs to mol2 and then producing structures and topologies
    
    
    and then run the bash script
    """
    find = "MOLECULE"
    replace = mol_name
    
    with open(script_templates+"exp_ante_bash.sh", 'r') as f:
        data = f.read()
        data = data.replace(find, replace)
    
    with open("data/" + mol_name + "/" + mol_name + "Antechamber.sh", 'w') as f:
        f.write(data)
    
    os.system("dos2unix data/" + mol_name + "/" + mol_name + "Antechamber.sh")
    os.system("bash data/" + mol_name + "/" + mol_name + "Antechamber.sh")

def tleap_file(mol_name, mol):
    """
    write a tleap.in script for producing 
    """
    find = ["MOLECULE", "MOL"]
    replace = [mol_name, mol]
    
    with open(script_templates + "exp_tleap.in", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
    
    with open("data/" + mol_name + "/" + mol_name + ".in", 'w') as f: 
        f.write(data)
    
    os.system("dos2unix data/" + mol_name + "/" + mol_name + ".in")
        
def create_structs(mol_name, mol):
    """
    create gromacs structures and topology files for the molecules 

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

    # get the directory of the acpype output 
    directory = "data/" + mol_name
    path = pathlib.Path(directory)
    for x in path.iterdir():
        if "amb2gmx" in str(x):
            amb2gmx = pathlib.Path(x)
            
    for x in amb2gmx.iterdir():
        if ".top" in str(x):
            top_file = x
    
    with open(top_file, 'r') as f:
        data = f.read()
        split_data = re.split('\n\n', data)      
    
    # defaults for use in mixture topology file
    defaults = split_data[1]
    
    # get the desired sections of the old topology file 
    new_file = split_data[2:9]
    
    # write them to a new itp file
    with open("data/" + mol_name + "/" + mol_name + '.itp', 'w') as f: 
        for x in new_file: 
            f.write(x + '\n\n')
    
    for x in new_file: 
        if "moleculetype" in x: 
            mol_type = x.split('\n')[2]
            mol_type = mol_type.split(' ')
            mol_type = mol_type[1]
            
        
    return defaults, mol_type

def create_single_itp(mol_name):
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

    # get the directory of the acpype output 
    directory = "data/" + mol_name
    path = pathlib.Path(directory)
    for x in path.iterdir():
        if "amb2gmx" in str(x):
            amb2gmx = pathlib.Path(x)
            
    for x in amb2gmx.iterdir():
        if ".top" in str(x):
            top_file = x
    
    with open(top_file, 'r') as f:
        data = f.read()
        split_data = re.split('\n\n', data)      
    
    # defaults for use in mixture topology file
    defaults = split_data[1]
    
    # get the desired sections of the old topology file 
    new_file = split_data[2:9]
    
    # write them to a new itp file
    with open(out + mol_name + '.itp', 'w') as f: 
        for x in new_file: 
            f.write(x + '\n\n')
    
    for x in new_file: 
        if "moleculetype" in x: 
            mol_type = x.split('\n')[2]
            mol_type = mol_type.split(' ')
            mol_type = mol_type[1]
                    
    return defaults, mol_type

def create_mix_top(mol1, mol2, mol1_type, mol2_type, nmol_A, nmol_B, defaults):
    # what to replace in the example topology script 
    find = ["mol1type", "mol2type", "mol1", "mol2", "X", "Y"]
    replace = [mol1_type, mol2_type, mol1, mol2, str(nmol_A), str(nmol_B)]
    
    # open the example topology file and read its contents
    with open(script_templates+"exp_mix_top.top", 'r') as f:
        data = f.read()
    
    # replace the placeholder text    
    for x in range(len(find)):
        data = data.replace(find[x], replace[x])
    
    # create the mixture topology file 
    with open(out+"mix.top", 'w') as f: 
        f.write(defaults)
        f.write(data)
        
def create_auto_top(mol1, mol1_type, nmol, defaults):
    find = ["mol1type", "mol1", "X"]
    replace = [mol1_type, mol1, str(nmol)]
    
    with open(script_templates+"exp_box_top.top", 'r') as f: 
        data = f.read()
        
    for x in range(len(find)):
        data = data.replace(find[x], replace[x])
        
    with open(out+"box.top", 'w') as f: 
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
    with open("data/"+mol1+"/"+mol1 + ".itp", 'r') as f:
        data1 = f.read()
        split_data1 = re.split('\n\n', data1)
    
    # open the new itp file for mol2 and split into sections
    with open("data/"+mol2+"/"+mol2 + ".itp", 'r') as f:
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

def mix_ff_gen(mol1, mol2, percentA, percentB, nmol):
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
    defaults, mol1_type = create_itp(mol1)
    defaults2, mol2_type = create_itp(mol2)
    
    # create a mixture topology file 
    create_mix_top(mol1, mol2, mol1_type, mol2_type, nMolA, nMolB, defaults)
    
    # merge the atom types from the itp files into mol1.itp 
    merge_atomtypes(mol1, mol2)
    
    return nMolA, nMolB


def box_ff_gen(mol1, nmol):
    """ 
    generate a topology and itp file for a single molecule type box
    """
    
    defaults, mol1_type = create_single_itp(mol1) 
    
    create_auto_top(mol1, mol1_type, nmol, defaults)
    
    return nmol 


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

def move_struct_file(mol_name):
    """
    Move the structure file from the acpype output folder to
    the mixture files folder so it can be turned into a 
    simulation box by gromacs
    """
    directory = "data/" + mol_name
    path = pathlib.Path(directory)
    for x in path.iterdir():
        if "amb2gmx" in str(x):
            amb2gmx = pathlib.Path(x)
            
    for x in amb2gmx.iterdir():
        if ".gro" in str(x):
            struct_file = x
        
    with open(struct_file, 'r') as f:
        data = f.read()
        
    with open(out + mol_name + ".gro", 'w') as f:
        f.write(data)
        

def mix_gen_bash(mol1_name, mol2_name, nmolA, nmolB):
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
    replace = [mol1_name, mol2_name, str(x[0]), str(x[1]), str(x[2]), str(nmolB)]
    
    
    with open(script_templates+"exp_mix_gen_bash.sh", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
    
    # write a new bash script         
    with open(out+"box_gen.sh", 'w') as file:
        file.write(data)
    
    os.system("dos2unix " + out+"/box_gen.sh")
    os.system("bash "+ out+"/box_gen.sh")
    
def box_gen_bash(mol1, nTotal):
    x = construct_box(nTotal)
    
    find = ["MOLECULE1", "X", "Y", "Z"]
    replace = [mol1, str(x[0]), str(x[1]), str(x[2])]
    
    with open(script_templates+"exp_box_gen_bash.sh", 'r') as f:
        data = f.read()
        for x in range(len(find)):
            data = data.replace(find[x], replace[x])
    
    with open(out+"box_gen.sh", 'w') as f:
        f.write(data)
        
    os.system("dos2unix " + out+"/box_gen.sh")
    os.system("bash "+ out+"/box_gen.sh")

if __name__ == "__main__":
    mix_gen_bash(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))