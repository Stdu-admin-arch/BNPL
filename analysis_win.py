import csv
from statsmodels.stats.contingency_tables import mcnemar

proto_res = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
base_res = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}

# Update this path to where your CSV is on Windows
with open('data/synthetic_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        exp = int(row['is_compliant'])
        # Prototype assumes compliance if amount <= 50000
        act = 1 if int(row['amount']) <= 50000 else 0
        
        # Metrics
        if exp==1 and act==1: proto_res['TP']+=1
        elif exp==0 and act==0: proto_res['TN']+=1
        elif exp==1 and act==0: proto_res['FN']+=1
        elif exp==0 and act==1: proto_res['FP']+=1

        # Baseline (API always approves)
        base_res['TP'] += 1 if exp == 1 else 0
        base_res['FP'] += 1 if exp == 0 else 0

print(f"Prototype: {proto_res}")
print(f"Baseline: {base_res}")

table = [[proto_res['FP'], proto_res['FN']], [base_res['FP'], base_res['FN']]]
result = mcnemar(table, exact=True)
print(f"McNemar p-value: {result.pvalue}")