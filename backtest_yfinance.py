#!/usr/bin/env python3
"""
yfinanceを使用した3ヶ月リバランスバックテスト機能
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from yfinance_utils import get_etf_data

warnings.filterwarnings('ignore')

def get_monthly_data_for_backtest(start_date, end_date):
    """
    バックテスト用の月次データを取得
    
    Args:
        start_date (datetime): 開始日
        end_date (datetime): 終了日
    
    Returns:
        dict: {'IEF': df, 'TQQQ': df, 'GLD': df} または None
    """
    
    print(f"📊 バックテスト用データ取得: {start_date.strftime('%Y-%m-%d')} ～ {end_date.strftime('%Y-%m-%d')}")
    
    symbols = ['IEF', 'TQQQ', 'GLD']
    data = {}
    
    for symbol in symbols:
        print(f"   {symbol} データ取得中...")
        df = get_etf_data(symbol, start_date, end_date)
        
        if df is None or df.empty:
            print(f"   ❌ {symbol}: データ取得失敗")
            return None
        else:
            print(f"   ✅ {symbol}: {len(df)}期間")
            data[symbol] = df
    
    return data

def calculate_real_backtest(start_date, end_date):
    """
    リアルデータを使用した3ヶ月リバランスバックテスト
    
    Args:
        start_date (datetime): 開始日
        end_date (datetime): 終了日
    
    Returns:
        pd.DataFrame: バックテスト結果 または None
    """
    
    print("\n🚀 リアルデータバックテスト開始")
    print("=" * 50)
    
    # データ取得
    data = get_monthly_data_for_backtest(start_date, end_date)
    if data is None:
        print("❌ データ取得に失敗しました")
        return None
    
    ief_data = data['IEF']
    tqqq_data = data['TQQQ']
    gld_data = data['GLD']
    
    # データの整合性チェック
    min_periods = min(len(ief_data), len(tqqq_data), len(gld_data))
    if min_periods < 4:  # 最低4期間必要（判定期間1 + 保有期間3）
        print(f"❌ データが不足しています (取得期間: {min_periods})")
        return None
    
    print(f"✅ データ整合性確認: {min_periods}期間で分析")
    
    # 日付インデックスを統一
    common_dates = ief_data.index.intersection(tqqq_data.index).intersection(gld_data.index)
    
    if len(common_dates) < 4:
        print(f"❌ 共通期間が不足: {len(common_dates)}期間")
        return None
    
    print(f"📅 分析期間: {common_dates[0].strftime('%Y-%m-%d')} ～ {common_dates[-1].strftime('%Y-%m-%d')}")
    
    # バックテスト実行
    results = []
    
    for i in range(len(common_dates) - 3):  # 3ヶ月保有のため-3
        signal_date = common_dates[i]
        start_date_period = common_dates[i + 1]  # 実際の保有開始
        end_date_period = common_dates[i + 3]    # 3ヶ月後
        
        # IEFモメンタム信号計算
        if i == 0:
            # 最初の期間は前月データがないのでスキップ
            continue
            
        ief_current = ief_data.loc[signal_date, 'Open']
        ief_previous = ief_data.loc[common_dates[i-1], 'Open']
        ief_return = ((ief_current - ief_previous) / ief_previous) * 100
        
        # 推奨銘柄判定
        selected_etf = 'TQQQ' if ief_return > 0 else 'GLD'
        
        # パフォーマンス計算
        if selected_etf == 'TQQQ':
            start_price = tqqq_data.loc[start_date_period, 'Open']
            end_price = tqqq_data.loc[end_date_period, 'Open']
        else:  # GLD
            start_price = gld_data.loc[start_date_period, 'Open']
            end_price = gld_data.loc[end_date_period, 'Open']
        
        return_pct = ((end_price - start_price) / start_price) * 100
        
        results.append({
            'period': start_date_period.strftime('%Y/%m'),
            'signal_date': signal_date.strftime('%Y/%m/%d'),
            'ief_signal': ief_return,
            'selected_etf': selected_etf,
            'start_price': start_price,
            'end_price': end_price,
            'return_pct': return_pct,
            'start_date': start_date_period,
            'end_date': end_date_period
        })
        
        print(f"   📈 {start_date_period.strftime('%Y/%m')}: IEF{ief_return:+.1f}% → {selected_etf} → {return_pct:+.1f}%")
    
    if not results:
        print("❌ バックテスト結果が生成されませんでした")
        return None
    
    df = pd.DataFrame(results)
    print(f"\n✅ バックテスト完了: {len(df)}期間の結果を生成")
    
    return df

def compare_backtest_results(start_date, end_date):
    """
    リアルデータとサンプルデータのバックテスト結果を比較
    """
    
    print("\n📊 バックテスト結果比較")
    print("=" * 50)
    
    # リアルデータでのバックテスト
    real_results = calculate_real_backtest(start_date, end_date)
    
    if real_results is None:
        print("❌ リアルデータバックテストが失敗しました")
        return
    
    # サンプルデータでのバックテスト（既存機能）
    try:
        from app import get_sample_backtest_data
        sample_results = get_sample_backtest_data(start_date.date(), end_date.date())
        
        print(f"\n📈 結果比較:")
        print(f"   リアルデータ: {len(real_results)}期間")
        print(f"   サンプルデータ: {len(sample_results)}期間")
        
        if len(real_results) > 0:
            real_total_return = ((1 + real_results['return_pct'] / 100).prod() - 1) * 100
            real_avg_return = real_results['return_pct'].mean()
            real_win_rate = (real_results['return_pct'] > 0).mean() * 100
            
            print(f"\n💰 リアルデータ統計:")
            print(f"   総リターン: {real_total_return:+.1f}%")
            print(f"   平均リターン: {real_avg_return:+.1f}%")
            print(f"   勝率: {real_win_rate:.1f}%")
        
        if len(sample_results) > 0:
            sample_total_return = ((1 + sample_results['return_pct'] / 100).prod() - 1) * 100
            sample_avg_return = sample_results['return_pct'].mean()
            sample_win_rate = (sample_results['return_pct'] > 0).mean() * 100
            
            print(f"\n📋 サンプルデータ統計:")
            print(f"   総リターン: {sample_total_return:+.1f}%")
            print(f"   平均リターン: {sample_avg_return:+.1f}%")
            print(f"   勝率: {sample_win_rate:.1f}%")
        
    except Exception as e:
        print(f"⚠️ サンプルデータ比較でエラー: {e}")

if __name__ == "__main__":
    # テスト実行（2024年のデータで）
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    print("🧪 yfinanceバックテスト機能テスト")
    compare_backtest_results(start_date, end_date)