# Energy Consumption Measurement for Docker Containers

This project measures the energy consumption of various Docker base images using EnergyBridge for ResNet-50 ML workload. The experiment runs multiple iterations, warms up the system, and logs energy data for each run.


## Requirements

- Docker: The project assumes that Docker images are available and can be run via Docker commands.

- EnergyBridge: Used for measuring energy consumption, make sure it is installed in the correct directory (./energy_measurement/energibridge_folder/energibridge).

- Python 3.x: Required to run the experiment script.

- Linux OS (but can be configured also to Windows)

## Installation

1. Clone the repository or download the script.
2. Ensure that EnergyBridge is installed and accessible from the path specified in the script (./energy_measurement/energibridge_folder/energibridge).
3. Install the required Python packages: `pip install -r requirements.txt`

## Usage

To run the energy consumption measurements, execute the following command: from `project2/` folder, run: `python ./energy_measurement/measure_linux.py`


## Script Details

The script performs the following:

1. **Warm-up Phase**: A Fibonacci sequence calculation is used to warm up the system.
2. **Measurement Phase**: Energy consumption is measured for a given Docker container image. The command for each image is provided and executed within the Docker container.
3. **Result Parsing**: The script parses the output of the experiment and extracts energy consumption and execution time.
4. **Logging**: The results of each run are saved into a `.csv` file for further analysis.

### Available Docker Images

The following Docker images are tested for energy consumption:

- `ubuntu`
- `pytorch-base`
- `python-base`
- `cuda-base`
- `nvcr`

Each image will be run one by one, and measurements will be taken for each image.

### Example Command

For 50 runs, with a 30-second warm-up and a 20-second pause between runs:

```bash
python energy_measurement.py --runs 50 --warmup 30 --pause 20

```


## Docker Images and Workload

In the `docker_workload` file, you can find all the configured docker images that we used for this experiment and are supported for later experiments as well as the ML workload used, specifically ResNet-50 inference workload, which is found in the `benchmark.py`. 

## Visualizations


This script located at `project2/visualizations/analyze.py` performs energy consumption analysis using data from multiple CSV files. It processes the data, generates statistical tests, and visualizes the results. The primary focus is on analyzing energy consumption across different variants (e.g., Docker images).

### Key Functions

1. **load_and_label_data**: Loads multiple CSV files and labels them with a 'Variant' column based on the filename.
2. **plot_violin_energy**: Generates a violin plot with a box plot inside, showing the energy consumption distribution across variants.
3. **check_normality**: Performs the Shapiro-Wilk normality test on the energy consumption data for each variant.
4. **mean_difference**: Computes the absolute mean difference between energy consumption values for all pairs of variants.
5. **percent_change**: Calculates the percent change in mean energy consumption between pairs of variants.
6. **perform_statistical_test**: Conducts an ANOVA or Kruskal-Wallis test to determine if there are significant differences in energy consumption across variants.
7. **analyze_variants**: Applies Tukey's HSD test for normally distributed pairs and Dunn's test for non-normal pairs, along with printing normality test results.
8. **summarize_data**: Summarizes the mean, median, and standard deviation of energy consumption for each variant.
9. **cliffs_delta**: Computes Cliff's Delta, a measure of effect size for ordinal data.
10. **analyze_pairwise_differences**: Computes the mean difference and Cliff's Delta for all pairwise comparisons of variants.

### Example Usage

1. The script will load the following CSV files containing energy consumption data:
    - `cuda-base_output.csv`
    - `python-base_output.csv`
    - `pytorch-base_output.csv`
    - `nvcr-base_output.csv`
    - `ubuntu-base_output.csv`

2. The script performs the following analyses:
   - **Normality tests** for each variant.
   - **ANOVA or Kruskal-Wallis test** for significance.
   - **Tukey’s HSD or Dunn’s test** for pairwise comparison of variants.
   - **Effect size** calculation using Cliff’s Delta.



