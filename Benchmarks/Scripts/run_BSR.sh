#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=8

# set max wallclock time
#PBS -l walltime=48:00:00

# set name of job
#PBS -N BSR-last

# set name of job error file
#PBS -e ./Outs/BSR.err

# set name of job output file
#PBS -o ./Outs/BSR.out

# memmory limit
##PBS -l mem=64GB

#cd /home/users/panastas/Mine
#make clean
#make
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

rootdir="/home/users/panastas/Diploma/Git-master/Benchmarks/Scripts/"
dir1="/local/panastas/Div_small_suite/"
#dir1="/home/users/panastas/Mine/tmp/"
#cd "${dir1}Benched/"
cd "${dir1}"

bbenchie="${rootdir}bsr_dss_benchmark.log"

tempie="${rootdir}tmp.log"

cuSPARSE="${rootdir}cuSPARSE"

#cp  $benchie "$benchie.backup"
#rm -f $bbenchie
for filename in *.mtx;
do 
	cd /home/users/panastas/Mine
	time=$(date +"%T")
	echo "-----$filename Benchmark Started at $time-----" > $tempie

	echo "cuSPARSE" >> $tempie
	$cuSPARSE "${dir1}${filename}" >> $tempie

	time=$(date +"%T")
	echo "------End of $filename Benchmark at $time------" >> $tempie

	# Finally output results for $filename

	cat $tempie >> $bbenchie

	mv "${dir1}${filename}" "${dir1}Benched/${filename}" 
	##mv "${dir1}Benched/${filename}" "$dir1${filename}" 
done


