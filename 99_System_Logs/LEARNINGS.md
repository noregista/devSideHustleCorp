# LEARNINGS.md — 学習ループログ

> セッション中に発見した「うまくいったこと・失敗・パターン」を記録する。
> 週次または節目ごとにClaudeが合成し、重要な原則は CLAUDE.md へ昇格させる。
>
> **フォーマット**
> - 観察: 発見した事実（日付付き）
> - 合成: 複数の観察から導き出された原則（週次レビュー時に記入）
> - 昇格済み: CLAUDE.md に組み込んだもの（アーカイブ）

---

## 観察ログ

### 2026-04-11

**[失敗] writer.py が trend_guide.json を半分しか使っていなかった**
- trending_topics: 全5件中3件のみ渡していた
- hook_phrases: 全7件中3件のみ渡していた
- post_patterns: 全3件中1件のみ、かつ例文を60字で切り捨てていた
- avoid_patterns: 全4件中2件のみ渡していた
- hashtags: 完全に未使用だった
- → `agents/writer.py` を修正して全件渡すよう改善（commit: 70f9397）

**[発見] バズサーチ（trend_researcher.py）の自動実行に証跡がない**
- Mac側でlaunchd経由で動いているが、logsディレクトリが存在しない
- trend_guide.json の updated_at を見るしかなく、正常終了か異常終了かが判別できない
- → ログ確認の習慣と、異常時の検知方法を要検討

**[改善] Claude Code の許可設定を bypassPermissions に変更**
- 毎回の確認プロンプトがオーナーの作業を中断していた
- `~/.claude/settings.json` に `"defaultMode": "bypassPermissions"` を設定
- → 以降の作業で確認なしにツール実行可能

---

## 合成ログ（週次レビュー時に記入）

*まだ合成なし — 2026-04-11 観察開始*

---

## 昇格済み（CLAUDE.md反映済み）

*まだなし*

---

*初版作成: 2026-04-11 | AI統括マネージャー*
