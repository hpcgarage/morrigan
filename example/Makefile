.PHONY: all clean

all: stream
	OMP_EXE=./stream sst miranda.py

stream:
	gcc stream.c -fopenmp -o stream

clean:
	rm -f miranda.txt miranda.json stream statuni-miranda.csv

