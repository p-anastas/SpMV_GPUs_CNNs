void get_nz_symmetric( int * n_z, char* name);
int mtx_read(int ** I, int ** cooCol, double ** cooVal, int * n, int * m, int * n_z, char * name);
int mtx_read1(int ** I, int ** cooCol, double ** cooVal, int * n, int * m, int * n_z, char * name);
void csr_transform(float **, int, int, int, float *, int *, int *);
void quickSort( int *a, int * b, double * c, int l, int r);
int partition( int *a, int * b, double * c, int l, int r);



