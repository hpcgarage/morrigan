#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

void ariel_enable() {
    printf("ARIEL-CLIENT: Library enabled.\n");
}

int main(int argc, char** argv)
{
    unsigned int magic = 1993;
    unsigned long int len;
    unsigned long int buflen = 1024*1024*256;
    long long int total = 0;
    long long int *data;

    // Read and validate input
    if (argc < 2) {
        printf("Usage: %s <len>\n", argv[0]);
        exit(1);
    }

    len = strtoul(argv[1], NULL, 0);

    if (len < 1) {
        printf("First argument must be a positive int.\n");
        exit(1);
    }

    // Seed random for reproducibility
    srand(magic);

    // Allocate and initialize data
    data = (long long int*)malloc(sizeof(long long int) * buflen);
    for (int i = 0; i < buflen; i++) {
        data[i] = i;
    }

    // Tell Ariel to begin tracing
    ariel_enable();

    #pragma omp parallel
    {
        unsigned int state = magic + omp_get_thread_num();
        long long int sum = 0;

        for (int i = 0; i < len; i++) {
            int ind = rand_r(&state) % buflen;
            sum += data[ind];
        }
        #pragma omp critical
        total += sum;
    }

    printf("Total: %lld\n", total);


}
