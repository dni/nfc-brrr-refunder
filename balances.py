import httpx
import json
import time

url = "https://legend.lnbits.com/api/v1/wallet"

with open('wallets.json') as f:
    data = json.load(f)
    balances = []
    for wallet in data:
        res = httpx.get(url, headers={"X-Api-Key": wallet.get("adminId")})
        res.raise_for_status()
        res_data = res.json()
        balances.append({
            "userId": wallet.get("userId"),
            "adminId": wallet.get("adminId"),
            "walletName": wallet.get("walletName"),
            "balance": res_data.get("balance"),
        })
        time.sleep(1)
        # break   # remove this line to get all wallets

    with open('balances.json', 'w') as f:
        json.dump(balances, f)

