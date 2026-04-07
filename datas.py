import pandas as pd
import numpy as np

data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
    "Subject": ["Math", "Science", "Math", "Science", "Math", "Science"],
    "Score": [85, 92, 78, 45, 88, np.nan],
    "Passed": [True, True, False, False, True, False]
}
df = pd.DataFrame(data)
print(df, "\n")

print(df["Score"], "\n")


print(df[["Name", "Score", "Passed"]], "\n")


passed_students = df[df["Passed"]]
print(passed_students, "\n")

df["Curved Score"] = df["Score"] + 5
print(df[["Name", "Score", "Curved Score"]], "\n")


df["Is Missing"] = df["Score"].isna()
print(df[["Name", "Score", "Is Missing"]], "\n")


df["Score"] = df["Score"].fillna(0)
print(df[["Name", "Score"]], "\n")


average_scores = df.groupby("Subject")["Score"].mean()
print(average_scores, "\n")


print(df.describe())