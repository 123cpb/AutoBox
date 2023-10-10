#! /bin/bash

module add gromacs 

cd data/out 

gmx editconf -f MOLECULE1.gro -o MOLECULE1.gro -bt cubic -d 2 
gmx genconf -f MOLECULE1.gro -nbox X Y Z -o box.gro -rot
gmx editconf -f MOLECULE2.gro -o MOLECULE2.gro -bt cubic -d 2 
gmx insert-molecules -ci MOLECULE2.gro -nmol nmolB -f box.gro -o mixed_box.gro

cd ..
cd .. 