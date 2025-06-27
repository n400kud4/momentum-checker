# Git ワークフロー

## 📱 コミット時の手順

### 1. バージョン情報の更新
```bash
python update_version.py
```

### 2. 変更をステージング
```bash
git add .
```

### 3. コミット
```bash
git commit -m "機能追加: 新機能の説明

詳細:
- 追加した機能1
- 修正した問題2
- 改善した点3

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 4. 新バージョンタグ作成（メジャーリリース時）
```bash
git tag -a v1.1.0 -m "Version 1.1.0: 新機能リリース

主な変更:
- 機能追加1
- 機能追加2
- バグ修正"
```

### 5. バージョン情報再更新（タグ作成後）
```bash
python update_version.py
git add VERSION.md
git commit -m "docs: VERSION.mdを最新タグ情報で更新"
```

---

## 📋 バージョンルール

### セマンティックバージョニング
- **v1.0.0** → **v1.0.1**: バグ修正
- **v1.0.0** → **v1.1.0**: 新機能追加
- **v1.0.0** → **v2.0.0**: 破壊的変更

### タグのタイミング
- 安定した機能追加時
- 重要なバグ修正時
- 本番デプロイ前

---

## 🔄 自動化された処理

1. `update_version.py` 実行で `VERSION.md` が自動更新
2. Git情報（タグ、コミット、ブランチ）を自動取得
3. iPhone用の簡潔な情報も含む

---

## 📞 iPhone確認時

`VERSION.md` ファイルを開くだけで以下が確認可能:
- 現在のバージョン
- 最新の変更内容  
- リリース日
- 技術仕様

---

*このワークフローにより、常に最新のバージョン情報が管理されます*