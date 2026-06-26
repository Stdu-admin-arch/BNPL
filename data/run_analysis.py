import subprocess, csv, os
base_dir = os.path.expanduser('~/bnpl-project/fabric-samples/fabric-samples/test-network')
res = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
with open('/home/Teamnagid/bnpl-project/data/synthetic_transactions.csv', 'r') as f:
    reader = list(csv.DictReader(f))
    for row in reader:
        cmd = (f'peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile {base_dir}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C bnplchannel -n bnpl --peerAddresses localhost:7051 --tlsRootCertFiles {base_dir}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles {base_dir}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c \'{{"function":"createLoan","Args":["{row['transaction_id']}","{row['customer']}","{row['amount']}"]}}\'')
        p = subprocess.run(cmd, shell=True, capture_output=True)
        act = 1 if p.returncode == 0 else 0
        exp = int(row['is_compliant'])
        if exp==1 and act==1: res['TP']+=1
        elif exp==0 and act==0: res['TN']+=1
        elif exp==1 and act==0: res['FN']+=1
        elif exp==0 and act==1: res['FP']+=1
print(f"Confusion Matrix: {res}")
