import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Momentum Checker",
    page_icon="📈",
    layout="wide"
)

@st.cache_data(ttl=600)  # 10分間キャッシュ
def get_monthly_data(symbol, start_date, end_date):
    """指定されたシンボルの月次データを取得"""
    try:
        st.write(f"📊 {symbol}のデータを取得中...")
        ticker = yf.Ticker(symbol)
        
        # 日付を文字列形式に変換
        if isinstance(start_date, datetime):
            start_str = start_date.strftime('%Y-%m-%d')
        else:
            start_str = str(start_date)
            
        if isinstance(end_date, datetime):
            end_str = end_date.strftime('%Y-%m-%d')
        else:
            end_str = str(end_date)
        
        st.write(f"期間: {start_str} ～ {end_str}")
        
        data = ticker.history(start=start_str, end=end_str, interval="1mo")
        
        if data.empty:
            st.error(f"❌ {symbol}: データが空です")
            return None
            
        st.success(f"✅ {symbol}: {len(data)}行のデータを取得")
        
        # タイムゾーン情報を削除
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)
            
        return data
        
    except Exception as e:
        st.error(f"❌ {symbol}のデータ取得エラー: {str(e)}")
        st.write(f"エラー詳細: {type(e).__name__}")
        return None

def calculate_ief_momentum():
    """IEFの直近1ヶ月リターンを計算してモメンタムを判定"""
    # 直近2ヶ月のデータを取得
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    ief_data = get_monthly_data("IEF", start_date, end_date)
    
    if ief_data is None or len(ief_data) < 2:
        return None, None, None
    
    # 最新の1ヶ月リターンを計算
    latest_return = ((ief_data['Open'].iloc[-1] - ief_data['Open'].iloc[-2]) / ief_data['Open'].iloc[-2]) * 100
    
    # モメンタム判定: IEFのリターンが正の場合はTQQQ、負の場合はGLD
    recommended_etf = "TQQQ" if latest_return > 0 else "GLD"
    
    period = f"{ief_data.index[-2].strftime('%Y/%m/%d')} ～ {ief_data.index[-1].strftime('%Y/%m/%d')}"
    
    return recommended_etf, latest_return, period

def calculate_simple_backtest(start_date, end_date):
    """簡素化されたバックテスト"""
    st.header("📊 データ取得状況")
    
    # データ取得
    ief_data = get_monthly_data("IEF", start_date, end_date)
    if ief_data is None:
        return None
        
    time.sleep(1)  # API制限回避
    tqqq_data = get_monthly_data("TQQQ", start_date, end_date)
    if tqqq_data is None:
        return None
        
    time.sleep(1)  # API制限回避
    gld_data = get_monthly_data("GLD", start_date, end_date)
    if gld_data is None:
        return None
    
    st.success("🎉 全てのデータ取得が完了しました！")
    
    # 簡単な分析例
    results = []
    
    # 月次リターンを計算（簡素化）
    for i in range(1, min(len(ief_data), 12)):  # 最大12ヶ月
        ief_return = ((ief_data['Open'].iloc[i] - ief_data['Open'].iloc[i-1]) / ief_data['Open'].iloc[i-1]) * 100
        selected_etf = "TQQQ" if ief_return > 0 else "GLD"
        
        if selected_etf == "TQQQ" and i < len(tqqq_data):
            etf_return = ((tqqq_data['Open'].iloc[i] - tqqq_data['Open'].iloc[i-1]) / tqqq_data['Open'].iloc[i-1]) * 100
            price_start = tqqq_data['Open'].iloc[i-1]
            price_end = tqqq_data['Open'].iloc[i]
        elif selected_etf == "GLD" and i < len(gld_data):
            etf_return = ((gld_data['Open'].iloc[i] - gld_data['Open'].iloc[i-1]) / gld_data['Open'].iloc[i-1]) * 100
            price_start = gld_data['Open'].iloc[i-1]
            price_end = gld_data['Open'].iloc[i]
        else:
            continue
            
        results.append({
            '月': ief_data.index[i].strftime('%Y-%m'),
            '保有銘柄': selected_etf,
            '開始価格': f"${price_start:.2f}",
            '終了価格': f"${price_end:.2f}",
            '損益率(%)': f"{etf_return:+.2f}%"
        })
    
    return pd.DataFrame(results)

def main():
    st.title("📈 Momentum Checker - 診断モード")
    st.markdown("---")
    
    # サイドバーで期間設定
    st.sidebar.header("📅 テスト期間設定")
    
    # より短い期間でテスト
    default_start = datetime(2023, 1, 1)
    default_end = datetime(2024, 1, 1)
    
    start_date = st.sidebar.date_input(
        "開始日",
        value=default_start,
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now()
    )
    
    end_date = st.sidebar.date_input(
        "終了日", 
        value=default_end,
        min_value=start_date,
        max_value=datetime.now()
    )
    
    if st.sidebar.button("🧪 診断実行", type="primary"):
        st.header("🎯 現在の推奨銘柄")
        
        # 現在の推奨銘柄
        recommended_etf, ief_return, period = calculate_ief_momentum()
        
        if recommended_etf:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("推奨銘柄", recommended_etf)
            
            with col2:
                st.metric("IEFリターン", f"{ief_return:.2f}%")
            
            with col3:
                st.metric("判定期間", period)
        
        st.markdown("---")
        
        # バックテスト結果
        backtest_results = calculate_simple_backtest(start_date, end_date)
        
        if backtest_results is not None and not backtest_results.empty:
            st.header("📊 バックテスト結果")
            st.dataframe(backtest_results, use_container_width=True)
            
            # 統計情報
            returns_numeric = backtest_results['損益率(%)'].str.replace('%', '').str.replace('+', '').astype(float)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("期間数", len(backtest_results))
            with col2:
                st.metric("平均リターン", f"{returns_numeric.mean():.2f}%")
            with col3:
                st.metric("勝率", f"{(returns_numeric > 0).mean() * 100:.1f}%")
        else:
            st.error("バックテストデータの取得に失敗しました")
    
    else:
        st.info("👈 サイドバーの「診断実行」ボタンを押してテストを開始してください")

if __name__ == "__main__":
    main()