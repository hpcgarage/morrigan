cat perf.svg  | grep -o '<title>.*%' | cut -d' ' -f1,4 | sed 's/<title>//
