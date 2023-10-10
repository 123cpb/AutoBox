# AutoBox

* Automatically generate Gromacs structure files from Gaussian output files. 
* Place gaussian outputs in the data/gaussian_outputs file

#How it works 

#COMMANDS

1. auto-box (MOLECULE_NAME) (TOTAL NUMBER OF MOLECULES IN SIMULATION BOX)
  Construct a gromacs simulation box of a single molecule   
2. mix-gen (MOLECULEA_NAME) (MOLECULEB_NAME) (PERCENTAGE OF MOLECULEA) (PERCENTAGE OF MOLECULEB) (TOTAL NUMBER OF MOLECULES IN SIMULATION BOX)
  Construct a simulation box of a mixture fo molecules. Note molecule A should be the component with the largest number of molecules 
