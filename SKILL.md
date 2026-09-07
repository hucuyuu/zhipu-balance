---
name: zhipu-balance
description: Check the remaining prepaid balance of a Zhipu BigModel (GLM) API account. Use when the user asks about Zhipu/BigModel/GLM API 余额 or account balance.
---

# Zhipu Balance

Query the pay-as-you-go balance of a Zhipu BigModel account with the bundled script:

```bash
python3 scripts/check_balance.py
```

Notes:

- The endpoint is `GET https://open.bigmodel.cn/api/biz/account/query-customer-account-report` with the raw API key as `Authorization: Bearer <key>`. It is a console-side endpoint that also accepts API-key auth; it is not part of the official inference API.
- Key resolution order: `ZHIPU_API_KEY`, then the current provider in `~/.cc-switch/cc-switch.db` (only providers whose name or config identifies Zhipu/BigModel). Never print the key and do not pass the key on the command line.
- This queries prepaid balance (`availableBalance`). It does not query GLM Coding Plan quota; that uses a different endpoint and different credentials.
- The request needs outbound network access. If the sandbox blocks it, rerun with escalated permissions and a justification before reporting failure.
- Pass `--json` when the user wants raw fields such as `rechargeAmount`, `giveAmount`, `totalSpendAmount`, or `frozenBalance`.
