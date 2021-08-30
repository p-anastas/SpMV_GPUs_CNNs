#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=1:00:00

# set name of job
#PBS -N manager

# set name of job error file
#PBS -e Outs/manager.err

# set name of job output file
#PBS -o Outs/manager.out

# memmory limit
##PBS -l mem=7GB

cd /home/users/panastas/Mine/python_pic/
## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/python_pic/Crop_crop.py"

rootdir="/local/panastas"
for dir1 in ["/Augumented_block_suite/", "/powerlaw_cluster/", "/Div_resized_small/", "/powerlaw_seq_graphs/", "/resized_small/"]
do
	python3 $gpu_prog "${rootdir}${dir1}Pics"
done

