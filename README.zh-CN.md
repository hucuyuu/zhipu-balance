# Zhipu Balance Skill

[English](README.md) | 简体中文

一个用于查询智谱 BigModel/GLM API 预付费余额的 Codex skill。

## 功能

- 查询可用余额、累计充值、累计消费和冻结金额
- 支持普通文本输出和原始 JSON 输出
- API key 不会写入仓库，也不会打印到终端

## 安装

把本目录复制或链接到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R . ~/.codex/skills/zhipu-balance
```

脚本只依赖 Python 3 标准库，无需额外安装包。

## 配置 API key

推荐通过环境变量提供 key：

```bash
export ZHIPU_API_KEY="your-api-key"
```

如果未设置 `ZHIPU_API_KEY`，脚本会尝试从本机 `~/.cc-switch/cc-switch.db`
中查找当前选中的 Zhipu/BigModel provider。该文件不会被读取进仓库，也不会被上传。

不要把 API key 放进 shell history、README、CI 日志或 Git 提交中。

## 使用

在 skill 目录中运行：

```bash
python3 scripts/check_balance.py
```

输出示例：

```text
可用余额: ¥123.45
累计充值: ¥200.00
累计消费: ¥76.55
冻结金额: ¥0.00
```

查看 API 返回的原始数据：

```bash
python3 scripts/check_balance.py --json
```

如果本机存在多个 `cc-switch` provider 配置，可以显式指定数据库路径：

```bash
python3 scripts/check_balance.py --db /path/to/cc-switch.db
```

## 说明

脚本调用的是：

```text
GET https://open.bigmodel.cn/api/biz/account/query-customer-account-report
```

这是一个控制台侧余额查询 endpoint，不是官方推理 API 文档中的模型调用接口。
本工具只查询预付费余额，不查询 GLM Coding Plan 的配额。

## License

MIT。详见 [LICENSE](LICENSE)。
