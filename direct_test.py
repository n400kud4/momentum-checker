#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

def test_etf_data():
    """ETFデータの直接テスト"""
    print("🧪 ETF Data Direct Test")
    print("=" * 50)
    
    symbols = ["IEF", "TQQQ", "GLD"]
    start_date = "2023-01-01"
    end_date = "2023-06-01"
    
    print(f"📅 期間: {start_date} ～ {end_date}")
    print(f"📊 銘柄: {', '.join(symbols)}")
    print()
    
    results = {}
    
    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] {symbol} データ取得中...")
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date, interval="1mo")
            
            if not data.empty:
                results[symbol] = data
                print(f"✅ {symbol}: {len(data)}行のデータを取得")
                print(f"   期間: {data.index[0].strftime('%Y-%m-%d')} ～ {data.index[-1].strftime('%Y-%m-%d')}")
                print(f"   価格範囲: ${data['Low'].min():.2f} ～ ${data['High'].max():.2f}")
            else:
                print(f"❌ {symbol}: データが空")
                
        except Exception as e:
            print(f"❌ {symbol}: エラー - {str(e)}")
        
        print()
        time.sleep(1)  # API制限回避
    
    # 結果サマリー
    print("📊 取得結果サマリー")
    print("-" * 30)
    
    for symbol, data in results.items():
        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            print(f"{symbol}: {len(data)}ヶ月分, 最新価格: ${latest_price:.2f}")
    
    print(f"\n🎉 テスト完了! {len(results)}/{len(symbols)} 銘柄取得成功")
    
    # モメンタム判定テスト
    if "IEF" in results and len(results["IEF"]) >= 2:
        print("\n🔍 モメンタム判定テスト")
        print("-" * 30)
        
        ief_data = results["IEF"]
        latest_return = ((ief_data['Open'].iloc[-1] - ief_data['Open'].iloc[-2]) / ief_data['Open'].iloc[-2]) * 100
        recommended = "TQQQ" if latest_return > 0 else "GLD"
        
        print(f"IEF 1ヶ月リターン: {latest_return:+.2f}%")
        print(f"推奨銘柄: {recommended}")
    
    return results

if __name__ == "__main__":
    test_etf_data()