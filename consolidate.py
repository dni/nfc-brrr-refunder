"""
This script has to be run multiple times because of the fee reserve.
it will stop draining the wallets below 10 sats.
"""

import httpx
import json
import time
from math import ceil

url = "https://legend.lnbits.com/api/v1/wallet"
purl = "https://legend.lnbits.com/api/v1/payments"
lnurl = "https://legend.lnbits.com/lnurlp/api/v1/lnurl/cb/C4bFuv?amount="


with open('wallets.json') as f:
    data = json.load(f)
    for wallet in data:
        res = httpx.get(url, headers={"X-Api-Key": wallet.get("adminId")})
        res.raise_for_status()
        res_data = res.json()
        time.sleep(1)

        balance = res_data.get("balance")

        if balance < 10000:
            print(f"{balance} is less than 10000 from {wallet.get('adminUrlLnBits')}")
            continue

        # fee reserve
        balance = balance - ceil(balance * 0.021)

        print(f"withdraw {balance} sats from {wallet.get('adminUrlLnBits')}")

        res = httpx.get(lnurl + str(balance))
        res.raise_for_status()
        lnurl_data = res.json()

        res = httpx.post(purl,
            json={"out": True, "bolt11": lnurl_data.get("pr")},
            headers={"X-Api-Key": wallet.get("adminId")},
        )

        res.raise_for_status()
        res_data = res.json()

        time.sleep(1)
