import csv
import subprocess
import time

def replay_data(csv_file):
    results = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # We only replay a subset for speed testing (e.g., first 50)
            start_time = time.perf_counter()
            
            # Construct the invoke command
            cmd = [
                'peer', 'chaincode', 'invoke', '-o', 'localhost:7050',
                '--ordererTLSHostnameOverride', 'orderer.example.com',
                '--tls', '--cafile', 'organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem',
                '-C', 'bnplchannel', '-n', 'bnpl',
                '--peerAddresses', 'localhost:7051', '--tlsRootCertFiles', 'organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt',
                '--peerAddresses', 'localhost:9051', '--tlsRootCertFiles', 'organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt',
                '-c', f'{{"function":"createLoan","Args":["{row["tx_id"]}","{row["customer_id"]}","{row["amount"]}"]}}'
            ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                end_time = time.perf_counter()
                latency = (end_time - start_time) * 1000
                results.append({'tx_id': row['tx_id'], 'latency': latency, 'status': 'SUCCESS'})
            except subprocess.CalledProcessError:
                results.append({'tx_id': row['tx_id'], 'latency': 0, 'status': 'FAILED'})
            
            print(f"Processed {row['tx_id']} - Latency: {latency:.2f}ms")
    
    return results

if __name__ == "__main__":
    replay_data('bnpl_synthetic_data.csv')