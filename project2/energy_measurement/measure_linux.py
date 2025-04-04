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
        
        #print(f"Performing Fibonacci warm-up for {self.warmup_time} seconds...")
        start_time = time.time()
        while time.time() - start_time < self.warmup_time:
            fib(n)
        print("Warm-up complete.")

    def parse_results(self, run_nr):
        # Open the log file and read it in reverse
        try:
            with open(self.measurements_file, "r") as f:
                lines = f.readlines()
            
            # Reverse the lines to find the last match
            lines.reverse()
            result = None

            # Search for the last match of the pattern in the reversed lines
            for line in lines:
                match = re.search(r"Energy consumption in joules:\s*([\d.]+)\s*for\s*([\d.]+)\s*sec", line)
                if match:
                    result = match
                    break  # Once we find the last match, stop the search

            # If a match is found, extract the energy and time
            if result:
                energy = float(result.group(1))
                time_taken = float(result.group(2))
          
                # Write the results to a CSV file
                with open(self.measurements_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([run_nr, energy, time_taken])
            else:
                print("Energy and time data not found in output.")
        except FileNotFoundError:
            print(f"The file {self.measurements_file} was not found.")

    
    def run_workload(self, command, run_nr):
        """Runs a docker command and records the enrgy measurement"""
        energibridge_path = "./energy_measurement/energibridge_folder/energibridge"

        if not os.path.isfile(energibridge_path):
            raise FileNotFoundError(f"Energibridge not found at: {energibridge_path}")
        output_per_run = f"{self.results_file}_{run_nr}.csv"
        
        env = os.environ.copy()  
        env['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
        env['CUDA_VISIBLE_DEVICES'] = '0'  

        command = f"sudo -S ../../energy_measurement/energibridge_folder/energibridge -o {output_per_run} -g -i 10000 --summary {command}"
        
        with open(self.log_file, "a") as log:
            try:
                result = subprocess.run(command, shell=True, check=True, input="Florawinx1!", text=True, stdout=log, stderr=log, cwd=self.workload_dir, env=env)
                return None
            except Exception as e:
                print(f"Error running command: {e}")
                return None
        
        
    def run_measurements(self, command):
        """Runs the measurement process multiple times."""
        
        with open(self.measurements_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Run", "Energy (J)", "Time (sec)"]) 

        for run in range(self.runs):
            print(f"Run {run + 1}/{self.runs}")

            self.run_workload(command, run)
            self.parse_results(run)

            #print(f"Sleeping for {self.pause_time} seconds before next run...")

            time.sleep(self.pause_time)  # Pause before next run
            
               
        print(f"All measurements completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure energy usage of a Docker container using EnergyBridge.")
    parser.add_argument("-n", "--runs", type=int, default=30, help="Number of monitoring runs.")
    parser.add_argument("-w", "--warmup", type=int, default=60, help="Warm-up time (seconds).")
    parser.add_argument("-p", "--pause", type=int, default=60, help="Pause time between runs (seconds).")

    args = parser.parse_args()
        
    image_names = ["ubuntu", "pytorch-base", "python-base", "cuda-base"]

    for image_name in image_names:
        print(f"Image {image_name}")
        # Command for idle run
        # command_hub = f'docker run --rm luciantosa/resnet50:{image_name} /bin/bash -c "sleep 180"'
        command_hub = f"docker run luciantosa/resnet50:{image_name}"
        runs = args.runs
        
        measurement = EnergyMeasurement(image_name, runs, args.warmup, args.pause)
        measurement.fibonacci_warmup()
        measurement.run_measurements(command_hub)
        time.sleep(60) # Pause between different image runs

    # Running last image 
    command_hub = f"docker run --rm quay.io/luci_tosa11/resnet50:nvcr"
    measurement = EnergyMeasurement("nvcr", runs, args.warmup, args.pause)
    measurement.fibonacci_warmup()
    measurement.run_measurements(command_hub)