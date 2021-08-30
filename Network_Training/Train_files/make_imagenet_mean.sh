#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

CAFFE_ROOT=/home/users/athena/caffe/
EXAMPLE=examples/imagenet
TOOLS=${CAFFE_ROOT}build/tools
NEURAL_ROOT=/home/users/panastas/Training_material/Neural_data/ 
TRAIN_DATA_ROOT=${NEURAL_ROOT}Training_data
TEST_DATA_ROOT=${NEURAL_ROOT}Testing_data

$TOOLS/compute_image_mean $TRAIN_DATA_ROOT/train_lmdb \
  $TRAIN_DATA_ROOT/imagenet_mean.binaryproto

echo "Train Mean Computed."

$TOOLS/compute_image_mean $TEST_DATA_ROOT/val_lmdb \
  $TEST_DATA_ROOT/imagenet_mean.binaryproto

echo "Test Mean Computed"


