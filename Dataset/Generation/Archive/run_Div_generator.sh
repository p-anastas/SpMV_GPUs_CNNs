#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=69:00:00

# set name of job
#PBS -N div_generator8

# set name of job error file
#PBS -e Outs/div_generator8.err

# set name of job output file
#PBS -o Outs/div_generator8.out

# memmory limit
##PBS -l mem=7GB

## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/python_pic/Div_generator_res.py"

cd /local/panastas/resized_small

for filename in *.mtx;
do
cd "/home/users/panastas/Mine/python_pic"
python3 $gpu_prog $filename "8"
done
