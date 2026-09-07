# Zhipu Balance Skill

English | [简体中文](README.zh-CN.md)

A Codex skill for querying the prepaid balance of a Zhipu BigModel/GLM API account.

## Features

- Query available balance, total recharge, total spend, and frozen amount
- Support both human-readable text and raw JSON output
- The API key is never stored in the repository or printed to the terminal

## Installation

Copy or link this directory into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/zhipu-balance
```

The script only uses the Python 3 standard library, so no additional packages are required.

## Configure the API key

Provide the key through an environment variable:

```bash
export ZHIPU_API_KEY="your-api-key"
```

If `ZHIPU_API_KEY` is not set, the script tries to find the currently selected
Zhipu/BigModel provider in the local `~/.cc-switch/cc-switch.db` database.
That database is not read into or uploaded by this repository.

Do not put API keys in shell history, README files, CI logs, or Git commits.

## Usage

Run the script from the skill directory:

```bash
python3 scripts/check_balance.py
```

Example output:

```text
可用余额: ¥123.45
累计充值: ¥200.00
累计消费: ¥76.55
冻结金额: ¥0.00
```

To print the raw API response:

```bash
python3 scripts/check_balance.py --json
```

If your local `cc-switch` configuration has multiple providers, you can specify
the database path explicitly:

```bash
python3 scripts/check_balance.py --db /path/to/cc-switch.db
```

## Notes

The script calls:

```text
GET https://open.bigmodel.cn/api/biz/account/query-customer-account-report
```

This is a console-side balance-query endpoint, not a model invocation endpoint
from the official inference API documentation. This tool only queries prepaid
balance; it does not query GLM Coding Plan quota.

## License

MIT. See [LICENSE](LICENSE).
