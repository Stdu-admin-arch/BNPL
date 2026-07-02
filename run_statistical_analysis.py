import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar

# Load your dataset
df = pd.read_csv('data/synthetic_transactions.csv')

# Calculate Prototype (act) and Baseline (base) outcomes
# Prototype: Logic <= 50,000
# Baseline: Logic always approves (but is 'wrong' on > 50,000)
proto_fp = len(df[(df['is_compliant'] == 0) & (df['amount'] <= 50000)])
proto_fn = len(df[(df['is_compliant'] == 1) & (df['amount'] > 50000)])

# Baseline (Always approves)
base_fp = len(df[df['is_compliant'] == 0])
base_fn = 0 # Baseline never rejects, so it has no False Negatives by its own definition

# Create Contingency Table for McNemar: [[TP, FP], [FN, TN]]
# We compare Prototype Errors vs Baseline Errors
table = [[proto_fp, proto_fn], [base_fp, base_fn]]

result = mcnemar(table, exact=True)
print(f"McNemar Test Result: p-value = {result.pvalue}")
print("If p < 0.05, the DLT prototype is statistically superior to the baseline.")