#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

typedef double dtype;

void ariel_enable() {
    printf("ARIEL-CLIENT: Library enabled.\n");
}

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
    fill(c, N, 0);

    ariel_enable();

    int count = 0;
    for(int jj=0;jj<N;jj+= s){
        for(int kk=0;kk<N;kk+= s){
            for(int ii=0;ii<N;ii+= s){
                for(int i = ii; i<((ii+s)>N?N:(ii+s)); i++){
                    for(int j = jj; j<((jj+s)>N?N:(jj+s)); j++){
                        temp = 0;
                        for(int k = kk; k<((kk+s)>N?N:(kk+s)); k++){
                            temp += a[i*N + k]*b[k*N + j];
                            //int kk2 = count % (N/s);
                            //int jj2 = s*(count / ((N/s)*(N/s)*(s*s*s)));
                            //int kk2 = (s*(count / ((N/s)*(s*s*s))))%(N);
                            //int ii2 = (s*(count/(s*s*s)))%(N);
                            //int localcount = count % (s*s*s);
                            //int i2 = (localcount/(s*s))%s + ii;
                            //int j2 = (localcount/s)%s + jj;
                            //int k2 = localcount%s + kk;
                            //printf("-jj: %d, kk: %d, ii: %d, i: %d, j: %d, k: %d\n", jj,kk,ii,i,j,k);
                            //printf(" jj: %d, kk: %d, ii: %d, i: %d, j: %d, k: %d\n", jj2,kk2,ii2,i2,j2,k2);
                            //assert( (ii==ii2) && (jj==jj2) && (kk==kk2) && (i==i2) && (j==j2) && (k==k2));
                            //count += 1;
                        }
                        c[i*N + j] += temp;
                    }
                }
            }
        }
    }

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%.0lf ", c[i*N+j]);
        }
        printf("\n");
    }

}
