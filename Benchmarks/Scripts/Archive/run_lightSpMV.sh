#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=5:00:00

# set name of job
#PBS -N lightSpMV

# set name of job error file
#PBS -e ./Outs/lightSpMV.err

# set name of job output file
#PBS -o ./Outs/lightSpMV.out

# memmory limit
##PBS -l mem=64GB

cd /home/users/panastas/Mine/lightSpMV
make clean
make 

cd /risky_store/athena/mmf_suite
##cd /users/guest/petyros/Mine/small_suite

## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/lightSpMV/lightspmv"

for filename in *.mtx; 
do 
	##/usr/local/cuda-7.5/bin/cuda-memcheck $gpu_prog ${filename}
	##nvprof --analysis-metrics -f --export-profile Outs/$filename.cs.nvvp $gpu_prog "${filename}.mtx"
	$gpu_prog -i ${filename} -d 1 -f 0 -r 0 -m 100  
done

for filename in *.mtx; 
do 
	##/usr/local/cuda-7.5/bin/cuda-memcheck $gpu_prog ${filename}
	##nvprof --analysis-metrics -f --export-profile Outs/$filename.cs.nvvp $gpu_prog "${filename}.mtx"
	$gpu_prog -i ${filename} -d 1 -f 0 -r 1 -m 100 
done
