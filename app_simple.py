import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# セッションの設定でconnection poolingを改善
@st.cache_resource
def get_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

st.set_page_config(
    page_title="Momentum Checker",
    page_icon="📈",
    layout="wide"
)

# グローバルセッション
session = get_session()

def get_data_safe(symbol, start_date, end_date):
    """安全なデータ取得"""
    try:
        ticker = yf.Ticker(symbol)
        # セッションを使用してコネクション再利用
        ticker.session = session
        
        data = ticker.history(
            start=start_date.strftime('%Y-%m-%d'), 
            end=end_date.strftime('%Y-%m-%d'), 
            interval="1mo",
            timeout=10
        )
        
        if data.empty:
            return None
            
        # タイムゾーン処理
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)
            
        return data
        
    except Exception as e:
        st.error(f"{symbol}エラー: {str(e)}")
        return None

def main():
    st.title("📈 Momentum Checker - Stable Version")
    
    # 固定期間でテスト
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 1, 1)
    
    st.write(f"📅 テスト期間: {start_date.strftime('%Y-%m-%d')} ～ {end_date.strftime('%Y-%m-%d')}")
    
    if st.button("🚀 実行", type="primary"):
        
        with st.spinner("データ取得中..."):
            # IEFデータ取得
            st.write("📊 IEF取得中...")
            ief_data = get_data_safe("IEF", start_date, end_date)
            
            if ief_data is not None:
                st.success(f"✅ IEF: {len(ief_data)}行")
                
                time.sleep(2)  # 間隔を空ける
                
                # TQQQ取得
                st.write("📊 TQQQ取得中...")
                tqqq_data = get_data_safe("TQQQ", start_date, end_date)
                
                if tqqq_data is not None:
                    st.success(f"✅ TQQQ: {len(tqqq_data)}行")
                    
                    time.sleep(2)  # 間隔を空ける
                    
                    # GLD取得
                    st.write("📊 GLD取得中...")
                    gld_data = get_data_safe("GLD", start_date, end_date)
                    
                    if gld_data is not None:
                        st.success(f"✅ GLD: {len(gld_data)}行")
                        st.balloons()
                        
                        # 簡単な結果表示
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("IEF期間", f"{len(ief_data)}ヶ月")
                            
                        with col2:
                            st.metric("TQQQ期間", f"{len(tqqq_data)}ヶ月")
                            
                        with col3:
                            st.metric("GLD期間", f"{len(gld_data)}ヶ月")
                        
                        # データ表示
                        st.subheader("📊 取得データサンプル")
                        
                        tab1, tab2, tab3 = st.tabs(["IEF", "TQQQ", "GLD"])
                        
                        with tab1:
                            st.dataframe(ief_data.head())
                            
                        with tab2:
                            st.dataframe(tqqq_data.head())
                            
                        with tab3:
                            st.dataframe(gld_data.head())
                    
                    else:
                        st.error("❌ GLDデータ取得失敗")
                else:
                    st.error("❌ TQQQデータ取得失敗")
            else:
                st.error("❌ IEFデータ取得失敗")
    
    # システム情報
    st.sidebar.header("🔧 システム情報")
    st.sidebar.write(f"yfinance: {yf.__version__}")
    st.sidebar.write(f"pandas: {pd.__version__}")
    st.sidebar.write(f"streamlit: {st.__version__}")

if __name__ == "__main__":
    main()