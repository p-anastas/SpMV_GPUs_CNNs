/*
 *  some GPU utility functions
 *  Author: Petros Anastasiadis(panastas@cslab.ece.ntua.gr) 
 */  

void gpu_free(void *gpuptr);
void cudaCheckErrors(const char * msg);
void *gpu_alloc(size_t count);
int copy_to_gpu(const void *host, void *gpu, size_t count);
int copy_from_gpu(void *host, const void *gpu, size_t count);
const char *gpu_get_errmsg(cudaError_t err);
const char *gpu_get_last_errmsg();
void gpu_memory_print();
double gpu_memory_start_count();
double gpu_memory_stop_count(double used);
