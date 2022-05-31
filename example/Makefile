.PHONY: all clean

all: stream
	OMP_EXE=./stream sst mirandams1.py

stream:
	gcc stream.c -fopenmp -o stream

clean:
	rm -f miranda.txt miranda.json stream stats-miranda.csv

