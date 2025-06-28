# 🚀 Streamlit Cloud デプロイガイド

## 📋 デプロイ手順

### 1. GitHub リポジトリ準備
```bash
# リモートリポジトリを追加（GitHubで作成後）
git remote add origin https://github.com/YOUR_USERNAME/momentum_checker.git

# プッシュ
git push -u origin main
```

### 2. Streamlit Cloud セットアップ
1. [Streamlit Cloud](https://streamlit.io/cloud) にアクセス
2. GitHubアカウントでサインイン
3. 「New app」をクリック
4. リポジトリを選択: `YOUR_USERNAME/momentum_checker`
5. メインファイル: `streamlit_app.py`
6. 「Deploy!」をクリック

### 3. 設定ファイル（自動認識）
```toml
# .streamlit/config.toml （既存）
[server]
runOnSave = false
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
```

### 4. 要件ファイル（自動認識）
```txt
# requirements.txt （既存）
streamlit>=1.28.0
yfinance>=0.2.20
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
```

## 🔗 デプロイ後のURL

デプロイ完了後、以下の形式のURLが生成されます：
```
https://YOUR_USERNAME-momentum-checker-streamlit-app-HASH.streamlit.app
```

## 📱 iPhone 設定

### Safari ブックマーク追加
1. iPhoneでデプロイ済みURLにアクセス
2. 共有ボタン → 「ホーム画面に追加」
3. アイコン名: 「ETF Momentum」

### ホーム画面アプリ化
デプロイしたWebアプリをPWA（Progressive Web App）として使用可能

## 🔄 自動更新

GitHubに新しいコミットをプッシュすると、Streamlit Cloudが自動的に再デプロイされます。

```bash
# 新機能を追加してプッシュ
git add .
git commit -m "feat: 新機能追加"
git push origin main
# → 自動的にWebアプリが更新される
```

## ⚙️ 環境変数（必要に応じて）

Streamlit Cloud の設定画面で環境変数を設定可能：
- API キー等の機密情報
- デバッグフラグ
- 外部サービスの設定

## 🐛 トラブルシューティング

### よくある問題

1. **デプロイ失敗**
   - `requirements.txt` の依存関係を確認
   - Python バージョンの互換性確認

2. **データ取得エラー**
   - yfinance の制限回避（キャッシュ設定）
   - タイムアウト設定の調整

3. **パフォーマンス問題**
   - `@st.cache_data` の活用
   - 不要な計算の削減

### ログ確認
Streamlit Cloud の管理画面でリアルタイムログを確認可能

## 📊 使用量制限

Streamlit Cloud（無料プラン）の制限：
- 同時接続数: 制限あり
- 月間使用時間: 制限あり
- リソース: CPU・メモリ制限

## 🔒 セキュリティ

- HTTPS 自動対応
- 機密情報は環境変数で管理
- 公開アプリのため、内部情報は含めない

## 📈 アクセス解析

Streamlit Cloud では基本的なアクセス統計を確認可能：
- 訪問者数
- セッション時間
- エラー発生状況

---

## 🎯 デプロイ完了チェックリスト

- [ ] GitHubリポジトリ作成・プッシュ完了
- [ ] Streamlit Cloud アカウント作成
- [ ] アプリデプロイ完了
- [ ] 動作確認（データ取得・チャート表示）
- [ ] iPhone Safari ブックマーク追加
- [ ] エラーログ確認
- [ ] README.md のURL更新

---

*デプロイ完了後は、世界中からアクセス可能なETF分析ツールが完成します！*