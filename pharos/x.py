import json
import random
import time
from web3 import Web3

# === Ağ bağlantısı ===
RPC_URL = "https://testnet.dplabs-internal.com"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
CHAIN_ID = w3.eth.chain_id

# === Cüzdan bilgileri ===
PRIVATE_KEY = "" # Private key buraya
FROM_ADDRESS = w3.to_checksum_address("cüzdan adresiniz buraya")

# === ABI yükle ===
with open("abi.json") as f:
    ABI = json.load(f)

CONTRACT_ADDRESS = w3.to_checksum_address("0xd17512b7ec12880bd94eca9d774089ff89805f02")
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# === Alıcı listesi ===
user_ids = [
    "omerbekta_s","herculesnode", "cembakan17", "mywsky", "sooneraydin", "zamazingog", "blastAway007",
    "onchainshadowx", "auto_staking", "BrokexFi", "primus_labs", "fiamma_labs", "AquaFluxPro", "KaranG09",
    "H2TEarn", "Surchmann", "DvmOnChain", "Qwertik960", "dens_club", "mrkiel_web3", "andreadeanarif",
    "crypto_ecu", "kikifar884", "SirNicco", "0xrzalc", "MavinoFriday"
]

token = {
    "tokenType": 1,
    "tokenAddress": "0x0000000000000000000000000000000000000000"
}

# === Sürekli gönderim döngüsü ===
while True:
    for user in user_ids:
        # Rastgele tutar: 0.00001 - 0.00002 PHRS
        random_amount_eth = random.uniform(0.00001, 0.00002)
        amount_wei = int(random_amount_eth * 10**18)

        recipient = {
            "idSource": "x",
            "id": user,
            "amount": amount_wei,
            "nftIds": []
        }

        try:
            nonce = w3.eth.get_transaction_count(FROM_ADDRESS)

            tx = contract.functions.tip(token, recipient).build_transaction({
                "from": FROM_ADDRESS,
                "nonce": nonce,
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
                "value": amount_wei,
                "chainId": CHAIN_ID,
            })

            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            print(f"✅ Gönderildi! Kullanıcı: {user} | Tutar: {random_amount_eth:.8f} PHRS | Tx: {w3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"❌ Hata oluştu ({user}): {e}")

        time.sleep(10)
