import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, ttest_ind

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
        variant_name = file.split(".csv")[0]  # Extract filename as variant label
        df["Variant"] = variant_name
        dataframes[variant_name] = df
        combined_data.append(df)
    
    return pd.concat(combined_data, ignore_index=True), dataframes

def plot_violin_energy(data):
    """
    Creates a Violin plot with Box plot inside it, of Energy (J) across all variants in grey color.
    
    Args:
        data (pd.DataFrame): The dataset containing the energy values.
    """
    plt.figure(figsize=(10, 6))
    
    # Creating the violin plot with box plot inside it
    sns.violinplot(x="Variant", y="Energy (J)", data=data, inner="box", palette="gray")
    
    # Adding title and labels
    plt.title("Energy Consumption Across Variants")
    plt.ylabel("Energy (J)")
    plt.xticks(rotation=45)
    
    # Show the plot
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()
    
def shapiro_wilk_test(data, column):
    """
    Performs the Shapiro-Wilk test for normality on a given dataset.
    
    Args:
        data (pd.DataFrame): The dataset to test.
        column (str): The column to test.
    
    Returns:
        dict: Dictionary of p-values for each variant.
    """
    results = {}
    for variant, df in data.items():
        _, p_value = shapiro(df[column])
        results[variant] = p_value
    return results

def student_t_test(data, column):
    """
    Performs an independent Student's t-test between the first two variants.

    Args:
        data (dict): Dictionary of DataFrames for each variant.
        column (str): The column to compare.

    Returns:
        float: p-value of the t-test.
    """
    variants = list(data.keys())
    if len(variants) < 2:
        return None  # Need at least two variants to compare
    
    _, p_value = ttest_ind(data[variants[0]][column], data[variants[1]][column], equal_var=False)
    return p_value

def mean_difference(data, column):
    """
    Computes the absolute mean difference between the first two variants.

    Args:
        data (dict): Dictionary of DataFrames for each variant.
        column (str): The column to compare.

    Returns:
        float: Absolute mean difference.
    """
    variants = list(data.keys())
    if len(variants) < 2:
        return None
    
    mean_1 = data[variants[0]][column].mean()
    mean_2 = data[variants[1]][column].mean()
    mean_3 = data[variants[3]][column].mean()
    
    print("\nMean Difference in Energy (J):")
    print("First and second: ")
    print(abs(mean_1 - mean_2))

    print("First and thirf: ")
    print(abs(mean_1 - mean_3))

    print("Second and third: ")
    print(abs(mean_2 - mean_3))

def percent_change(data, column):
    """
    Computes the percent change in means between the first two variants.

    Args:
        data (dict): Dictionary of DataFrames for each variant.
        column (str): The column to compare.

    Returns:
        float: Percent change.
    """
    variants = list(data.keys())
    if len(variants) < 2:
        return None
    
    mean_1 = data[variants[0]][column].mean()
    mean_2 = data[variants[1]][column].mean()
    
    return ((mean_2 - mean_1) / mean_1) * 100 if mean_1 != 0 else None

def main():
    """
    Main function to load data, generate plots, and compute statistical tests.
    """
    csv_files = [
        "test.csv",
        "test1.csv",
    ]

    # Load and label data
    combined_data, dataframes = load_and_label_data(csv_files)

    # Generate violin plot for Energy (J)
    plot_violin_energy(combined_data)

    # Perform statistical tests
    print("\nShapiro-Wilk Test for Normality (p-values):")
    print(shapiro_wilk_test(dataframes, "Energy (J)"))

    print("\nStudent's t-test (p-value) for Energy:")
    print(student_t_test(dataframes, "Energy (J)"))

    mean_difference(dataframes, "Energy (J)")

    print("\nPercent Change in Energy (J):")
    print(percent_change(dataframes, "Energy (J)"))

if __name__ == "__main__":
    main()
