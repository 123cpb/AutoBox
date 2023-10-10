# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:55:57 2023

deal with the molecules that are to be used in the simulations 

@author: py21capb
"""


import typer
import box_gen
import os 
import em 


app = typer.Typer()

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
        if not os.path.exists("data/" + x):
            os.mkdir("data/" + x) 
            
    if not os.path.exists("data/out"):
        os.mkdir("data/out")
        

def mv_log(mol_name):
    
    with open("data/gaussian_outputs/" + mol_name + ".log", 'r') as f:
        data = f.read()
        
    with open("data/" + mol_name + '/' + mol_name + ".log", 'w') as f:
        f.write(data)
        
@app.command()
def mix_gen(mol1:str, mol2:str, percent_a:int, percent_b:int, ntotal:int):
    
    mols = [mol1, mol2]
    mk_dirs(mols)
    
    mv_log(mol1)
    mv_log(mol2)
    
    box_gen.create_structs(mol1, mol1)
    box_gen.create_structs(mol2, mol2) 
    
    nmolA, nmolB = box_gen.mix_ff_gen(mol1, mol2, percent_a,
                                 percent_b, ntotal)
    
    box_gen.move_struct_file(mol1)
    box_gen.move_struct_file(mol2)
    box_gen.mix_gen_bash(mol1, mol2, nmolA, nmolB)
    
    em.move_files_bash(mol1, mol2)
    em.create_em_job()

@app.command()    
def auto_box(mol1: str, ntotal: int):
    
    mols = [mol1]
    mk_dirs(mols)
    
    mv_log(mol1)
    
    box_gen.create_structs(mol1, mol1)
    
    box_gen.box_ff_gen(mol1, ntotal)
    
    box_gen.move_struct_file(mol1)
    box_gen.box_gen_bash(mol1, ntotal)    
    
    em.move_file_bash(mol1)
    em.create_em_job()

if __name__ == "__main__":
    app()





    
