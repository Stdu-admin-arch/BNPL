import csv, random
with open('/home/Teamnagid/bnpl-project/data/synthetic_transactions.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['transaction_id', 'customer', 'amount', 'is_compliant'])
    for i in range(1, 5001):
        amt = random.randint(100, 100000)
        writer.writerow([f'TXN{i:04d}', f'Customer{i}', amt, 1 if amt <= 50000 else 0])
