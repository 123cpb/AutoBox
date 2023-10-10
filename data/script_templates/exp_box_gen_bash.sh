#! /bin/bash

module add gromacs 

cd data/out 

gmx editconf -f MOLECULE1.gro -o MOLECULE1.gro -bt cubic -d 2 
gmx genconf -f MOLECULE1.gro -nbox X Y Z -o box.gro -rot

cd .. 
cd ..