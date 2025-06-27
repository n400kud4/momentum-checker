import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ETF Test", layout="wide")

st.title("🧪 ETF Data Test")

# 固定パラメータ
start_date = "2023-01-01"
end_date = "2023-06-01"
symbols = ["IEF", "TQQQ", "GLD"]

st.write(f"📅 期間: {start_date} ～ {end_date}")
st.write(f"📊 銘柄: {', '.join(symbols)}")

if st.button("🚀 テスト実行"):
    results = {}
    
    for symbol in symbols:
        with st.spinner(f"{symbol} データ取得中..."):
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(start=start_date, end=end_date, interval="1mo")
                
                if not data.empty:
                    results[symbol] = data
                    st.success(f"✅ {symbol}: {len(data)}行のデータを取得")
                else:
                    st.error(f"❌ {symbol}: データが空")
                    
            except Exception as e:
                st.error(f"❌ {symbol}: {str(e)}")
    
    # 結果表示
    if results:
        st.header("📊 取得結果")
        
        for symbol, data in results.items():
            st.subheader(f"{symbol} データ")
            st.dataframe(data)
            
            # 価格チャート
            if not data.empty:
                st.line_chart(data['Close'])
    
    st.success("🎉 テスト完了！")

st.sidebar.header("ℹ️ 情報")
st.sidebar.write(f"Streamlit: {st.__version__}")
st.sidebar.write(f"yfinance: {yf.__version__}")
st.sidebar.write(f"pandas: {pd.__version__}")