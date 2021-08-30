/*
 * Some basic functions for mtx reading and formating
 * 
 * Author: Petros Anastasiadis(panastas@cslab.ece.ntua.gr) 
 */
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "alloc.h"
#include "input.h"
#include <cuda_runtime.h>
#include <cusp/io/matrix_market.h>

int mtx_read1(int ** csrRow, int ** cooCol, double ** cooVal, int * n, int * m, int * n_z, char * name)
{
	cusp::csr_matrix<int, double, cusp::host_memory> matrix;

	// load a matrix stored in MatrixMarket format
	cusp::io::read_matrix_market_file(matrix,name);

	/*save the matrix information*/
	*n = matrix.num_rows;
	*m = matrix.num_cols;
	*n_z = matrix.num_entries;

	cudaMallocManaged(csrRow, (*n+1)*sizeof(int));
	cudaMallocManaged(cooCol, *n_z*sizeof(int));
	cudaMallocManaged(cooVal, *n_z*sizeof(double));
	cudaDeviceSynchronize();

	/*copy the elements*/
	//numBytes = (*n + 1) * sizeof(int);
	for (int i=0; i < (*n+1); i++) (*csrRow)[i] = matrix.row_offsets[i] ;
	//cudaMemcpy(csrRow, &matrix.row_offsets[0], numBytes,cudaMemcpyHostToHost);
	//CudaCheckError();

	//numBytes = *n_z * sizeof(int);
	for (int i=0; i < *n_z; i++) (*cooCol)[i] = matrix.column_indices[i] ;
	//cudaMemcpy(cooCol, &matrix.column_indices[0], numBytes,cudaMemcpyHostToHost);
	//CudaCheckError();

	//numBytes = *n_z * sizeof(double);
	for (int i=0; i < *n_z; i++) (*cooVal)[i] = matrix.values[i] ;
	//cudaMemcpy(cooVal, &matrix.values[0], numBytes,cudaMemcpyHostToHost);
	//CudaCheckError();

	return 1;
}

int mtx_read(int ** I, int ** cooCol, double ** cooVal, int * n, int * m, int * n_z, char * name)
{
	
	char c;
	char *type, *format, *var_type, *symmetry, *string=NULL;
	FILE *fp ;
	size_t len=0;
	if ((fp=fopen(name, "r"))==NULL){
		printf("Problem in read pass\n");
		exit(1);
	}
	getline(&string, &len, fp);
	strtok(string," ");
	type = strtok(NULL," ");
	format = strtok(NULL," ");
	var_type = strtok(NULL," ");
	symmetry = strtok(NULL,"\n");
	//printf("type=%s, format=%s, var_type=%s, ", type, format, var_type);
	if (strcmp(type,"matrix")){
		printf("type=%s unsupported...terminating\n\n\n\n\n\n\n\n\n\n\n\n", type);
		exit(1);
	}
	if (strcmp(format,"coordinate") ){
		printf("format=%s unsupported...terminating\n\n\n\n\n\n\n\n\n\n\n\n", format);
		exit(1);
	}
	if (strcmp(var_type,"integer") && strcmp(var_type,"real") && strcmp(var_type,"pattern")){
		printf("Var_type=%s unsupported...terminating\n\n\n\n\n\n\n\n\n\n\n\n", var_type);
		exit(1);
	}
	while((c=getc(fp))=='%') while( (c=getc(fp))!='\n') ; 
	ungetc(c, fp);
	int k, lines = 0, sym_k=0;
	fscanf(fp,"%d %d %d", n, m, &lines);
	//printf("n=%d, m=%d, lines=%d, ", *n, *m, lines);
	
	*n_z = 0;
	if (!strcmp(symmetry,"symmetric")){
		get_nz_symmetric(n_z, name);
		//printf("symmetry=symmetric\n");
	}
	else if (!strcmp(symmetry,"general")) {
		*n_z=lines;
		//printf("symmetry=general\n");
	}
	else {
		printf("Invalid symmetry value:%s\n", symmetry); 
		return 0; 
	}
	//printf("n_z=%d\n", *n_z);
	cudaMallocManaged(I, *n_z*sizeof(int));
	cudaMallocManaged(cooCol, *n_z*sizeof(int));
	cudaMallocManaged(cooVal, *n_z*sizeof(double));
	double dum;
	if ( !*I || !*cooCol || !*cooVal ) return 0;
	
	if (!strcmp(symmetry,"symmetric")){
		for (k = 0; k < lines; k++) {
			if (!strcmp(var_type,"pattern")) {
				fscanf(fp,"%d %d", &((*I)[sym_k]), &((*cooCol)[sym_k]));
				(*cooVal)[sym_k]= 1.0;	
			}
			else {	
				fscanf(fp,"%d %d %lf", &((*I)[sym_k]), &((*cooCol)[sym_k]), &dum);
			 	(*cooVal)[sym_k]=(double) dum;
			}
			(*I)[sym_k]--;
			(*cooCol)[sym_k]--;
			sym_k++;
			if ((*I)[sym_k-1] != (*cooCol)[sym_k-1]) {
				(*I)[sym_k] = (*cooCol)[sym_k-1];
				(*cooCol)[sym_k] = (*I)[sym_k-1];
				(*cooVal)[sym_k] = (*cooVal)[sym_k-1];
				sym_k++;
			}
		}
		if (sym_k!=*n_z){
			printf("Error in symmetric read: sym_k=%d n_z=%d\n", sym_k, *n_z);
			return 0;
		}
	}
	else if (!strcmp(symmetry,"general")) 
	{
		for (k = 0; k < lines; k++){
			if (!strcmp(var_type,"pattern")) {
				fscanf(fp,"%d %d", &((*I)[sym_k]), &((*cooCol)[sym_k]));
				(*cooVal)[sym_k]= 1.0;	
			}
			else {	
				fscanf(fp,"%d %d %lf", &((*I)[sym_k]), &((*cooCol)[sym_k]), &dum);
			 	(*cooVal)[sym_k]=(double) dum;
			}
			(*I)[k]--;
			(*cooCol)[k]--;
		}
	}
	quickSort( *I, *cooCol, *cooVal, 0, *n_z-1);
	fclose(fp);
	return 1;
}


