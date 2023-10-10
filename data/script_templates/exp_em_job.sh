#$ -cwd 
#$ -V
#$ -l h_rt=48:00:00
#$ -l coproc_v100=1

module unload gromacs
module load gromacs/2022.2gpu
module load cuda
gmx mdrun -ntmpi 1 -s em.tpr -deffnm em 