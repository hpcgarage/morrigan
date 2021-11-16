mmb: mm_blocked.c
	gcc -fopenmp -o mmb mm_blocked.c

mml: mm_lapacke.c
	gcc -fopenmp -o mml mm_lapacke.c -lopenblas #-lcblas

rand: random.c
	gcc -g -fopenmp -o rand random.c

# sudo apt-install libatlas-base-dev liblapack-dev libblas-dev liblapacke-dev libopenblas-dev libopenblas-base
