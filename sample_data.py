"""
サンプルデータ関数
yfinance統合版アプリで使用するサンプルデータ機能
"""

import pandas as pd
from datetime import datetime

def get_sample_momentum_signal():
    """サンプルのモメンタムシグナル（後でyfinanceに置き換え）"""
    # サンプルデータ：IEF 1ヶ月リターン
    ief_return = 0.75  # +0.75%の例
    recommended_etf = "TQQQ" if ief_return > 0 else "GLD"
    period = "2024/11/01 ～ 2024/12/01"
    
    return recommended_etf, ief_return, period

def get_sample_backtest_data(start_date, end_date):
    """サンプルバックテストデータ（Core Strategy Logic に基づく）"""
    # より多くのサンプルデータを用意
    all_backtest_data = [
        {
            "period": "2022-01",
            "date": datetime(2022, 1, 1),
            "ief_signal": 0.8,
            "selected_etf": "TQQQ",
            "start_price": 38.20,
            "end_price": 32.10,
            "return_pct": -16.0
        },
        {
            "period": "2022-04", 
            "date": datetime(2022, 4, 1),
            "ief_signal": -1.5,
            "selected_etf": "GLD",
            "start_price": 172.30,
            "end_price": 177.80,
            "return_pct": 3.2
        },
        {
            "period": "2022-07",
            "date": datetime(2022, 7, 1),
            "ief_signal": 1.1,
            "selected_etf": "TQQQ", 
            "start_price": 22.90,
            "end_price": 26.40,
            "return_pct": 15.3
        },
        {
            "period": "2022-10",
            "date": datetime(2022, 10, 1),
            "ief_signal": -0.7,
            "selected_etf": "GLD",
            "start_price": 165.50,
            "end_price": 172.20,
            "return_pct": 4.0
        },
        {
            "period": "2023-01",
            "date": datetime(2023, 1, 1),
            "ief_signal": 1.2,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ",
            "start_price": 25.50,
            "end_price": 32.10,
            "return_pct": 25.9
        },
        {
            "period": "2023-04", 
            "date": datetime(2023, 4, 1),
            "ief_signal": -0.8,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 180.20,
            "end_price": 175.80,
            "return_pct": -2.4
        },
        {
            "period": "2023-07",
            "date": datetime(2023, 7, 1),
            "ief_signal": 0.6,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ", 
            "start_price": 28.90,
            "end_price": 31.40,
            "return_pct": 8.7
        },
        {
            "period": "2023-10",
            "date": datetime(2023, 10, 1),
            "ief_signal": -0.3,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 185.50,
            "end_price": 191.20,
            "return_pct": 3.1
        },
        {
            "period": "2024-01",
            "date": datetime(2024, 1, 1),
            "ief_signal": 1.5,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ",
            "start_price": 35.20,
            "end_price": 42.80,
            "return_pct": 21.6
        },
        {
            "period": "2024-04",
            "date": datetime(2024, 4, 1),
            "ief_signal": -1.1,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 195.30,
            "end_price": 188.90,
            "return_pct": -3.3
        },
        {
            "period": "2024-07",
            "date": datetime(2024, 7, 1),
            "ief_signal": 0.9,
            "selected_etf": "TQQQ",
            "start_price": 44.20,
            "end_price": 47.50,
            "return_pct": 7.5
        },
        {
            "period": "2024-10",
            "date": datetime(2024, 10, 1),
            "ief_signal": -0.4,
            "selected_etf": "GLD",
            "start_price": 192.10,
            "end_price": 196.30,
            "return_pct": 2.2
        }
    ]
    
    df = pd.DataFrame(all_backtest_data)
    
    # 指定期間でフィルタリング
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    return filtered_df