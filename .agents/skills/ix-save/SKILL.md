---
name: ix-save
description: 対象を明示して確認後に NEC IX の running-config を write memory で永続化する。
---

# Codex adapter

[共通の ix-save skill](../../../skills/ix-save/SKILL.md) を最後まで読み、その手順と安全条件に従う。

この adapter ファイルの実体（symlink/junction の target）を解決し、その3階層上を ix-toolkit repository root の絶対パスとする。共通手順中の `${CLAUDE_PLUGIN_ROOT}` は実際の環境変数として使わず、この絶対パスへ置き換える。Claude Code 固有の `$ARGUMENTS` は Codex では現在のユーザー要求として解釈する。ユーザーの明示確認を得るまで `write memory` を実行しない。
