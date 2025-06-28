#!/usr/bin/env python3
"""
yfinance基本機能テスト
"""

import yfinance as yf
import pandas as pd

def test_yfinance():
    print("🧪 yfinance 接続テストを開始...")
    
    symbols = ["IEF", "TQQQ", "GLD"]
    
    for symbol in symbols:
        try:
            print(f"\n📊 {symbol} をテスト中...")
            
            # Ticker作成
            ticker = yf.Ticker(symbol)
            
            # 直近5日のデータ取得
            data = ticker.history(period="5d", interval="1d")
            
            if not data.empty:
                latest_price = data["Close"].iloc[-1]
                print(f"✅ {symbol}: {len(data)}日分のデータを取得")
                print(f"   最新価格: ${latest_price:.2f}")
                print(f"   最新日付: {data.index[-1].strftime('%Y-%m-%d')}")
            else:
                print(f"⚠️ {symbol}: データが空です")
                
        except Exception as e:
            print(f"❌ {symbol}: エラー - {str(e)[:100]}...")
    
    print("\n🚀 基本テスト完了！")

if __name__ == "__main__":
    test_yfinance()