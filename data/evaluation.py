import subprocess, csv, os, time

base_dir = os.path.expanduser('~/bnpl-project/fabric-samples/fabric-samples/test-network')
proto_res = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
base_res = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
latencies = []

with open('/home/Teamnagid/bnpl-project/data/synthetic_transactions.csv', 'r') as f:
    reader = list(csv.DictReader(f))[:20] # Limiting to 20 for video
    for row in reader:
        # Prototype Analysis
        start = time.time()
        cmd = (f'peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile {base_dir}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C bnplchannel -n bnpl --peerAddresses localhost:7051 --tlsRootCertFiles {base_dir}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles {base_dir}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c \'{{"function":"createLoan","Args":["{row['transaction_id']}","{row['customer']}","{row['amount']}"]}}\'')
        p = subprocess.run(cmd, shell=True, capture_output=True)
        latencies.append(time.time() - start)
        
        act = 1 if p.returncode == 0 else 0
        exp = int(row['is_compliant'])
        if exp==1 and act==1: proto_res['TP']+=1
        elif exp==0 and act==0: proto_res['TN']+=1
        elif exp==1 and act==0: proto_res['FN']+=1
        elif exp==0 and act==1: proto_res['FP']+=1

        # Baseline Analysis
        if int(row['amount']) <= 50000:
            base_res['TP'] += 1 if exp == 1 else 0
            base_res['FP'] += 1 if exp == 0 else 0
        else:
            base_res['FN'] += 1 if exp == 1 else 0
            base_res['TN'] += 1 if exp == 0 else 0

print(f"Prototype: {proto_res}")
print(f"Baseline: {base_res}")
print(f"Avg Latency: {sum(latencies)/len(latencies):.3f}s")
table = [[proto_res['FP'], proto_res['FN']], [base_res['FP'], base_res['FN']]]
