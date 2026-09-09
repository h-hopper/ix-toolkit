---
name: ix-configure
description: 対象と設定行を明示し、確認後に NEC IX の config モードで設定を適用する。設定変更を求められた場合に使用する。
---

# Codex adapter

[共通の ix-configure skill](../../../skills/ix-configure/SKILL.md) を最後まで読み、その手順と安全条件に従う。

この adapter ファイルの実体（symlink/junction の target）を解決し、その3階層上を ix-toolkit repository root の絶対パスとする。共通手順中の `${CLAUDE_PLUGIN_ROOT}` は実際の環境変数として使わず、この絶対パスへ置き換える。Claude Code 固有の `$ARGUMENTS` は Codex では現在のユーザー要求として解釈する。対象機器と設定行についてユーザーの明示確認を得るまで変更を実行しない。
