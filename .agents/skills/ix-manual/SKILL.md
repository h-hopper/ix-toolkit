---
name: ix-manual
description: ローカル生成済みの NEC IX マニュアル corpus を検索し、コマンド構文、制約、機能仕様、諸元値を確認する。
---

# Codex adapter

[共通の ix-manual skill](../../../skills/ix-manual/SKILL.md) を最後まで読み、その手順と安全条件に従う。

この adapter ファイルの実体（symlink/junction の target）を解決し、その3階層上を ix-toolkit repository root の絶対パスとする。共通手順中の `${CLAUDE_PLUGIN_ROOT}` は実際の環境変数として使わず、この絶対パスへ置き換える。manual corpus が無い場合は共通手順どおり停止し、記憶や推測で NEC IX コマンドを補わない。
