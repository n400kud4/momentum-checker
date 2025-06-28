#!/usr/bin/env python3
"""
IEFモメンタム判定ロジックのテスト
リアルデータとサンプルデータの比較
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import warnings

# yfinance_utilsから関数をインポート
from yfinance_utils import calculate_ief_momentum_real
from app import get_sample_momentum_signal

warnings.filterwarnings('ignore')

def test_momentum_comparison():
    """リアルデータとサンプルデータのモメンタム判定を比較"""
    
    print("🧪 IEFモメンタム判定ロジック比較テスト")
    print("=" * 50)
    
    # 1. サンプルデータでの判定
    print("\n📘 1. サンプルデータでの判定:")
    try:
        sample_etf, sample_return, sample_period = get_sample_momentum_signal()
        print(f"   推奨銘柄: {sample_etf}")
        print(f"   IEFリターン: {sample_return:+.2f}%")
        print(f"   判定期間: {sample_period}")
    except Exception as e:
        print(f"   ❌ エラー: {e}")
        sample_etf, sample_return = None, None
    
    # 2. リアルデータでの判定
    print("\n📊 2. リアルデータでの判定:")
    try:
        real_etf, real_return, real_period = calculate_ief_momentum_real()
        if real_etf is not None:
            print(f"   推奨銘柄: {real_etf}")
            print(f"   IEFリターン: {real_return:+.2f}%")
            print(f"   判定期間: {real_period}")
        else:
            print("   ❌ リアルデータ取得に失敗")
            real_etf, real_return = None, None
    except Exception as e:
        print(f"   ❌ エラー: {e}")
        real_etf, real_return = None, None
    
    # 3. 比較結果
    print("\n📈 3. 比較結果:")
    if sample_etf and real_etf:
        print(f"   サンプル判定: {sample_etf} (IEF: {sample_return:+.2f}%)")
        print(f"   リアル判定:   {real_etf} (IEF: {real_return:+.2f}%)")
        
        if sample_etf == real_etf:
            print("   ✅ 判定結果が一致しています！")
        else:
            print("   ⚠️ 判定結果が異なります")
            print("   　→ これは期間やデータの違いによる正常な現象です")
        
        # リターンの差を確認
        return_diff = abs(real_return - sample_return)
        print(f"   📊 IEFリターン差: {return_diff:.2f}ポイント")
        
    else:
        print("   ❌ 比較できませんでした")
    
    print("\n" + "=" * 50)

def test_detailed_ief_data():
    """IEFの詳細データを確認"""
    
    print("\n🔍 IEF詳細データ分析")
    print("=" * 50)
    
    try:
        # 直近3ヶ月のIEFデータを取得
        end_date = datetime.now()
        start_date = end_date - timedelta(days=120)
        
        print(f"📅 取得期間: {start_date.strftime('%Y-%m-%d')} ～ {end_date.strftime('%Y-%m-%d')}")
        
        # IEFデータ取得
        ief = yf.Ticker("IEF")
        data = ief.history(
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            interval="1mo",
            auto_adjust=True
        )
        
        if data.empty:
            print("❌ IEFデータが取得できませんでした")
            return
        
        # タイムゾーン正規化
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)
        
        print(f"✅ {len(data)}期間のデータを取得")
        print("\n📊 直近のIEF月次データ:")
        
        # 直近5期間を表示
        recent_data = data.tail(5)
        for i, (date, row) in enumerate(recent_data.iterrows()):
            print(f"   {date.strftime('%Y-%m-%d')}: Open=${row['Open']:.2f}, Close=${row['Close']:.2f}")
        
        # 1ヶ月リターン計算
        if len(data) >= 2:
            latest_open = data['Open'].iloc[-1]
            previous_open = data['Open'].iloc[-2]
            return_pct = ((latest_open - previous_open) / previous_open) * 100
            
            print(f"\n💰 1ヶ月リターン計算:")
            print(f"   前月始値: ${previous_open:.2f} ({data.index[-2].strftime('%Y-%m-%d')})")
            print(f"   今月始値: ${latest_open:.2f} ({data.index[-1].strftime('%Y-%m-%d')})")
            print(f"   リターン: {return_pct:+.2f}%")
            
            recommended = "TQQQ" if return_pct > 0 else "GLD"
            print(f"   推奨銘柄: {recommended}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    test_momentum_comparison()
    test_detailed_ief_data()
    print("\n🚀 モメンタム判定テスト完了！")