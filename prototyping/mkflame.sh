perf script | ./FlameGraph/stackcollapse-perf.pl | grep "start_simulation" | ./FlameGraph/flamegraph.pl > sstsimonly.svg
perf script | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > full.svg
