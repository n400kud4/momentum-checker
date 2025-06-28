import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(
    page_title="ETF Momentum Checker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_sample_momentum_signal():
    """サンプルのモメンタムシグナル（後でyfinanceに置き換え）"""
    # サンプルデータ：IEF 1ヶ月リターン
    ief_return = 0.75  # +0.75%の例
    recommended_etf = "TQQQ" if ief_return > 0 else "GLD"
    period = "2024/11/01 ～ 2024/12/01"
    
    return recommended_etf, ief_return, period

def get_sample_backtest_data():
    """サンプルバックテストデータ（Core Strategy Logic に基づく）"""
    # 3ヶ月リバランス戦略のサンプルデータ
    backtest_data = [
        {
            "period": "2023-01",
            "ief_signal": 1.2,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ",
            "start_price": 25.50,
            "end_price": 32.10,
            "return_pct": 25.9
        },
        {
            "period": "2023-04", 
            "ief_signal": -0.8,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 180.20,
            "end_price": 175.80,
            "return_pct": -2.4
        },
        {
            "period": "2023-07",
            "ief_signal": 0.6,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ", 
            "start_price": 28.90,
            "end_price": 31.40,
            "return_pct": 8.7
        },
        {
            "period": "2023-10",
            "ief_signal": -0.3,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 185.50,
            "end_price": 191.20,
            "return_pct": 3.1
        },
        {
            "period": "2024-01",
            "ief_signal": 1.5,  # IEF 1ヶ月リターン（正 → TQQQ選択）
            "selected_etf": "TQQQ",
            "start_price": 35.20,
            "end_price": 42.80,
            "return_pct": 21.6
        },
        {
            "period": "2024-04",
            "ief_signal": -1.1,  # IEF 1ヶ月リターン（負 → GLD選択）
            "selected_etf": "GLD",
            "start_price": 195.30,
            "end_price": 188.90,
            "return_pct": -3.3
        }
    ]
    
    return pd.DataFrame(backtest_data)

def main():
    # ヘッダー
    st.title("📈 ETF Momentum Checker")
    st.markdown("**IEFモメンタムに基づくTQQQ/GLD切り替え戦略**")
    st.markdown("---")
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 戦略設定")
        
        # 戦略情報
        st.subheader("📋 Strategy Logic")
        st.write("**1. データ収集**: IEF, TQQQ, GLD月次始値")
        st.write("**2. モメンタム判定**: IEF 1ヶ月リターン")
        st.write("**3. 銘柄選択**: 正→TQQQ, 負→GLD")
        st.write("**4. リバランス**: 3ヶ月周期")
        st.write("**5. 計算**: (売値-買値)/買値 × 100")
        
        st.markdown("---")
        
        # 期間設定
        st.subheader("📅 分析期間")
        start_date = st.date_input(
            "開始日",
            value=datetime(2023, 1, 1),
            min_value=datetime(2020, 1, 1),
            max_value=datetime.now()
        )
        end_date = st.date_input(
            "終了日",
            value=datetime.now(),
            min_value=start_date,
            max_value=datetime.now()
        )
        
        # データソース
        st.subheader("📊 データソース")
        st.write("🔹 **TQQQ**: 3倍レバレッジNASDAQ ETF")
        st.write("🔹 **GLD**: ゴールド ETF")  
        st.write("🔹 **IEF**: 中期米国債 ETF（判定指標）")
        
        st.markdown("---")
        st.caption("現在はサンプルデータを表示")
    
    # メインコンテンツ
    # 1. 現在の推奨銘柄
    st.header("🎯 現在の推奨銘柄")
    
    recommended_etf, ief_return, period = get_sample_momentum_signal()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if recommended_etf == "TQQQ":
            st.success(f"### 🚀 {recommended_etf}")
            st.write("**ProShares UltraPro QQQ**")
            st.write("NASDAQ 100 × 3倍レバレッジ")
        else:
            st.warning(f"### 🥇 {recommended_etf}")
            st.write("**SPDR Gold Trust**")
            st.write("金価格連動ETF")
    
    with col2:
        delta_color = "normal" if ief_return > 0 else "inverse"
        st.metric(
            "IEF 1ヶ月リターン",
            f"{ief_return:+.2f}%",
            delta="モメンタム指標",
            delta_color=delta_color
        )
    
    with col3:
        st.info(f"**判定期間**\n\n{period}")
    
    # 判定ロジックの説明
    st.info(f"""
    **📊 判定ロジック**: IEF 1ヶ月リターンが **{ief_return:+.2f}%** → 
    {'**正の値**なのでTQQQ（成長資産）を選択' if ief_return > 0 else '**負の値**なのでGLD（安全資産）を選択'}
    """)
    
    st.markdown("---")
    
    # 2. バックテスト結果
    st.header("📊 バックテスト結果（3ヶ月リバランス）")
    
    # データ取得
    backtest_df = get_sample_backtest_data()
    
    # 表示用データフレーム作成
    display_df = backtest_df.copy()
    display_df['開始月'] = display_df['period']
    display_df['IEF信号(%)'] = display_df['ief_signal'].apply(lambda x: f"{x:+.1f}%")
    display_df['保有銘柄'] = display_df['selected_etf']
    display_df['開始価格'] = display_df['start_price'].apply(lambda x: f"${x:.2f}")
    display_df['終了価格'] = display_df['end_price'].apply(lambda x: f"${x:.2f}")
    display_df['損益率(%)'] = display_df['return_pct'].apply(lambda x: f"{x:+.1f}%")
    
    # テーブル表示
    st.dataframe(
        display_df[['開始月', 'IEF信号(%)', '保有銘柄', '開始価格', '終了価格', '損益率(%)']],
        use_container_width=True,
        hide_index=True
    )
    
    # 3. パフォーマンス統計
    st.header("📈 パフォーマンス統計")
    
    returns = backtest_df['return_pct']
    total_periods = len(backtest_df)
    avg_return = returns.mean()
    win_rate = (returns > 0).mean() * 100
    max_gain = returns.max()
    max_loss = returns.min()
    total_return = ((1 + returns / 100).prod() - 1) * 100
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("総期間数", f"{total_periods}")
    
    with col2:
        st.metric("平均リターン", f"{avg_return:.1f}%")
    
    with col3:
        st.metric("勝率", f"{win_rate:.1f}%")
    
    with col4:
        st.metric("最大利益", f"{max_gain:+.1f}%")
    
    with col5:
        st.metric("最大損失", f"{max_loss:+.1f}%")
    
    # 総合リターン
    st.subheader("💰 累積パフォーマンス")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "総リターン", 
            f"{total_return:+.1f}%",
            delta=f"{total_periods}期間の累積"
        )
    
    with col2:
        annual_return = (((1 + total_return / 100) ** (4 / total_periods)) - 1) * 100
        st.metric(
            "年率リターン（推定）",
            f"{annual_return:+.1f}%",
            delta="年率換算"
        )
    
    # 4. 戦略の詳細説明
    st.markdown("---")
    st.header("💡 戦略の仕組み")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 リバランス周期")
        st.write("""
        **3ヶ月ごとにポジション見直し**
        - 各期間開始時にIEFの1ヶ月リターンを計算
        - 正の場合：TQQQ（攻撃的成長）
        - 負の場合：GLD（守備的安全）
        - 3ヶ月間はポジション維持
        """)
    
    with col2:
        st.subheader("📊 判定指標")
        st.write("""
        **IEF（中期米国債ETF）をモメンタム指標として使用**
        - 債券価格上昇→金利低下→成長株に有利→TQQQ
        - 債券価格下落→金利上昇→安全資産に有利→GLD
        - 月次始値ベースで正確な計算
        """)
    
    # CSV出力
    st.markdown("---")
    csv = display_df[['開始月', 'IEF信号(%)', '保有銘柄', '開始価格', '終了価格', '損益率(%)']].to_csv(index=False)
    st.download_button(
        label="📥 CSV形式でダウンロード",
        data=csv,
        file_name=f"momentum_backtest_{start_date}_{end_date}.csv",
        mime="text/csv"
    )
    
    # フッター
    st.markdown("---")
    with st.expander("ℹ️ 免責事項"):
        st.write("""
        **免責事項**
        
        このアプリケーションは教育・研究目的で作成されています。
        - 投資判断は自己責任で行ってください
        - 過去のパフォーマンスは将来の結果を保証しません
        - 現在はサンプルデータを使用しています
        
        **次回アップデート**: リアルタイムデータ取得機能
        """)
    
    st.markdown("🤖 **ETF Momentum Checker v1.0** | 📱 iPhone対応 | 🌐 Streamlit Cloud")

if __name__ == "__main__":
    main()