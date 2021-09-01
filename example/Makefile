.PHONY: all clean

all: stream
	OMP_EXE=stream sst ariel_snb_dramsim3.py

stream:
	gcc stream.c -fopenmp -o stream

clean:
	rm -f dramsim3.txt dramsim3.json stream stats-snb-ariel-dramsim3.csv

