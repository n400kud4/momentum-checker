# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a momentum-based ETF trading strategy backtesting application built with Python and Streamlit. The app analyzes momentum between TQQQ (3x leveraged NASDAQ ETF) and GLD (Gold ETF) to determine optimal holdings based on IEF (Treasury ETF) performance as a benchmark.

**🆕 Current Status**: yfinance統合Phase 1完了 - リアルデータ取得機能実装済み
- **メインアプリ**: `app.py` (サンプルデータ版・本番稼働中)
- **開発版**: `app_yfinance.py` (yfinance統合版・Phase 1完了)
- **ブランチ**: `feature/yfinance-integration` でyfinance機能開発中

## Development Commands

### Environment Setup
```bash
# 仮想環境作成と依存関係インストール
python3 -m venv momentum_env
source momentum_env/bin/activate
pip install -r requirements.txt
```

### Running the Application
```bash
# 🟢 本番アプリ (Streamlit Cloud稼働中)
source momentum_env/bin/activate && streamlit run app.py

# 🔴 yfinance統合版 (開発中・Phase 1完了)
source momentum_env/bin/activate && streamlit run app_yfinance.py

# 🧪 yfinance接続テスト
source momentum_env/bin/activate && python3 test_yfinance.py

# Legacy versions (参考用)
streamlit run app_simple.py     # Simplified version with connection pooling
streamlit run direct_test.py    # Direct data testing (no UI)
```

### Streamlit Configuration
- Custom config at `.streamlit/config.toml` optimizes connection stability
- Default ports: 8505-8509 (configured to avoid conflicts)
- Connection error mitigation: CORS disabled, XSRF protection disabled

## Application Architecture

### Core Strategy Logic
The momentum strategy follows this decision tree:
1. **Data Collection**: Monthly open prices for IEF, TQQQ, GLD via yfinance
2. **Momentum Signal**: IEF 1-month return calculation: `(current_open - previous_open) / previous_open * 100`
3. **Position Selection**: Positive IEF return → TQQQ, Negative IEF return → GLD
4. **Rebalancing**: 3-month holding periods starting from user-defined start date
5. **Performance Calculation**: Simple return formula for each 3-month period

### 🚀 yfinance統合の進行状況

#### ✅ Phase 1完了: 基本データ取得機能
- **ファイル**: `yfinance_utils.py`, `app_yfinance.py`, `test_yfinance.py`
- **機能**: ETFデータ取得、接続テスト、エラーハンドリング、キャッシュ機能
- **対応ETF**: IEF, TQQQ, GLD
- **テスト結果**: 全ETFで正常にデータ取得確認済み

#### 🟡 Phase 2進行中: IEFモメンタム判定
- リアルタイム推奨銘柄判定（基本実装済み）
- モメンタム計算ロジックの完全実装

#### ⏳ Phase 3予定: 完全バックテスト
- TQQQ・GLDでのリアルデータバックテスト
- 3ヶ月リバランス計算
- パフォーマンス統計の更新

#### ⏳ Phase 4予定: 本番デプロイ
- Streamlit Cloudでの動作確認
- エラー処理の最終調整

### Key Technical Implementation

**Data Handling**:
- `@st.cache_data(ttl=600)` caching prevents excessive API calls
- Timezone normalization via `tz_localize(None)` prevents comparison errors
- Sequential data fetching with 1-2 second delays to avoid rate limiting

**Connection Stability**:
- Multiple app versions handle different levels of connection issues
- `direct_test.py` provides fallback for pure data verification
- Custom requests session with retry logic in advanced versions

**File Structure**:
- `app.py`: 🟢 Main production application (サンプルデータ版・Streamlit Cloud稼働中)
- `app_yfinance.py`: 🔴 yfinance統合版アプリ (Phase 1完了・開発中)
- `yfinance_utils.py`: yfinanceデータ取得ユーティリティ関数
- `test_yfinance.py`: yfinance接続テスト用スクリプト
- `app_simple.py`: 旧版 - Connection-optimized version  
- `direct_test.py`: 旧版 - Standalone data testing script
- `requirements.txt`: 依存関係 (streamlit, yfinance, pandas, numpy)

### Data Requirements
- **TQQQ**: March 2010 onwards
- **GLD/IEF**: 2004 onwards  
- **Default period**: January 2015 to present
- **Pricing**: Monthly open prices only (not adjusted close)
- **Interval**: Monthly data (`interval="1mo"` in yfinance)

### Known Issues & Solutions
- **yfinance connection errors**: ✅ 解決済み - retry logic and request session management
- **Timezone comparison errors**: ✅ 解決済み - timezone normalization in data preprocessing  
- **Streamlit connection drops**: ✅ 解決済み - custom server configuration and multiple app variants
- **yfinance統合**: ✅ Phase 1完了 - 基本データ取得機能実装済み

### 🔧 現在の開発環境
- **仮想環境**: `momentum_env`
- **メインブランチ**: `main` (サンプルデータ版・安定稼働)
- **開発ブランチ**: `feature/yfinance-integration` (yfinance機能開発中)
- **接続テスト**: 全ETF（IEF, TQQQ, GLD）で正常動作確認済み
- **アプリURL**: http://localhost:8501 (ローカル開発時)