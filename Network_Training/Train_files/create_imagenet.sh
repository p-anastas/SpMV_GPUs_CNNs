#!/usr/bin/env sh
# Create the imagenet lmdb inputs
# N.B. set the path to the imagenet train + val data dirs
set -e

Input="all_data_RGB.in"
CAFFE_ROOT=/home/users/athena/caffe/
NEURAL_ROOT=/home/users/panastas/Training_material/Neural_data/ #/media/Shared/Drive/Diploma_thesis/Training_material/Neural_data/
TRAIN_DATA_ROOT=${NEURAL_ROOT}Training_data
VAL_DATA_ROOT=${NEURAL_ROOT}Testing_data
TOOLS=${CAFFE_ROOT}build/tools

rm -r -f $TRAIN_DATA_ROOT/train_lmdb
rm -r -f $VAL_DATA_ROOT/val_lmdb

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=false
if $RESIZE; then
  RESIZE_HEIGHT=256
  RESIZE_WIDTH=256
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet training data is stored."
  exit 1
fi

if [ ! -d "$VAL_DATA_ROOT" ]; then
  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
  echo "Set the VAL_DATA_ROOT variable in create_imagenet.sh to the path" \
       "where the ImageNet validation data is stored."
  exit 1
fi

echo "Creating train lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
	'' \
    $TRAIN_DATA_ROOT/train_$Input \
    $TRAIN_DATA_ROOT/train_lmdb

echo "Creating val lmdb..."

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    '' \
    $VAL_DATA_ROOT/test_$Input \
    $VAL_DATA_ROOT/val_lmdb

echo "Done."
