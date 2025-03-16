#!/bin/zsh

python warm_up.py

mkdir -p logs
mkdir -p results
LOG_FILE="logs/power_monitoring_results_$(date +%Y%m%d_%H%M%S).log"
SIMULATOR_LOG="logs/load_simulator_$(date +%Y%m%d_%H%M%S).log"
RESULTS_FILE="results/results_$(date +%Y%m%d_%H%M%S).out"

for i in {1..30}; do
    echo "Iteration $i: Running powermetrics..." 
    echo "Timestamp: $(date)" | tee -a "$LOG_FILE"

    # sudo python power_metrics.py "~/Library/Java/JavaVirtualMachines/openjdk-21/Contents/Home/bin/java -jar ../sb-app/target/rest-service-0.0.1-SNAPSHOT.jar" 60 "${RESULTS_FILE}" >> "$LOG_FILE" &

    # sudo python power_metrics.py "~/Library/Java/JavaVirtualMachines/openjdk-21/Contents/Home/bin/java -jar ../dropwizard-app/target/dropwizard-app-1.0.jar server ../dropwizard-app/config.yml" 60 "${RESULTS_FILE}" >> "$LOG_FILE" &

    sleep 3
    python -W ignore ../load_simulator/SB_Simulator.py 20 >> "$SIMULATOR_LOG"
    wait
    
    echo "Iteration $i completed." | tee -a "$LOG_FILE"

    echo "Pausing for 1 minute after iteration $i..." | tee -a "$LOG_FILE"
    sleep 60
done
