#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=1

# set max wallclock time
#PBS -l walltime=24:00:00

# set name of job
#PBS -N train_me_up

# set name of job error file
#PBS -e ./train.err

# set name of job output file
#PBS -o ./train.out

# memmory limit
##PBS -l mem=64GB

##cd /home/users/panastas/Mine
##make clean
##make
##cd /home/users/panastas/Mine/cusplibrary-0.5.1/performance/spmv
##make clean
##make
##cd /home/users/panastas/Mine/bhSPARSE/CSR5_cuda
##make clean
##make
##cd /home/users/panastas/Mine/lightSpMV
##make clean
##make 
##cd /home/users/panastas/Mine/ViennaCL-1.7.1/examples/benchmarks
##make clean
##make

dir1="/home/users/panastas/Training_material/Neural_data/caffe_train"
cd $dir1

./train_caffenet.sh
