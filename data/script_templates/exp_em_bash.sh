cp data/out/mixed_box.gro data/out/em
cp data/out/MOLECULE1.itp data/out/em
cp data/out/MOLECULE2.itp data/out/em 
cp data/out/mix.top data/out/em 
cp data/script_templates/exp_em.mdp data/out/em/em.mdp

cd data/out/em

module unload gromacs
module load gromacs/2022.2gpu
gmx grompp -f em.mdp -c mixed_box.gro -p mix.top -o em.tpr

cd .. 
cd ..
cd .. 