void get_nz_symmetric( int * n_z, char* name)
{
	char c;
	FILE *fp ;
	if ((fp=fopen(name, "r"))==NULL){
		printf("Problem in symmetric read pass\n");
		exit(1);
	}

	while((c=getc(fp))=='%') while( (c=getc(fp))!='\n') ; 
	ungetc(c, fp);
	int k, i, j, n, m, lines;
	double x;
	fscanf(fp,"%d %d %d", &n, &m, &lines);
	for (k = 0; k < lines; k++){
		fscanf(fp,"%d %d %lf", &i, &j, &x);
		(*n_z)++;
		if(i!=j) (*n_z)++;
	}
}


	
void csr_transform(float ** A, int n, int m, int n_z, float  *csrValA, int *csrRowPtrA, int *csrColIndA)
{
	int i,j,k=0;
	for (i = 0; i < n; i++){
		csrRowPtrA[i]=k;
		for (j = 0; j < m; j++){
			if (A[i][j]!=0.0){
				csrValA[k]=A[i][j];
				csrColIndA[k]= j;
				k++;
			}
		}
	}
	csrRowPtrA[i]=k;
	if (k!=n_z) printf("Error at non zeroes: %d\n", k-n_z);
	return;
}

void quickSort( int *a, int * b, double * c, int l, int r)
{
	int j;
	if( l < r ) 
	{	// divide and conquer		
		j = partition( a, b, c, l, r);
		quickSort( a, b, c, l, j-1);
		quickSort( a, b, c, j+1, r);
	}
}



int partition( int *a, int * b, double * c, int l, int r) 
{
	int pivot, i, j, t;
	double t1;
	pivot = a[l];
	i = l; j = r+1;
		
	while(1)
	{
		do ++i; while( a[i] <= pivot && i <= r );
   		do --j; while( a[j] > pivot );
   		if( i >= j ) break;
   		t = a[i]; a[i] = a[j]; a[j] = t;
		t = b[i]; b[i] = b[j]; b[j] = t;
		t1 = c[i]; c[i] = c[j]; c[j] = t1;
   	}
   	t = a[l]; a[l] = a[j]; a[j] = t;
	t = b[l]; b[l] = b[j]; b[j] = t;
	t1 = c[l]; c[l] = c[j]; c[j] = t1;
   	return j;
}









