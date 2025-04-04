import argparse
import subprocess
import time
import os
import csv, re

class EnergyMeasurement:
    def __init__(self, workload_name, runs, warmup_time, pause_time):
        self.workload_name = workload_name
        self.workload_dir = os.path.abspath(f"./deployment/{workload_name}")
        self.runs = runs
        self.warmup_time = warmup_time
        self.pause_time = pause_time
        self.log_file = f"{self.workload_dir}/energy_logs_{self.workload_name}.txt"
        self.results_file = f"{self.workload_dir}/results/energy_results_{self.workload_name}"
        self.measurements_file = f"{self.workload_dir}/energy_measurements_{self.workload_name}.csv"
        

    def fibonacci_warmup(self, n=35):
        """Computes Fibonacci sequence for warm-up."""
        def fib(n):
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)
        
        print(f"Performing Fibonacci warm-up for {self.warmup_time} seconds...")
        start_time = time.time()
        while time.time() - start_time < self.warmup_time:
            fib(n)
        print("Warm-up complete.")

    def parse_results(self, run_nr, result):
        match = re.search(r"Energy consumption in joules:\s*([\d.]+)\s*for\s*([\d.]+)\s*sec", result)

        if match:
            energy = float(match.group(1))  # Extract energy value
            time_taken = float(match.group(2))  # Extract execution time
            print(f"Extracted Energy: {energy} J")
            print(f"Extracted Time: {time_taken} sec")
            with open(self.measurements_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([run_nr, energy, time_taken])
        else:
            print("Energy and time data not found in output.")
    
    def run_workload(self, command, run_nr):
        """Runs a docker command and records the enrgy measurement"""
        energibridge_path = "./energy_measurement/energibridge_folder/energibridge"

        if not os.path.isfile(energibridge_path):
            raise FileNotFoundError(f"Energibridge not found at: {energibridge_path}")
        output_per_run = f"{self.results_file}_{run_nr}.csv"
        command = f"../..//energy_measurement/energibridge_folder/energibridge -o {output_per_run} --summary {command}"
        
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True, cwd=self.workload_dir)
        
        with open(self.log_file, "a") as f:
            f.write(result.stdout.strip())
            f.write(result.stderr.strip())

        return result.stdout.strip()
        

    def run_measurements(self, command):
        """Runs the measurement process multiple times."""
        
        with open(self.measurements_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Run", "Energy (J)", "Time (sec)"]) 

        for run in range(self.runs):
            print(f"Run {run + 1}/{self.runs}")

            result = self.run_workload(command, run)
            self.parse_results(run, result)

            print(f"Sleeping for {self.pause_time} seconds before next run...")

            time.sleep(self.pause_time)  # Pause before next run
            
               
        print(f"All measurements completed. Logs saved in {self.log_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure energy usage of a Docker container using EnergyBridge.")
    parser.add_argument("-l", "--name", required=True, help="Workload name.")
    parser.add_argument("-n", "--runs", type=int, default=30, help="Number of monitoring runs.")
    parser.add_argument("-w", "--warmup", type=int, default=300, help="Warm-up time (seconds).")
    parser.add_argument("-p", "--pause", type=int, default=60, help="Pause time between runs (seconds).")

    args = parser.parse_args()
    measurement = EnergyMeasurement(args.name, args.runs, args.warmup, args.pause)
    command = "docker compose build"
    command_hub = f"docker run --gpus all --rm -it luciantosa/resnet50:{args.name}"
    measurement.fibonacci_warmup()
    measurement.run_measurements(command_hub)
