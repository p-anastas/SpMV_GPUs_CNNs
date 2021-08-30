CC=g++
ICC =icc

DEBUG ?= 1

CFLAGS=-O3 -lm -Wall #-mavx -march=ivybridge -mtune=ivybridge -fopenmp
#CFLAGS=-O3 -lm -Wall -mavx2 -mfma  -march=haswell -mtune=haswell 

#CFLAGS=-O3 -Wall -xCORE-AVX-I
#CFLAGS=-O3 -Wall -xCORE-AVX2 
#ICFLAGS=-O3 -Wall -qopenmp -axCORE-AVX2,CORE-AVX-I

##MPI_PREFIX = $(I_MPI_ROOT)
CUDA_PREFIX = $(CUDAROOT)
##GPU_MPI_CXX = nvcc -L $(I_MPI_ROOT)/lib64 -lmpi -ccbin mpiicc
GPU_CXX = nvcc

LDFLAGS ?=-L $(CUDA_PREFIX)/lib64 -lcudart -lcublas -lcusparse -lm -lrt

GPU_COMPILE = nvcc -I$(CUDA_PREFIX)/include -I./cusplibrary-0.5.1  -arch sm_35
##GPU_MPI_COMPILE = $(GPU_MPI_CXX) -I $(CUDA_PREFIX)/include -I $(I_MPI_ROOT)/include -arch sm_35
CPU_COMPILE = $(CC) $(CFLAGS)

ifeq ($(DEBUG), 1)
	CPU_COMPILE 	+= -D_DEBUG_
	GPU_COMPILE 	+= -D_DEBUG_
	GPU_MPI_COMPILE += -D_DEBUG_
endif

CPU_COMPILE_OBJ= $(CPU_COMPILE) -c
GPU_COMPILE_OBJ= $(GPU_COMPILE) -c

EXT_DIR = /home/users/panastas/Diploma/Git-master/Benchmarks/Scripts/Ext_lib/

SOURCE = main-cuSPARSE.cu 
OBJECTS = alloc.o dmv.o timer.o input.o gpu_util.o
PROGRAMS= cuSPARSE

all: $(PROGRAMS)

cuSPARSE: $(OBJECTS) $(SOURCE)
	$(GPU_COMPILE) -o $@ $(OBJECTS) $(LDFLAGS) main-cuSPARSE.cu 

gpu_util.o: $(EXT_DIR)gpu_util.cu
	$(GPU_COMPILE_OBJ) -o $@ $<

input.o: $(EXT_DIR)input.cu
	$(GPU_COMPILE_OBJ) -o $@ $<

%.o: $(EXT_DIR)%.c
	$(CPU_COMPILE_OBJ) -o $@ $<

%.o: %.h

clean:
	$(RM) $(PROGRAMS) $(OBJECTS)
