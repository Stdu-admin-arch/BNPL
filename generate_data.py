import csv
import random
import uuid

def generate_synthetic_data(filename, num_records=5000):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header includes metrics for your evaluation phase
        writer.writerow(['tx_id', 'customer_id', 'amount', 'compliance_label', 'latency_ms', 'fraud_risk_flag'])
        
        for i in range(num_records):
            tx_id = str(uuid.uuid4())[:8]
            customer_id = f"CUST_{random.randint(1000, 9999)}"
            amount = random.randint(100, 5000)
            
            # Compliance Logic: > 2000 is non-compliant (Rule-based)
            compliance_label = 1 if amount > 2000 else 0
            
            # Simulated Latency: 50ms to 300ms
            latency = random.randint(50, 300)
            
            # Fraud Risk: 5% chance of being flagged as high risk
            fraud_risk = 1 if random.random() < 0.05 else 0
            
            writer.writerow([tx_id, customer_id, amount, compliance_label, latency, fraud_risk])

    print(f"Successfully generated {num_records} synthetic transactions in {filename}")

if __name__ == "__main__":
    generate_synthetic_data('bnpl_synthetic_data.csv')