import pandas as pd

# 1. Download the dataset directly from a public URL
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"

# 2. Load it into a Pandas DataFrame (think of this as a virtual spreadsheet)
# This specific file uses tabs to separate columns, so we tell pandas to split on '\t'
df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])

# 3. Look at the first 5 rows


# 4. Check how much data we actually have
print(f"\nTotal dataset size: {len(df)} rows")

print("\nMessage counts in our dataset:")
print(df['label'].value_counts())