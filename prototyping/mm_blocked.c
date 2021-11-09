#include <stdlib.h>
#include <stdio.h>
#include <lapacke.h>

typedef double dtype;

void fill(dtype *a, int N, double f) {
    for (int i = 0; i < N*N; i++) {
        a[i] = f;
    }
}

int main(int argc, char** argv) {

    dtype *a, *b, *c, temp = 0;
    int N, s;

    if (argc < 3) {
        printf("Too few arguments.\n");
        exit(1);
    }

    N = atoi(argv[1]);
    s = atoi(argv[2]);

    if ( s > N || (N % s != 0)) {
        printf("Invalid arguments\n");
        exit(1);
    }


    a = (dtype*)malloc(sizeof(dtype) * N * N);
    b = (dtype*)malloc(sizeof(dtype) * N * N);
    c = (dtype*)malloc(sizeof(dtype) * N * N);

    fill(a, N, 3);
    fill(b, N, 2);

    for(int jj=0;jj<N;jj+= s){
        for(int kk=0;kk<N;kk+= s){
            for(int i=0;i<N;i++){
#pragma omp parallel for
                for(int j = jj; j<((jj+s)>N?N:(jj+s)); j++){
                    temp = 0;
                    for(int k = kk; k<((kk+s)>N?N:(kk+s)); k++){
                        temp += a[i*N + k]*b[k*N + j];
                    }
                    c[i*N + j] += temp;
                }
            }
        }
    }

}
