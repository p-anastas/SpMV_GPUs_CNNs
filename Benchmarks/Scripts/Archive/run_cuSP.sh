#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=00:20:00

# set name of job
#PBS -N cuSP

# set name of job error file
#PBS -e ./Outs/cuSP.err

# set name of job output file
#PBS -o ./Outs/cuSP.out

# memmory limit
##PBS -l mem=64GB

cd /home/users/panastas/Mine/cusplibrary-0.5.1/performance/spmv
make clean
make

cd /risky_store/athena/training_suite
##cd /home/users/panastas/Mine/small_suite

## Change this to the directory of your executable!
gpu_prog="/home/users/panastas/Mine/cusplibrary-0.5.1/performance/spmv/spmv"
gpu_prog1="/home/users/panastas/Mine/cusplibrary-0.5.1/performance/spmv/conv"

for filename in *.mtx; 
do 
	##/usr/local/cuda-7.5/bin/cuda-memcheck $gpu_prog ${filename}
	##nvprof --analysis-metrics -f --export-profile Outs/$filename.cs.nvvp $gpu_prog "${filename}.mtx"
	$gpu_prog "${filename}"  "--value_type=double"
done

for filename in *.mtx; 
do 
	##/usr/local/cuda-7.5/bin/cuda-memcheck $gpu_prog ${filename}
	##nvprof --analysis-metrics -f --export-profile Outs/$filename.cs.nvvp $gpu_prog "${filename}.mtx"
	$gpu_prog1 ${filename}  --value_type=double > ~/Mine/Outs/cuSP_conv.out
done
