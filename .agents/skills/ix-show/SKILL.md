---
name: ix-show
description: NEC IX の show コマンドを安全に実行して、インターフェース、ルーティング、IPsec、ログなどの状態を確認する。
---

# Codex adapter

[共通の ix-show skill](../../../skills/ix-show/SKILL.md) を最後まで読み、その手順と安全条件に従う。

この adapter ファイルの実体（symlink/junction の target）を解決し、その3階層上を ix-toolkit repository root の絶対パスとする。共通手順中の `${CLAUDE_PLUGIN_ROOT}` は実際の環境変数として使わず、この絶対パスへ置き換える。Claude Code 固有の `$ARGUMENTS` は Codex では現在のユーザー要求として解釈する。
