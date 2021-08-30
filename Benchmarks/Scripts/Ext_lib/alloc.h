/*
 *  alloc.h -- 2D array allocation.
 *
 *  Copyright (C) 2010-2012, Computing Systems Laboratory (CSLab)
 *  Copyright (C) 2010-2012, Vasileios Karakasis
 */ 

void **calloc_2d(size_t n, size_t m, size_t size);
void **copy_2d(void **dst, const void **src, size_t n, size_t m, size_t size);
void free_2d(void **array);

