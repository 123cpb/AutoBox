#! bin/bash


cd data/MOLECULE
module add amber
antechamber -i MOLECULE.log -fi gout -o MOLECULE.mol2 -fo mol2 -c resp -rn MOLECULE
parmchk2 -i MOLECULE.mol2 -f mol2 -o MOLECULE.frcmod
tleap -f MOLECULE.in
module add anaconda
source activate md
acpype -x MOLECULE.inpcrd -p MOLECULE.prmtop -c user
conda deactivate
cd ..
cd ..