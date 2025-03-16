import os
import signal
import subprocess
import time
import sys

# Time interval for sampling (miliseconds)
INTERVAL = 0.1

def get_system_power():
    """ Get system-wide CPU and GPU power (in Watts) using powermetrics. """
    cmd = ["sudo", "powermetrics", "--samplers", "cpu_power", "-i", "1", "-n", "1"]
    output = subprocess.check_output(cmd, text=True)

    cpu_power = 0.0
    for line in output.split("\n"):
        if "CPU Power" in line:
            cpu_power = float(line.split(":")[1].strip().split()[0]) / 1000  # Convert mW to W

    return cpu_power

def start_background_process(command):
    try:
        # Start the process in the background
        process = subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Started process with PID {process.pid}")
        return process.pid
    except Exception as e:
        print(f"Error starting process: {e}")
        return -1

def kill_process(pid):
    print(f"Killing pid {pid}")
    os.kill(pid, signal.SIGTERM)

def estimate_energy(cpu_power, process_pid, duration):
    """ Get per-process CPU usage (%) using ps. """
    cmd = ["ps", "-eo", "pid,%cpu,comm"]

    output = subprocess.check_output(cmd, text=True)
    total_cpu_usage = 0
    process_cpu = 0
    process_name = ""

    for line in output.strip().split("\n")[1:]:
        parts = line.split(None, 2)
        if len(parts) == 3:
            pid, cpu, name = parts
            total_cpu_usage += float(cpu)
            if int(pid) == process_pid:
                process_cpu = float(cpu)
                process_name = name

    """ Estimate energy usage for each process (in Joules). """
    if total_cpu_usage == 0:
        return process_name, process_cpu

    process_power = (process_cpu / total_cpu_usage) * cpu_power if total_cpu_usage > 0 else 0
    energy = process_power * duration  # Energy (J) = Power (W) × Time (s)

    return process_name, energy

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py '<command>' <time_in_s> <results_file>")
        sys.exit(1)
    
    bash_command = sys.argv[1]
    runtime = int(sys.argv[2])
    results_file = sys.argv[3]

    print("Estimating per-process energy consumption... (Press Ctrl+C to stop)")
    total_energy = 0
    time_elapsed = 0
    pid = -1
    try:
        pid = start_background_process(bash_command)
        start_time = time.time()
        while time.time() - start_time < runtime:
            time_elapsed += INTERVAL
            cpu_power = get_system_power()
            process, energy = estimate_energy(cpu_power, pid, INTERVAL)
            total_energy += energy

            # print(f"Total energy consumed so far by {process}: {energy}J in last {INTERVAL}s")
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping...")
    
    finally:
        if pid != -1:
            kill_process(pid)
            print(f"Total energy used by {process}: {round(total_energy, 3)}J")
            f = open(results_file, "a")
            f.write(f"{round(total_energy, 3)}\n")
            f.close()

if __name__ == "__main__":
    main()
