.PHONY: all

all: stream
	OMP_EXE=stream sst ariel_snb.py

stream:
	gcc stream.c -fopenmp -o stream

