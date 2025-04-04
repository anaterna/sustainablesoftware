import re
import csv

# Define the regex pattern
pattern = r"Energy consumption in joules: ([\d\.]+) for ([\d\.]+) sec of execution."

# Function to extract data from a text file and save to CSV
def extract_energy_data(input_file, output_file):
    extracted_data = []

    # Read the text file
    with open(input_file, "r", encoding="utf-8") as file:
        run = 1
        for line in file:
            match = re.search(pattern, line)
            if match:
                energy = float(match.group(1))  # Extract energy consumption
                time = float(match.group(2))    # Extract execution time
                extracted_data.append([run, energy, time])
                run += 1

    # Write to CSV
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Run", "Energy Consumption (Joules)", "Execution Time (Seconds)"])  # Header
        writer.writerows(extracted_data)

    print(f"Extraction complete. Data saved to {output_file}")


files = ['cuda_idle/energy_logs_cuda.txt', 'python_idle/energy_logs_python.txt', 'pytorch_idle/energy_logs_pytorch.txt', 'ubuntu_idle/energy_logs_ubuntu.txt', 
         'nvcr_idle/energy_logs_nvcr.txt']
folder = '../deployment/'

for file in files:
    first_path = file.split('/')[0]
    extract_energy_data(f"{folder}{file}", f"{first_path}_output.csv")
