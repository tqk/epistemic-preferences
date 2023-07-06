#!/bin/bash

# Check if the runs directory exists
if [ -d runs30 ]; then
    echo "runs30 directory exists"
    exit 1
else
    mkdir runs30
fi

python3 run.py --problem /root/PROJECT/benchmarks/corridor-doxastic/prob_1_3.pdkbddl --agents a,b,c --time 30 |& tee -a runs30/corridor_1_3.log 
python3 run.py --problem /root/PROJECT/benchmarks/corridor-doxastic/prob_1_5.pdkbddl --agents a,b,c,d,e --time 30 |& tee -a runs30/corridor_1_5.log
python3 run.py --problem /root/PROJECT/benchmarks/corridor-doxastic/prob_1_7.pdkbddl --agents a,b,c,d,e,f,g --time 30 |& tee -a runs30/corridor_1_7.log


python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-4ag-2g-1d.pdkbddl --agents a,b,c,d --time 30 |& tee -a runs30/grapevine_4ag_2g_1d.log
python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-4ag-4g-1d.pdkbddl --agents a,b,c,d --time 30 |& tee -a runs30/grapevine_4ag_4g_1d.log
python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-4ag-8g-1d.pdkbddl --agents a,b,c,d --time 30 |& tee -a runs30/grapevine_4ag_8g_1d.log
python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-8ag-2g-1d.pdkbddl --agents a,b,c,d,e,f,g,h --time 30 |& tee -a runs30/grapevine_8ag_2g_1d.log
python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-8ag-4g-1d.pdkbddl --agents a,b,c,d,e,f,g,h --time 30 |& tee -a runs30/grapevine_8ag_4g_1d.log
python3 run.py --problem /root/PROJECT/benchmarks/grapevine-doxastic/prob-8ag-8g-1d.pdkbddl --agents a,b,c,d,e,f,g,h --time 30 |& tee -a runs30/grapevine_8ag_8g_1d.log


