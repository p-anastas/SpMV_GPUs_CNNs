#!/usr/bin/env sh
set -e

CAFFE_ROOT=/home/users/athena/caffe/
NEURAL_ROOT=/home/users/panastas/Training_material/Neural_data/ 

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/various/common_tools/boost-1.54/lib

#${CAFFE_ROOT}/build/tools/caffe train \
#    --solver=${NEURAL_ROOT}caffe_train/Arch/Googlenet/solver.prototxt 

${CAFFE_ROOT}/build/tools/caffe train \
    --solver=${NEURAL_ROOT}caffe_train/Arch/caffenet/solver.prototxt 

#${CAFFE_ROOT}/build/tools/caffe train \
#	 --solver=${NEURAL_ROOT}caffe_train/Arch/lenet/lenet_solver.prototxt 
