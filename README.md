# AutoBox

* Automatically generate Gromacs structure files from Gaussian output files. 
* Place gaussian outputs in the data/gaussian_outputs file
* Requires python environment with acpype. pip install -r requirements.txt to get modules


**What it does** 
Antechamber - convert .log to mol2 antechamber and tleap. parameterises molecules
Acpype - creates topologies and gromacs files from antechamber outputs 
Creates new itp and topologies if needed (for mixtures)
Stacks gromacs structures to create a box 
(mixture) insert second molecule type
generates the necessary files (job script) to run an energy minimisation

**COMMANDS**

1. auto-box (MOLECULE_NAME) (TOTAL NUMBER OF MOLECULES IN SIMULATION BOX)
  Construct a gromacs simulation box of a single molecule   
2. mix-gen (MOLECULEA_NAME) (MOLECULEB_NAME) (PERCENTAGE OF MOLECULEA) (PERCENTAGE OF MOLECULEB) (TOTAL NUMBER OF MOLECULES IN SIMULATION BOX)
  Construct a simulation box of a mixture fo molecules. Note molecule A should be the component with the largest number of molecules 
