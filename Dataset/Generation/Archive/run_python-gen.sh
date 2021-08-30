#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=49:00:00

# set name of job
#PBS -N gen_pw_seq18

# set name of job error file
#PBS -e gen_pw_seq18.err

# set name of job output file
#PBS -o gen_pw_seq18.out

# memmory limit
##PBS -l mem=64GB


cd "/home/users/panastas/Mine/python_pic"

## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/python_pic/powerlaw_seq-gen.py"
python3 $gpu_prog "1.8"

