import pandas as pd
from collections import Counter

# Load the dataset
df = pd.read_excel("job_dataset_all.xlsx")  # Replace with the correct file path

# Extract the 'Salary (₹ LPA)' column
salary_column = df["Salary (₹ LPA)"]

# Count the occurrences of each salary range
salary_counts = Counter(salary_column)

# Print the count of each salary range
for salary_range, count in salary_counts.items():
    print(f"{salary_range}: {count}")