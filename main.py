import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("student_data.csv")

# Display dataset
print("\nSTUDENT PERFORMANCE DATA")
print(df)

# Dataset information
print("\nDATASET INFORMATION")
print(df.info())

# Check missing values
print("\nMISSING VALUES")
print(df.isnull().sum())

# Calculate average marks
subjects = ["Maths", "Science", "English", "Computer"]
df["Average"] = df[subjects].mean(axis=1)

# Display top performer
topper = df.loc[df["Average"].idxmax()]

print("\nTOP PERFORMER")
print(topper["Student"])
print("Average:", round(topper["Average"], 2))

# Subject-wise average
print("\nSUBJECT-WISE AVERAGE")
print(df[subjects].mean())

# Create visualization
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x="Student", y="Average")

plt.title("Student Performance Analysis")
plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()