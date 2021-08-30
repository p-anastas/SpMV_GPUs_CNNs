/*
 *  dmv.h -- Declarations and definitions related to the DMV
 *           multiplication kernels.
 *
 *  Copyright (C) 2010-2012, Computing Systems Laboratory (CSLab)
 *  Copyright (C) 2010-2012, Vasileios Karakasis
 */ 

#include <stddef.h>

void vec_init(double *v, size_t n, double val);
void vec_init_rand(double *v, size_t n, double max);
void vec_init_rand_p(double *v, size_t n, size_t np, double max);
int vec_equals(const double *v1, const double *v2, size_t n, double eps);
void vec_print(const double *v, size_t n);
void dmv_csr(int * csrPtr, int *csrCol, double * csrVal, double *x, double *ys, int n);
void dmv_serial(float **a, const float *x, float *y, size_t n);


