"""
yfinance統合のためのユーティリティ関数
段階的にyfinanceデータ取得機能を実装
"""

import yfinance as yf
import pandas as pd
import streamlit as st
import time
from datetime import datetime, timedelta
import warnings

# 警告を抑制
warnings.filterwarnings('ignore')

@st.cache_data(ttl=1800, show_spinner=False)  # 30分キャッシュ、期間変更に対応
def get_etf_data(symbol, start_date, end_date, max_retries=3):
    """
    ETFの月次データを取得（yfinance使用）
    
    Args:
        symbol (str): ETFシンボル（IEF, TQQQ, GLD）
        start_date (datetime): 開始日
        end_date (datetime): 終了日
        max_retries (int): 最大再試行回数
    
    Returns:
        pd.DataFrame: 月次OHLCデータ、取得失敗時はNone
    """
    
    # 進行状況表示
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    for attempt in range(max_retries):
        try:
            progress_placeholder.info(f"📊 {symbol} データ取得中... (試行 {attempt + 1}/{max_retries})")
            
            # yfinance Ticker作成
            ticker = yf.Ticker(symbol)
            
            # 日付を文字列に変換
            start_str = start_date.strftime('%Y-%m-%d')
            end_str = end_date.strftime('%Y-%m-%d')
            
            # 月次データ取得
            data = ticker.history(
                start=start_str,
                end=end_str,
                interval="1mo",
                auto_adjust=True,
                prepost=False,
                timeout=30
            )
            
            if data.empty:
                if attempt < max_retries - 1:
                    status_placeholder.warning(f"⚠️ {symbol}: データが空です。再試行中...")
                    time.sleep(2)
                    continue
                else:
                    status_placeholder.error(f"❌ {symbol}: データを取得できませんでした")
                    progress_placeholder.empty()
                    return None
            
            # タイムゾーン正規化
            if data.index.tz is not None:
                data.index = data.index.tz_localize(None)
            
            # 成功メッセージ
            progress_placeholder.success(f"✅ {symbol}: {len(data)}期間のデータを取得")
            status_placeholder.empty()
            
            # 少し待ってからプレースホルダーをクリア
            time.sleep(1)
            progress_placeholder.empty()
            
            return data
            
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                status_placeholder.warning(f"⚠️ {symbol}: エラー発生、再試行中... ({error_msg[:50]}...)")
                time.sleep(2 * (attempt + 1))  # 指数バックオフ
            else:
                status_placeholder.error(f"❌ {symbol}: 最終エラー - {error_msg}")
                progress_placeholder.empty()
                return None
    
    return None

def test_yfinance_connection():
    """yfinance接続テスト"""
    st.subheader("🧪 yfinance接続テスト")
    
    test_symbols = ["IEF", "TQQQ", "GLD"]
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)  # 直近3ヶ月
    
    results = {}
    
    for symbol in test_symbols:
        st.write(f"**{symbol}** をテスト中...")
        
        data = get_etf_data(symbol, start_date, end_date)
        
        if data is not None:
            results[symbol] = {
                "status": "✅ 成功",
                "rows": len(data),
                "latest_date": data.index[-1].strftime('%Y-%m-%d'),
                "latest_price": f"${data['Close'].iloc[-1]:.2f}"
            }
        else:
            results[symbol] = {
                "status": "❌ 失敗",
                "rows": 0,
                "latest_date": "N/A",
                "latest_price": "N/A"
            }
    
    # 結果表示
    st.subheader("📊 テスト結果")
    
    result_df = pd.DataFrame(results).T
    result_df.index.name = "ETF"
    result_df.columns = ["ステータス", "データ数", "最新日付", "最新価格"]
    
    st.dataframe(result_df, use_container_width=True)
    
    # 成功率計算
    success_count = sum(1 for r in results.values() if "成功" in r["status"])
    success_rate = success_count / len(test_symbols) * 100
    
    if success_rate == 100:
        st.success(f"🎉 全てのETFで接続成功！ ({success_rate:.0f}%)")
        return True
    elif success_rate > 0:
        st.warning(f"⚠️ 部分的成功: {success_count}/{len(test_symbols)} ETF ({success_rate:.0f}%)")
        return False
    else:
        st.error("❌ 全てのETFで接続失敗")
        return False

def calculate_ief_momentum_real(start_date=None, end_date=None):
    """
    実際のIEFデータを使用したモメンタム計算
    
    Args:
        start_date (datetime): 開始日（デフォルト: 60日前）
        end_date (datetime): 終了日（デフォルト: 現在）
    
    Returns:
        tuple: (推奨ETF, IEFリターン, 期間文字列)
    """
    
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=90)
    
    # 最新の期間での計算のため、期間情報を表示
    period_info = f"{start_date.strftime('%Y-%m-%d')} ～ {end_date.strftime('%Y-%m-%d')}"
    st.info(f"📊 選択期間でIEFモメンタム計算中: {period_info}")
    
    # IEFデータ取得（期間を拡張して十分なデータを確保）
    extended_start = start_date - timedelta(days=60)  # 追加のマージン
    ief_data = get_etf_data("IEF", extended_start, end_date)
    
    if ief_data is None or len(ief_data) < 2:
        st.error("❌ IEFデータが不足しています。サンプルデータを使用します。")
        return None, None, None
    
    # 1ヶ月リターン計算（最新 vs 前月）
    latest_price = ief_data['Open'].iloc[-1]
    previous_price = ief_data['Open'].iloc[-2]
    
    ief_return = ((latest_price - previous_price) / previous_price) * 100
    
    # 推奨銘柄判定
    recommended_etf = "TQQQ" if ief_return > 0 else "GLD"
    
    # 期間文字列
    period = f"{ief_data.index[-2].strftime('%Y/%m/%d')} ～ {ief_data.index[-1].strftime('%Y/%m/%d')}"
    
    st.success(f"✅ リアルデータ取得完了: IEF {ief_return:+.2f}% → {recommended_etf}")
    
    return recommended_etf, ief_return, period

def get_etf_info():
    """ETF情報を表示"""
    etf_info = {
        "IEF": {
            "name": "iShares 7-10 Year Treasury Bond ETF",
            "description": "中期米国債ETF（7-10年満期）",
            "use": "モメンタム判定指標",
            "available_from": "2004年"
        },
        "TQQQ": {
            "name": "ProShares UltraPro QQQ",
            "description": "NASDAQ 100の3倍レバレッジETF",
            "use": "成長資産（正のモメンタム時）",
            "available_from": "2010年3月"
        },
        "GLD": {
            "name": "SPDR Gold Trust",
            "description": "金価格連動ETF",
            "use": "安全資産（負のモメンタム時）",
            "available_from": "2004年"
        }
    }
    
    return etf_info