# 📈 ETF Momentum Checker

IEFモメンタムに基づくTQQQ/GLD切り替え戦略のバックテストアプリケーション

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🎯 概要

このアプリケーションは、中期米国債ETF（IEF）のモメンタムを指標として、ナスダック3倍レバレッジETF（TQQQ）とゴールドETF（GLD）を切り替える投資戦略をバックテストします。

### 戦略ロジック
- **判定指標**: IEFの1ヶ月リターン
- **選択ルール**: 
  - IEFリターン > 0 → TQQQ保有
  - IEFリターン < 0 → GLD保有
- **リバランス**: 3ヶ月ごと
- **データ**: 月次始値を使用

## 🚀 機能

- ✅ **リアルタイム推奨銘柄**: 現在のIEFモメンタムに基づく推奨表示
- 📊 **インタラクティブチャート**: Plotlyによる累積パフォーマンス可視化
- 📋 **詳細バックテスト**: 3ヶ月ごとの保有履歴と損益計算
- 📈 **統計分析**: 平均リターン、勝率、総リターン等
- 💾 **CSV出力**: 結果のダウンロード機能
- 📱 **レスポンシブデザイン**: PC・スマートフォン対応

## 🛠 技術スタック

- **フレームワーク**: Streamlit
- **データ取得**: yfinance
- **可視化**: Plotly
- **分析**: pandas, numpy
- **デプロイ**: Streamlit Cloud

## 📱 使用方法

### Webアプリ（推奨）
1. [Streamlit Cloud デプロイ版](https://your-app-url.streamlit.app) にアクセス
2. サイドバーで期間を設定
3. 「バックテスト実行」ボタンをクリック

### ローカル実行
```bash
# 環境構築
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# アプリ起動
streamlit run streamlit_app.py
```

### iPhone での使用
- **推奨**: Webアプリをブックマーク
- **Pythonista 3**: `iphone_momentum.py` をインポート
- **a-Shell**: コマンドライン実行

詳細は [IPHONE_SETUP.md](IPHONE_SETUP.md) を参照

## 📊 対象ETF

| ETF | 名称 | 特徴 |
|-----|------|------|
| **TQQQ** | ProShares UltraPro QQQ | NASDAQ 100の3倍レバレッジ |
| **GLD** | SPDR Gold Trust | 金価格連動ETF |
| **IEF** | iShares 7-10 Year Treasury | 中期米国債（判定指標） |

## 📋 ファイル構成

```
momentum_checker/
├── streamlit_app.py          # メインWebアプリ
├── app.py                    # オリジナル版
├── iphone_momentum.py        # iPhone用軽量版
├── direct_test.py           # データ取得テスト
├── requirements.txt         # 依存関係
├── VERSION.md              # バージョン情報
├── ROADMAP.md              # 開発計画
├── CLAUDE.md               # 開発ガイド
└── README.md               # このファイル
```

## 🔄 開発ワークフロー

```bash
# バージョン情報更新
python3 update_version.py

# コミット
git add .
git commit -m "feat: 新機能の説明"

# タグ作成（リリース時）
git tag -a v1.1.0 -m "Version 1.1.0: 説明"
```

詳細は [git_workflow.md](git_workflow.md) を参照

## 📈 パフォーマンス例

*2020-2024年の期間例（実際の結果はアプリで確認）*
- 平均リターン: +8.5%（3ヶ月あたり）
- 勝率: 65%
- 最大利益: +45%
- 最大損失: -12%

## ⚠️ 免責事項

このアプリケーションは教育・研究目的で作成されています。投資判断は自己責任で行ってください。過去のパフォーマンスは将来の結果を保証するものではありません。

## 🔗 関連リンク

- [Streamlit Cloud](https://streamlit.io/cloud)
- [yfinance ドキュメント](https://pypi.org/project/yfinance/)
- [開発ロードマップ](ROADMAP.md)

## 📞 サポート

問題や要望がある場合は、GitHubのIssuesで報告してください。

---

*ETF Momentum Checker v1.0.0*