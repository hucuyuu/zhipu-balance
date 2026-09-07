#!/usr/bin/env python3
"""Check the prepaid balance of a Zhipu BigModel API account."""

import argparse
import json
import os
import sqlite3
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://open.bigmodel.cn/api/biz/account/query-customer-account-report"
DEFAULT_DB = Path.home() / ".cc-switch" / "cc-switch.db"


def key_from_db(db_path: Path) -> str:
    if not db_path.exists():
        raise SystemExit(f"cc-switch database not found: {db_path}")
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "select name, is_current, settings_config from providers"
        ).fetchall()
    finally:
        con.close()

    candidates = []
    for name, is_current, cfg_json in rows:
        try:
            cfg = json.loads(cfg_json)
        except (TypeError, ValueError):
            continue
        key = (cfg.get("auth") or {}).get("OPENAI_API_KEY") or ""
        blob = json.dumps(cfg, ensure_ascii=False).lower()
        if key and ("zhipu" in name.lower() or "bigmodel.cn" in blob):
            candidates.append((is_current, name, key))
    if not candidates:
        raise SystemExit(f"No Zhipu/BigModel provider with an API key in {db_path}")
    current = [c for c in candidates if c[0]]
    if len(current) > 1:
        raise SystemExit("Multiple current Zhipu providers; set ZHIPU_API_KEY explicitly")
    chosen = current[0] if current else candidates[0]
    return chosen[2]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="cc-switch database path")
    parser.add_argument("--json", action="store_true", help="print the raw response body")
    args = parser.parse_args()

    key = os.environ.get("ZHIPU_API_KEY") or key_from_db(args.db)
    req = urllib.request.Request(
        ENDPOINT,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        raise SystemExit(f"HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error: {e.reason}")

    if not body.get("success"):
        raise SystemExit(f"API error: {body.get('msg', body)}")

    if args.json:
        print(json.dumps(body["data"], ensure_ascii=False, indent=2))
        return
    data = body["data"]
    print(f"可用余额: ¥{float(data['availableBalance']):.2f}")
    print(f"累计充值: ¥{float(data['rechargeAmount']):.2f}")
    print(f"累计消费: ¥{float(data['totalSpendAmount']):.2f}")
    print(f"冻结金额: ¥{float(data.get('frozenBalance') or 0):.2f}")


if __name__ == "__main__":
    main()
