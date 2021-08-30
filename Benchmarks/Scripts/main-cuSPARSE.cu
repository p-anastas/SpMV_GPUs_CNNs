/*
 * A front-end SparseMatrix-Vector(SMV) multiplication implementation
 * 
 * Author: Petros Anastasiadis(panastas@cslab.ece.ntua.gr) 
 */
#include <stdlib.h>
#include <stdio.h>
#include <cuda.h>
#include <string.h>
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <cusparse_v2.h>
#include "Ext_lib/alloc.h"
#include "Ext_lib/dmv.h"
#include "Ext_lib/gpu_util.h"
#include "Ext_lib/timer.h"
#include "Ext_lib/input.h"
#include <cuda_profiler_api.h>
#include <time.h>
#include <stdint.h>
#include <inttypes.h>

#define NR_ITER 100



double csecond(void) {

    struct timespec tms;

    if (clock_gettime(CLOCK_REALTIME,&tms)) {
        return (0.0);
    }
    /* seconds, multiplied with 1 million */
    int64_t micros = tms.tv_sec * 1000000;
    /* Add full microseconds */
    micros += tms.tv_nsec/1000;
    /* round up if necessary */
    if (tms.tv_nsec % 1000 >= 500) {
        ++micros;
    }
    return( (double) micros /1000000.0) ;
}

static void check_result(double *test, double *orig, size_t n)
{
	size_t  i_fail = vec_equals(test, orig, n, 0.0001);
	if (!i_fail) printf("Checked, ");
	else printf("FAILED %ld times", i_fail );
}

static void report_results(double timer, int flops, int bytes)
{
	double time = timer/NR_ITER;
	double Gflops = flops/(time*1.e9);
	double Gbytes = bytes/(time*1.e9);
	printf("%lf ms ( %lf Gflops/s %lf Gbytes/s)\n",1000.0*time, Gflops, Gbytes);
}

static void error(const char * msg)
{
	printf("Error: %s\n", msg);
	exit(1);
}

