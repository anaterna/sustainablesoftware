import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_ind
import scipy.stats as stats
import itertools
import scipy.stats as stats
import scikit_posthocs as sp
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def load_and_label_data(csv_files):
    """
    Reads multiple CSV files and adds a 'Variant' column based on filename.
    
    Args:
        csv_files (list of str): List of CSV file paths.
    
    Returns:
        pd.DataFrame: Combined DataFrame with all variants.
        dict: Dictionary of DataFrames for individual variants.
    """
    dataframes = {}
    combined_data = []
    
    for file in csv_files:
        df = pd.read_csv(file)
        #variant_name = file.split(".csv")[0]  # Extract filename as variant label
        variant_name = file.replace("_output.csv", "")
        df["Variant"] = variant_name
        dataframes[variant_name] = df
        combined_data.append(df)
    
    return pd.concat(combined_data, ignore_index=True), dataframes

def plot_violin_energy(data):
    """
    Creates a Violin plot with Box plot inside it, of Energy (J) across all variants in a blue gradient.
    
    Args:
        data (pd.DataFrame): The dataset containing the energy values.
    """
    plt.figure(figsize=(10, 6))
    
    # Creating the violin plot with a blue gradient
    sns.violinplot(
        x="Variant", 
        y="Execution Time (Seconds)", 
        data=data, 
        inner="box", 
        palette="Blues"  # Blue gradient
    )
    
    # Adding title and labels
    plt.title("Execution Across Variants")
    plt.ylabel("Execution Time (Seconds)")
    plt.xticks(rotation=45)
    
    # Show the plot
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()
    
def check_normality(data):
    """
    Performs Shapiro-Wilk test for normality on Energy Consumption data for each Variant.
    
    Args:
        data (pd.DataFrame): The dataset containing 'Variant' and 'Energy Consumption (Joules)'.
    
    Returns:
        dict: p-values for each variant.
    """
    normality_results = {}

    for variant, group in data.groupby("Variant"):
        stat, p = stats.shapiro(group["Energy Consumption (Joules)"])
        normality_results[variant] = p
        print(f"Variant: {variant} | p-value: {p:.5f} {'(Normal)' if p > 0.05 else '(Not Normal)'}")

    return normality_results

def mean_difference(data, column):
    """
    Computes the absolute mean difference between the first two variants and all pairs of variants.

    Args:
        data (dict): Dictionary of DataFrames for each variant.
        column (str): The column to compare.

    Returns:
        None
    """
    variants = list(data.keys())
    if len(variants) < 2:
        return None
    
    means = {variant: data[variant][column].mean() for variant in variants}
    
    print("\nMean Difference in Energy (J):")
    for i, variant1 in enumerate(variants):
        for variant2 in variants[i+1:]:
            print(f"{variant1} vs {variant2}: {abs(means[variant1] - means[variant2]):.4f} Joules")

def percent_change(data, column):
    """
    Computes the percent change in means between the first two variants.

    Args:
        data (dict): Dictionary of DataFrames for each variant.
        column (str): The column to compare.

    Returns:
        None
    """
    variants = list(data.keys())
    if len(variants) < 2:
        return None
    
    means = {variant: data[variant][column].mean() for variant in variants}
    
    for i, variant1 in enumerate(variants):
        for variant2 in variants[i+1:]:
            percent_change = ((means[variant2] - means[variant1]) / means[variant1]) * 100 if means[variant1] != 0 else None
            print(f"Percent Change from {variant1} to {variant2}: {percent_change:.2f}%")

def perform_statistical_test(data):
    """
    Runs ANOVA if all groups are normal; otherwise, runs Kruskal-Wallis test.

    Args:
        data (pd.DataFrame): The dataset containing energy values.

    Returns:
        str: The test performed and its p-value.
    """
    normality_results = check_normality(data)
    
    if all(p > 0.05 for p in normality_results.values()):
        print("\nData is normally distributed, running ANOVA...")
        stat, p = stats.f_oneway(*[group["Energy Consumption (Joules)"] for _, group in data.groupby("Variant")])
        test_name = "ANOVA"
    else:
        print("\nData is NOT normally distributed, running Kruskal-Wallis test...")
        stat, p = stats.kruskal(*[group["Energy Consumption (Joules)"] for _, group in data.groupby("Variant")])
        test_name = "Kruskal-Wallis"

    print(f"{test_name} Test | p-value: {p} {'(Significant Differences)' if p < 0.05 else '(No Significant Differences)'}\n")
    return test_name, p


