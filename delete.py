import httpx
import json
import time

url = "https://legend.lnbits.com/api/v1/wallet"

with open('wallets.json') as f:
    data = json.load(f)
    for wallet in data:
        res = httpx.delete(url, headers={"X-Api-Key": wallet.get("adminId")})
        res.raise_for_status()
        print(f"deleted {wallet.get('adminUrlLnBits')}")
        time.sleep(1)
