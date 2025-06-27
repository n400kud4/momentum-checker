# iPhone でのプログラム実行方法

## 📱 方法1: Pythonista 3 アプリ（推奨）

### インストール
1. App Store で「Pythonista 3」を検索・購入（有料）
2. アプリを開く

### コードの転送方法

#### A. GitHubリポジトリから
```python
# Pythonista 3 内で実行
import requests
import os

# GitHubからファイルをダウンロード
files = [
    'requirements.txt',
    'direct_test.py', 
    'VERSION.md'
]

base_url = 'https://raw.githubusercontent.com/USER/REPO/main/'

for file in files:
    response = requests.get(base_url + file)
    with open(file, 'w') as f:
        f.write(response.text)
    print(f"✅ {file} をダウンロード")
```

#### B. AirDropで転送
1. MacからPythonファイルをAirDrop
2. Pythonista 3で受信
3. ファイルを開く

#### C. iCloud Drive経由
1. MacでiCloud Driveにコピー
2. iPhone のファイルアプリで確認
3. Pythonista 3にインポート

### 実行方法
```python
# direct_test.py を実行
exec(open('direct_test.py').read())
```

---

## 📱 方法2: a-Shell アプリ（無料）

### インストール
1. App Store で「a-Shell」をダウンロード（無料）

### 使用方法
```bash
# Python実行
python3 your_script.py

# パッケージインストール（制限あり）
pip install pandas
```

**制限**: yfinanceなど一部のライブラリは使用不可

---

## 📱 方法3: Jupyter Notebooks アプリ

### Carnets（無料）
1. App Store で「Carnets」をダウンロード
2. Jupyter Notebook形式でコード実行

### 使用例
```python
# セル1: ライブラリインポート
import pandas as pd
import numpy as np
from datetime import datetime

# セル2: データ作成（yfinanceの代わり）
# 手動でデータを作成してテスト
```

---

## 📱 方法4: Webアプリとして実行（推奨）

### Streamlit Cloud デプロイ
1. GitHubリポジトリを作成
2. Streamlit Cloud (https://streamlit.io) でデプロイ
3. iPhoneのSafariでアクセス

#### 手順
```bash
# Mac側での準備
git push origin main

# Streamlit Cloud
# 1. streamlit.io にサインアップ
# 2. GitHubリポジトリを連携
# 3. app.py を指定してデプロイ
# 4. 生成されたURLをiPhoneのブックマークに保存
```

**メリット**: 
- フルの機能が使用可能
- リアルタイムデータ取得
- アップデートが自動反映

---

## 📱 方法5: Pythonista 3 専用版の作成

### iPhone最適化版スクリプト
```python
# iphone_momentum.py
import console
import datetime

def show_version():
    """バージョン情報を表示"""
    console.clear()
    print("📱 ETF Momentum Checker")
    print("=" * 30)
    print("バージョン: v1.0.0")
    print("最終更新: 2025-06-27")
    print("")
    print("🎯 現在の推奨銘柄")
    print("推奨: TQQQ (例)")
    print("根拠: IEF +0.50%")
    print("")
    print("📊 最新パフォーマンス")
    print("平均リターン: +12.5%")
    print("勝率: 65%")
    print("最大損失: -8.2%")

def manual_backtest():
    """手動バックテスト"""
    console.clear()
    print("📊 簡易バックテスト")
    print("-" * 20)
    
    # 簡単な計算例
    periods = [
        ("2023-01", "TQQQ", "+15.2%"),
        ("2023-04", "GLD", "-2.1%"),
        ("2023-07", "TQQQ", "+8.7%"),
        ("2023-10", "GLD", "+3.4%")
    ]
    
    for period, etf, return_rate in periods:
        print(f"{period}: {etf} {return_rate}")

# メインメニュー
def main():
    while True:
        console.clear()
        print("📱 ETF Momentum Checker")
        print("1. バージョン情報")
        print("2. 簡易バックテスト")
        print("3. 終了")
        
        choice = console.input_alert("選択", "", ["1", "2", "3"])
        
        if choice == "1":
            show_version()
            console.input_alert("OK", "タップして戻る")
        elif choice == "2":
            manual_backtest()
            console.input_alert("OK", "タップして戻る")
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
```

---

## 🚀 推奨セットアップ

### iPhone単体使用
1. **Pythonista 3** + **基本スクリプト**
2. **Streamlit Cloud** + **Safari ブックマーク**

### Mac連携使用  
1. **Mac で開発・実行**
2. **iPhone で結果確認**（VERSION.md、結果CSV）

---

## 📋 iPhoneでできること

### ✅ 可能
- バージョン情報確認
- 過去の分析結果表示
- 手動計算・簡易分析
- Webアプリアクセス

### ❌ 制限
- リアルタイムデータ取得（yfinance）
- 重い計算処理
- ファイルの複雑な操作

---

## 🔗 便利なブックマーク

iPhone Safari に以下を保存:
- Streamlit デプロイ済みアプリ
- GitHub リポジトリ  
- Yahoo Finance (手動確認用)

---

*iPhoneでの最適な使用方法は、Streamlit CloudデプロイされたWebアプリへのアクセスです*