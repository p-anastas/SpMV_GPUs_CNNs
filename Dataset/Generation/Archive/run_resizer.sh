#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=36:00:00

# set name of job
#PBS -N 1_core_generator

# set name of job error file
#PBS -e Outs/aug_arr.err

# set name of job output file
#PBS -o Outs/aug_arr.out

# memmory limit
##PBS -l mem=7GB

export PATH=/usr/local/python3.4/bin/:$PATH

dirn="/local/panastas/small_suite/"
dest="/local/panastas/Augumented_small_suite/"
cd $dirn
## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/python_pic/Block_dataset_create.py"

for filename in *.mtx;
do
cd "/home/users/panastas/Mine/python_pic"
python3  $gpu_prog
done