def analyze_variants(data):
    """
    Performs normality tests on each variant and applies the appropriate statistical test:
    - If both variants in a pair are normally distributed, performs Tukey's HSD test.
    - Otherwise, performs Dunn's test with Bonferroni correction.

    Args:
        data (pd.DataFrame): DataFrame with columns ["Variant", "Energy Consumption (Joules)"].

    Prints:
        - Shapiro-Wilk normality results
        - Tukey's test results for normal pairs
        - Dunn's test results for non-normal pairs
    """

    # Step 1: Check normality per variant
    normality_results = {}
    for variant, group in data.groupby("Variant"):
        values = group["Energy Consumption (Joules)"]
        if len(values) < 3:
            print(f"Skipping Shapiro-Wilk test for {variant} (only {len(values)} values).")
            normality_results[variant] = False
        else:
            try:
                stat, p_value = stats.shapiro(values)
                normality_results[variant] = p_value > 0.05
            except Exception as e:
                print(f"Error in Shapiro-Wilk test for {variant}: {e}")
                normality_results[variant] = False

    # Step 2: Categorize variant pairs
    normal_pairs = []
    non_normal_pairs = []
    
    for variant1, variant2 in itertools.combinations(normality_results.keys(), 2):
        if normality_results[variant1] and normality_results[variant2]:
            normal_pairs.append((variant1, variant2))
        else:
            non_normal_pairs.append((variant1, variant2))

     # Step 3: Run appropriate tests
    if normal_pairs:
        print("\nApplying Tukey's Test for normally distributed variant pairs...")
        normal_variants = [v for v, is_normal in normality_results.items() if is_normal]
        tukey_data = data[data["Variant"].isin(normal_variants)]
        tukey_results = pairwise_tukeyhsd(tukey_data["Energy Consumption (Joules)"], tukey_data["Variant"])
        print(tukey_results)

    if non_normal_pairs:
        print("\nApplying Dunn's Test for non-normally distributed variant pairs...")
        non_normal_variants = [v for v, is_normal in normality_results.items() if not is_normal]
        dunn_data = data[data["Variant"].isin(non_normal_variants)]
        dunn_results = sp.posthoc_dunn(data, val_col="Energy Consumption (Joules)", group_col="Variant", p_adjust="bonferroni")
        print(dunn_results)


def summarize_data(data):
    """
    Prints the mean, median, and standard deviation of Energy Consumption for each Variant.
    
    Args:
        data (pd.DataFrame): The dataset containing 'Variant' and 'Energy Consumption (Joules)'.
    """
    summary = data.groupby("Variant")["Energy Consumption (Joules)"].agg(["mean", "median", "std"])
    
    print("\n🔍 **Energy Consumption Summary (J)**")
    print(summary.to_string(float_format="%.2f"))


def cliffs_delta(x, y):
    """
    Computes Cliff's Delta, a measure of effect size for ordinal data.
    - Values near 0: Little to no effect.
    - Values near ±1: Strong effect.
    
    Returns:
        delta (float): Cliff's Delta value.
    """
    x, y = np.array(x), np.array(y)
    n_x, n_y = len(x), len(y)
    greater = sum((xi > yi) for xi in x for yi in y)
    less = sum((xi < yi) for xi in x for yi in y)
    return (greater - less) / (n_x * n_y)

def analyze_pairwise_differences(data):
    """
    Computes Cliff's Delta and mean differences for all variant pairs.
    
    Args:
        data (pd.DataFrame): DataFrame with columns ["Variant", "Energy Consumption (Joules)"].
    
    Returns:
        pd.DataFrame: Table with mean differences and Cliff's Delta for each variant pair.
    """
    results = []
    variants = data["Variant"].unique()

    for var1, var2 in itertools.combinations(variants, 2):
        group1 = data[data["Variant"] == var1]["Energy Consumption (Joules)"]
        group2 = data[data["Variant"] == var2]["Energy Consumption (Joules)"]
        
        # Compute Mean Difference
        mean_diff = group1.mean() - group2.mean()

        # Compute Cliff’s Delta
        cliff_delta = cliffs_delta(group1, group2)

        # Store Results
        results.append({"Variant 1": var1, "Variant 2": var2, 
                        "Mean Difference": mean_diff, "Cliff's Delta": cliff_delta})

    return pd.DataFrame(results)

def main():
    """
    Main function to load data, generate plots, and compute statistical tests.
    """
    csv_files = [
        "cuda_idle_output.csv",
        "python_idle_output.csv",
        "pytorch_idle_output.csv",
        "nvcr_idle_output.csv",
        "ubuntu_idle_output.csv"
    ]

    # Load and label data
    combined_data, dataframes = load_and_label_data(csv_files)

    # Generate violin plot for Energy Consumption (Joules)
    plot_violin_energy(combined_data)

    # Perform statistical tests
    print("Performing normality tests and significance statistics")
    perform_statistical_test(combined_data)

    print("Summarize Data")
    summarize_data(combined_data)

    print("Perform pair-wise significance tests")
    analyze_variants(combined_data)

    print("Compute Effect Size")
    print(analyze_pairwise_differences(combined_data))

if __name__ == "__main__":
    main()
