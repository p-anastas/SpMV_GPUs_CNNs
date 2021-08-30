#!/bin/bash 

# set the number of nodes and processes per node
#PBS -l nodes=1:ppn=8

# set max wallclock time
#PBS -l walltime=48:00:00

# set name of job
#PBS -N Init_suite

# set name of job error file
#PBS -e ./Outs/benchmark.err

# set name of job output file
#PBS -o ./Outs/benchmark.out

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

rootdir="/home/users/panastas/Diploma/Git-master/Benchmarks/Scripts/"
dir1="/local/panastas/Full_suite/"
cd $dir1

benchie="${rootdir}fs_benchmark.log"
vbenchie="${rootdir}vienna_fs_benchmark.log"
mbenchie="${rootdir}merge_fs_benchmark.log"
mtempie="${rootdir}mtmp.log"
tempie="${rootdir}tmp.log"
vtempie="${rootdir}vtmp.log"

cuSPARSE="${rootdir}cuSPARSE"
cuSP="${rootdir}cusplibrary-0.5.1/performance/spmv/spmv"
cuSP_conv="${rootdir}cusplibrary-0.5.1/performance/spmv/conv"
bhSPARSE="${rootdir}bhSPARSE/CSR5_cuda/spmv"
lightspmv="${rootdir}lightSpMV/lightspmv"
vienna="${rootdir}ViennaCL-1.7.1/examples/benchmarks/sparse"
merge="${rootdir}merge-spmv-master/_gpu_spmv_driver"

#cp  $benchie "$benchie.backup"
#rm -f $benchie
#rm -f $vbenchie
#rm -f $mbenchie
for filename in *.mtx;
do 
	cd /home/users/panastas/Mine
	time=$(date +"%T")
	echo "-----$filename Benchmark Started at $time-----" > $tempie

	echo "cuSPARSE" >> $tempie
	$cuSPARSE "$dir1${filename}" >> $tempie

	echo "cuSP" >> $tempie
	$cuSP  "$dir1${filename}"  "--value_type=double" >> $tempie

	echo "bhSPARSE" >> $tempie
	$bhSPARSE  "$dir1${filename}" >> $tempie

	echo "lightspmv" >> $tempie
	$lightspmv -i  "$dir1${filename}" -d 1 -f 0 -r 0 -m 100 >> $tempie

	$lightspmv -i  "$dir1${filename}" -d 1 -f 0 -r 1 -m 100 >> $tempie
	
	#echo "ViennaCl" >> $tempie
	#$vienna "$dir1${filename}" >> $tempie

	time=$(date +"%T")
	echo "------End of $filename Benchmark at $time------" >> $tempie

	##cat $tempie >> $benchie

	##mv "$dir1${filename}" "${dir1}Benched/${filename}"

	##/usr/local/cuda-7.5/bin/cuda-memcheck $gpu_prog ${filename}
	#$gpu_prog ${filename} ## nvprof --export-profile timeline.prof

	time=$(date +"%T")
	echo "-----$filename Benchmark Started at $time-----" > $vtempie

	echo "ViennaCl"  >> $vtempie
	$vienna "${dir1}${filename}"  >> $vtempie

	time=$(date +"%T")
	echo "------End of $filename Benchmark at $time------"  >> $vtempie

	time=$(date +"%T")
	echo "-----$filename Benchmark Started at $time-----" > $mtempie

	echo "merge_SpMV" >> $mtempie
	$merge --mtx="$dir1${filename}" --i=100 >> $mtempie --quiet

	time=$(date +"%T")
	echo "------End of $filename Benchmark at $time------" >> $mtempie

	# Finally output results for $filename
	cat $mtempie >> $mbenchie
	cat $vtempie >> $vbenchie
	cat $tempie >> $benchie

	mv "$dir1${filename}" "${dir1}Benched/${filename}"
	##mv "${dir1}Benched/${filename}" "$dir1${filename}" 
done


