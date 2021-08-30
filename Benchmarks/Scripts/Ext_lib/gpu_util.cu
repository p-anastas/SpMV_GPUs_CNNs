/*
 *  Some GPU utility functions for SpMV multiplication
 *  Author: Petros Anastasiadis(panastas@cslab.ece.ntua.gr) 
 */ 

#include <cuda.h>
#include <stdio.h>
#include <cuda_runtime.h>
#include "gpu_util.h"

const char *gpu_get_errmsg(cudaError_t err)
{
    return cudaGetErrorString(err);
}

const char *gpu_get_last_errmsg()
{
    return gpu_get_errmsg(cudaGetLastError());
}

void cudaCheckErrors(const char * msg)
{
        cudaError_t __err = cudaGetLastError();
        if (__err != cudaSuccess) { 
            printf("\nFatal error: %s (%s)\n", msg, cudaGetErrorString(__err));
            exit(1); 
        }
}

void *gpu_alloc(size_t count)
{
	void *ret;
	if (cudaMalloc(&ret, count) != cudaSuccess) {
		printf("Gpu alloc failed: %s\n", gpu_get_last_errmsg());
		exit(1);
	}
	return ret;
}

void gpu_free(void *gpuptr)
{
    cudaFree(gpuptr);
}

int copy_to_gpu(const void *host, void *gpu, size_t count)
{
	if (cudaMemcpy(gpu, host, count, cudaMemcpyHostToDevice) != cudaSuccess){
		printf("Copy to GPU failed: %s\n", gpu_get_last_errmsg());
		exit(1);
	}   
	return 1;
}

int copy_from_gpu(void *host, const void *gpu, size_t count)
{
	if (cudaMemcpy(host, gpu, count, cudaMemcpyDeviceToHost) != cudaSuccess){
		printf("Copy to Host failed: %s\n", gpu_get_last_errmsg());
		exit(1);
	}   
	return 1;
}
double gpu_memory_start_count()
{
	size_t free_byte ;
        size_t total_byte ;

        cudaMemGetInfo( &free_byte, &total_byte ) ;
	double free_db = (double)free_byte ;
	double total_db = (double)total_byte ;
	double used_db = total_db - free_db ;
	return used_db/1024.0/1024.0;
}


double gpu_memory_stop_count(double used)
{
	size_t free_byte ;
        size_t total_byte ;

	cudaMemGetInfo( &free_byte, &total_byte ) ;
	double free_db = (double)free_byte ;
	double total_db = (double)total_byte ;
	double used_db = total_db - free_db ;
	return used_db/1024.0/1024.0 - used;
}


void gpu_memory_print()
{
	size_t free_byte ;
        size_t total_byte ;
	cudaError_t cuda_status;

        cuda_status = cudaMemGetInfo( &free_byte, &total_byte ) ;
        if ( cudaSuccess != cuda_status ){
		printf("Error: cudaMemGetInfo fails, %s \n", cudaGetErrorString(cuda_status) );
		exit(1);
	}
	double free_db = (double)free_byte ;
	double total_db = (double)total_byte ;
	double used_db = total_db - free_db ;

        printf("GPU memory usage: used = %lf, free = %lf MB, total = %lf MB\n", used_db/1024.0/1024.0, free_db/1024.0/1024.0, total_db/1024.0/1024.0);
}