int main(int argc, char **argv)
{
	/* Initializations */
	double alf=1.0;
	double beta=0;
	int n,m, n_z, /* *csrRowPtrA, */ *cooCol, *csrRowPtrA;
	double *cooVal, *x, *y;
	cusparseHandle_t handle1;
    cusparseCreate(&handle1);
	cusparseMatDescr_t descA;
	cusparseCreateMatDescr(&descA);
	cusparseSetMatType(descA,CUSPARSE_MATRIX_TYPE_GENERAL);
    cusparseSetMatIndexBase(descA,CUSPARSE_INDEX_BASE_ZERO); 
	double timer;

	/* File Input to COO */
	if (argc < 2) error("Too few Arguments");
	char * name = argv[1];
	FILE *fp;
	if ((fp = fopen(name, "r"))==NULL || (strstr(name, "mtx"))==NULL) error("Invalid File");
	fclose(fp);
	//printf("Serial-CSR version:File=%s, ", name);
	//if(!mtx_read(&csrRowPtrA, &cooCol, &cooVal, &n, &m, &n_z, name)) error("input and/or COO convertion failed");
	if(!mtx_read1(&csrRowPtrA, &cooCol, &cooVal, &n, &m, &n_z, name)) error("input and/or COO convertion failed");		
	
	/* Allocate unified space */	
	//cudaMallocManaged(&csrRowPtrA, (n+1)*sizeof(*csrRowPtrA));
	cudaMallocManaged(&x, m*sizeof(*x));
	double * y_serial = (double*) calloc(n, sizeof(*y_serial));
	cudaMallocManaged(&y, n*sizeof(*y));
	if (!csrRowPtrA || !x || !y || !y_serial) error("Vector Alloc failed");
	cudaDeviceSynchronize();
	/* Initialize vectors */
	vec_init_rand(x, m, 1.0);
	vec_init(y_serial, n, 0.0);
	vec_init(y, n, 0.0);

	// Bytes per spmv 
	size_t bytes = 0;
    bytes += 2*sizeof(int) * n;     // row pointer
    bytes += 1*sizeof(int) * n_z;  // column index
    bytes += 2*sizeof(double) * n_z;  // A[i,j] and x[j]
    bytes += 2*sizeof(double) * n;     // y[i] = y[i] + ...

	//FLOPS
	int flops = 2 * n_z ;
	
	/*
	printf("csrRowPtrA=\n");
	for (int i = 0; i < n_z; i++) printf("%d ", csrRowPtrA[i]);
	printf("\ncooCol=\n");
	for (int i = 0; i < n_z; i++) printf("%d ", cooCol[i]);
	printf("\ncooVal=\n");
	for (int i = 0; i < n_z; i++) printf("%lf ", cooVal[i]);
	printf("\nx=\n");
	for(int j = 0 ; j < m ; j++) printf("%lf ",x[j]);
	printf("\n");
	*/
	
	/*
	// Warmup!!! 
	cusparseXcoo2csr(handle1, csrRowPtrA, n_z, n, csrRowPtrA, CUSPARSE_INDEX_BASE_ZERO);
	cudaDeviceSynchronize();	
	cudaCheckErrors("cusparseXcoo2csr warmup fail");	

	printf("n=%d, m=%d, n_z=%d, ", n, m, n_z);
	
	// Transform to CSR 
	timer = csecond();
	cusparseXcoo2csr(handle1, csrRowPtrA, n_z, n, csrRowPtrA, CUSPARSE_INDEX_BASE_ZERO);
	cudaDeviceSynchronize();	
	timer = csecond() - timer;
	cudaCheckErrors("cusparseXcoo2csr fail");
	printf("transform time= %lf ms, ", 1000.0*timer);
	*/

	/*
	// Execute serial CSR 
	timer = csecond();
	for (size_t i = 0; i < NR_ITER; ++i) dmv_csr(csrRowPtrA, cooCol, cooVal, x, y_serial, n);
	timer = csecond() - timer;
	report_results(timer);
	*/

	
	
	
	printf("File=%s, n=%d, m=%d, n_z=%d\nCuSPARCE-CSR : ",name, n, m, n_z);
		
	// Warmup!!! 
	cusparseDcsrmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, n, m, n_z, &alf, descA, cooVal, csrRowPtrA, cooCol, x, &beta, y);
	cudaDeviceSynchronize();	
	cudaCheckErrors("cusparseDcsrmv warmup fail");	

	// Kernel launch NR_ITER times 
	timer = csecond();
	//cudaProfilerStart();
    for (size_t i = 0; i < NR_ITER; ++i) 
		cusparseDcsrmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, n, m, n_z, &alf, descA, cooVal, csrRowPtrA, cooCol, x, &beta, y);	
	cudaDeviceSynchronize();	
    
	//cudaProfilerStop();
   	timer = csecond() - timer;
	cudaCheckErrors("cusparseDcsrmv fail");	

	report_results(timer,flops,bytes);
	
	
	// Hybrid SpMv 
	
	cusparseHybMat_t hybA;
	timer = csecond();
	cusparseCreateHybMat(&hybA);
	// cuSPARSE create Hyb descriptor for A 
	cusparseDcsr2hyb(handle1, n, m, descA, cooVal, csrRowPtrA, cooCol, hybA, 0, CUSPARSE_HYB_PARTITION_AUTO);
	timer = csecond() - timer;
	cudaCheckErrors("cusparseDcsr2hyb fail");	
	printf("CuSPARCE-CSR to HYB : %lf ms\n", 1000.0*timer);
	printf("CuSPARCE-Hybrid : ");
	// Warmup!!! 
	cusparseDhybmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, &alf, descA, hybA, x, &beta, y);
	cudaDeviceSynchronize();	
	cudaCheckErrors("cusparseDhybmv warmup fail");


	// Kernel launch NR_ITER times 
	timer = csecond();
	//cudaProfilerStart();
    for (size_t i = 0; i < NR_ITER; ++i) 
		cusparseDhybmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, &alf, descA, hybA, x, &beta, y);
	cudaDeviceSynchronize();	
    
	//cudaProfilerStop();
   	timer = csecond() - timer;
	cudaCheckErrors("cusparseDhybrmv fail");	

	report_results(timer,flops,bytes);
	

	/* Sort cooCol */ /*
	size_t pBufferSizeInBytes = 0;
	cusparseXcsrsort_bufferSizeExt(handle1, n, m, n_z, gpu_csrRowPtrA, gpu_cooCol, &pBufferSizeInBytes); 
	void *pBuffer = (void *) gpu_alloc(sizeof(char)* pBufferSizeInBytes); 
	int *P		  = (int *)  gpu_alloc(sizeof(int)*n_z); 
	cusparseCreateIdentityPermutation(handle1, n_z, P);
	cudaDeviceSynchronize();
	cusparseXcsrsort(handle1, n, m, n_z, descA, gpu_csrRowPtrA, gpu_cooCol, P, pBuffer); 
	cudaDeviceSynchronize();
	double *gpu_cooVal_S = (double *) gpu_alloc(n_z*sizeof(*gpu_cooVal_S));
	cusparseDgthr(handle1, n_z, gpu_cooVal, gpu_cooVal_S, P, CUSPARSE_INDEX_BASE_ZERO);
	cudaDeviceSynchronize();
	cudaCheckErrors("csr sort fail");
	gpu_free(pBuffer);
	gpu_free(P);

	
	copy_from_gpu(cooCol, gpu_cooCol, n_z*sizeof(*cooCol));
	copy_from_gpu(cooVal, gpu_cooVal_S, n_z*sizeof(*cooVal));
	printf("cooCol=\n");
	for (int i = 0; i < n_z; i++) printf("%d ", cooCol[i]);
	printf("\ncooVal(S)=\n");
	for (int i = 0; i < n_z; i++) printf("%lf ", cooVal[i]);
	printf("\n");
	

	printf("CuSPARCE-CSR-Sorted version:File=%s, n=%d, m=%d, n_z=%d, ",name, n, m, n_z);

	// Warmpup 
	cusparseDcsrmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, n, m, n_z, &alf, descA, gpu_cooVal_S, gpu_csrRowPtrA, gpu_cooCol, gpu_x, &beta, gpu_y);	
	cudaDeviceSynchronize();
	cudaCheckErrors("cusparseDcsrmv sorted fail");		
	
	// Kernel launch NR_ITER times 
	timer = csecond();
    for (size_t i = 0; i < NR_ITER; ++i) {
		cusparseDcsrmv(handle1, CUSPARSE_OPERATION_NON_TRANSPOSE, n, m, n_z, &alf, descA, gpu_cooVal_S, gpu_csrRowPtrA, gpu_cooCol, gpu_x, &beta, gpu_y);	
		cudaDeviceSynchronize();	
    }
   	timer = csecond() - timer;
	cudaCheckErrors("cusparseDcsrmv sorted fail");	

    // Copy result back to host 
	copy_from_gpu(y, gpu_y, n*sizeof(*y));
	check_result(y, y_serial, n);
	report_results(timer);
	
	
/*
	
	// BSR Initializations
	int nnzb = 0, mb, nb, blockdim;
	cusparseMatDescr_t descB;
	cusparseCreateMatDescr(&descB);
	cusparseSetMatType(descB,CUSPARSE_MATRIX_TYPE_GENERAL);
    cusparseSetMatIndexBase(descB,CUSPARSE_INDEX_BASE_ZERO);
	cusparseDirection_t dir = CUSPARSE_DIRECTION_ROW; 

	// BSR blockdim 
	for ( blockdim=3; blockdim < 5; blockdim++ ) {
	nb = (n + blockdim-1)/blockdim; 
	mb = (m + blockdim-1)/blockdim; 
	int *gpu_bsrRowPtr  = (int *) 	 gpu_alloc((nb+1)*sizeof(*gpu_bsrRowPtr));
		
	

	timer = csecond();
	// Get nnzb 
	cusparseXcsr2bsrNnz(handle1, dir, n, m, descA, csrRowPtrA, cooCol, blockdim, descB, gpu_bsrRowPtr, &nnzb); 
	cudaDeviceSynchronize();	
	int 	*gpu_bsrCol = (int *) 	 gpu_alloc(nnzb*sizeof(*gpu_bsrCol));
	double  *gpu_bsrVal = (double *) gpu_alloc((blockdim*blockdim)*nnzb*sizeof(*gpu_bsrVal));

	cusparseDcsr2bsr(handle1, dir, n, m, descA, cooVal, csrRowPtrA, cooCol, blockdim, descB, gpu_bsrVal, gpu_bsrRowPtr, gpu_bsrCol); 
	cudaDeviceSynchronize();
	timer = csecond() - timer;
	cudaCheckErrors("cusparseXcsr2bsrNnz/cusparseDcsr2bsr fail");
	
	printf("CuSPARCE-CSR to BSR (BlockDim= %d ): %lf ms\n",blockdim, 1000.0*timer);

	// Final allocations/copies 
	double *xp, *yp;
	cudaMallocManaged(&xp, mb * blockdim * sizeof(*xp));
	cudaMallocManaged(&yp, nb * blockdim * sizeof(*yp));
	if (!xp || !yp ) error("Unified Alloc failed for bsr");

	vec_init_rand_p(xp, m, mb*blockdim, 1.0);

	printf("CuSPARCE-BSR version(dir=row, BlockDim= %d ): ", blockdim);

	// Warmup 
	cusparseDbsrmv(handle1, dir, CUSPARSE_OPERATION_NON_TRANSPOSE, nb, mb, nnzb, &alf, descB, gpu_bsrVal, gpu_bsrRowPtr, gpu_bsrCol, blockdim, xp, &beta, yp);
	cudaDeviceSynchronize();
	cudaCheckErrors("cusparseDbsrmv fail");
	
	// Kernel launch NR_ITER times 
	timer = csecond();
	for (size_t i = 0; i < NR_ITER; ++i) 
		cusparseDbsrmv(handle1, dir, CUSPARSE_OPERATION_NON_TRANSPOSE, nb, mb, nnzb, &alf, descB, gpu_bsrVal, gpu_bsrRowPtr, gpu_bsrCol, blockdim, xp, &beta, yp);
	cudaDeviceSynchronize();
	timer = csecond() - timer;
	cudaCheckErrors("cusparseDbsrmv fail");
	report_results(timer,flops,bytes);
	
	gpu_free(gpu_bsrRowPtr);
	gpu_free(gpu_bsrCol);
	gpu_free(gpu_bsrVal);
	gpu_free(yp);
	gpu_free(xp);	

	}
	
	*/

	/* Free resources on unified memory */
	gpu_free(x);
	gpu_free(y);
	gpu_free(y_serial);
	//gpu_free(csrRowPtrA);
	gpu_free(cooCol);
	gpu_free(cooVal);
	gpu_free(csrRowPtrA);

    return 0;
}


