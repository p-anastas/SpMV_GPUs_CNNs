/*
 * Helpfull functions for SpMV multiplication
 * 
 * Author: Petros Anastasiadis(panastas@cslab.ece.ntua.gr) 
 */
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "dmv.h"

void dmv_serial(float **a, const float *x, float *y,
                size_t n)
{
    size_t  i, j;
    for (i = 0; i < n; ++i) {
        register float    _yi = 0;
        for (j = 0; j < n; ++j) {
            _yi += a[i][j]*x[j];
        }

        y[i] = _yi;
    }
}


void dmv_csr(int * csrPtr, int *csrCol, double * csrVal, double *x, double *ys, int n)
{
	int  i, j;
	for (i = 0; i < n; ++i) {
        	double yi = 0;
        	for (j = csrPtr[i]; j < csrPtr[i + 1]; j++) yi += csrVal[j] * x[csrCol[j]];
        	ys[i] = yi;
    	}
}

int vec_equals(const double *v1, const double *v2, size_t n, double eps)
{
	size_t  i,k=0;
    	for (i = 0; i < n; ++i) {
		if (fabs(v1[i] - v2[i]) > eps) k++;	
    	}
	return k;
}

void vec_init(double *v, size_t n, double val)
{
    size_t  i;
    for (i = 0; i < n; ++i) {
        v[i] = val;
    }
}

void vec_init_rand(double *v, size_t n, double max)
{
    srand48(42);   // should only be called once
    size_t  i;
    for (i = 0; i < n; ++i) {
        v[i] = (double) drand48();
    }
}

void vec_init_rand_p(double *v, size_t n, size_t np, double max)
{
    srand48(42);   // should only be called once
    size_t  i;
    for (i = 0; i < n; ++i) {
        v[i] = (double) drand48();
    }
	for (i = n; i < np; ++i) {
        v[i] = 0.0;
    }
}


void vec_print(const double *v, size_t n)
{
    size_t  i;
    for (i = 0; i < n; ++i)
        printf("%f\n", v[i]);
}
