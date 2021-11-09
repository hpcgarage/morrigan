#include <stdlib.h>
#include <stdio.h>
#include <lapacke.h>
#include <cblas.h>

typedef double dtype;

void ariel_enable() {
	printf("ARIEL-CLIENT: Library enabled.\n");
}

void fill(dtype *a, int N, double f) {
#pragma omp parallel for
    for (int i = 0; i < N*N; i++) {
        a[i] = f;
    }
}

int main(int argc, char** argv) {

    dtype *a, *b, *c, temp = 0;
    int N, s;

    if (argc < 2) {
        printf("Too few arguments.\n");
        exit(1);
    }

    N = atoi(argv[1]);

    a = (dtype*)malloc(sizeof(dtype) * N * N);
    b = (dtype*)malloc(sizeof(dtype) * N * N);
    c = (dtype*)malloc(sizeof(dtype) * N * N);

    fill(a, N, 3);
    fill(b, N, 2);

    ariel_enable();

    cblas_dgemm ( CblasRowMajor,
                  CblasNoTrans,
                  CblasNoTrans,
                  N,
                  N,
                  N,
                  1.0,
                  a,
                  N,
                  b,
                  N,
                  0.0,
                  c,
                  N );

}
