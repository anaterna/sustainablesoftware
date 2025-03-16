#!/bin/zsh

METHOD="energibridge"
FRAMEWORK="$1"

python warm_up.py

mkdir -p logs
mkdir -p results
LOG_FILE="logs/power_monitoring_results_$(date +%Y%m%d_%H%M%S).log"
SIMULATOR_LOG="${METHOD}_logs/${FRAMEWORK}_load_simulator_$(date +%Y%m%d_%H%M%S).log"
RESULTS_FILE="${METHOD}_results/results_${FRAMEWORK}_$(date +%Y%m%d_%H%M%S).out"

for i in {1..30}; do
    echo "Iteration $i: Running powermetrics..." 
    echo "Timestamp: $(date)" | tee -a "$LOG_FILE"
    
    if [ "$FRAMEWORK" = "spring" ]; then
        echo "Building ${FRAMEWORK} app"
        sudo python power_metrics.py "${METHOD}" "python -W ignore ../load_simulator/SB_Simulator.py sb-app 20" 60 "${RESULTS_FILE}" >> "$LOG_FILE" &
    elif [ "$FRAMEWORK" = "dropwizard" ]; then
        echo "Building ${FRAMEWORK} app"
        sudo python power_metrics.py "${METHOD}" "~/Library/Java/JavaVirtualMachines/openjdk-21/Contents/Home/bin/java -jar ../dropwizard-app/target/dropwizard-app-1.0.jar server ../dropwizard-app/config.yml" 60 "${RESULTS_FILE}" >> "$LOG_FILE" &
    else
        echo "Error: Unsupported framework. Choose 'spring' or 'dropwizard'."
        exit 1
    fi   
    echo "Build finished"

    sleep 3
    #python -W ignore ../load_simulator/SB_Simulator.py 20 >> "$SIMULATOR_LOG"
    wait
    
    echo "Iteration $i completed." | tee -a "$LOG_FILE"

    #Killing process
    PID=$(ps aux | grep 'mvn spring-boot:run' | grep -v grep | awk '{print $2}')

    if [ -n "$PID" ]; then
        echo "Killing Spring Boot process with PID: $PID"
        kill -9 $PID
    else
        echo "No Spring Boot process found."
    fi

    echo "Pausing for 1 minute after iteration $i..." | tee -a "$LOG_FILE"
    sleep 60
done
