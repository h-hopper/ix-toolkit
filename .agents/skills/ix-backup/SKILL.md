---
name: ix-backup
description: 対象を明示して NEC IX の running-config をローカルファイルへ読み取り専用で退避する。
---

# Codex adapter

[共通の ix-backup skill](../../../skills/ix-backup/SKILL.md) を最後まで読み、その手順と安全条件に従う。

この adapter ファイルの実体（symlink/junction の target）を解決し、その3階層上を ix-toolkit repository root の絶対パスとする。共通手順中の `${CLAUDE_PLUGIN_ROOT}` は実際の環境変数として使わず、この絶対パスへ置き換える。Claude Code 固有の `$ARGUMENTS` は Codex では現在のユーザー要求として解釈する。
