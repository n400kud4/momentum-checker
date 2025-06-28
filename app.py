import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# yfinanceユーティリティをインポート
from yfinance_utils import (
    test_yfinance_connection, 
    calculate_ief_momentum_real,
    calculate_period_summary_real,
    get_etf_info
)
from backtest_yfinance import calculate_real_backtest

# 既存のサンプルデータ関数をインポート
from sample_data import get_sample_momentum_signal, get_sample_backtest_data

# ページ設定
st.set_page_config(
    page_title="ETF Momentum Checker - yfinance版",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # ヘッダー
    st.title("📈 ETF Momentum Checker - yfinance統合版")
    st.markdown("**IEFモメンタムに基づくTQQQ/GLD切り替え戦略（リアルデータ対応）**")
    st.markdown("---")
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ データソース設定")
        
        # データソース選択
        data_source = st.radio(
            "📊 使用するデータ",
            ["🔴 リアルデータ（yfinance）", "🔵 サンプルデータ"],
            index=0
        )
        
        st.markdown("---")
        
        # yfinance接続テスト
        if data_source == "🔴 リアルデータ（yfinance）":
            st.subheader("🧪 接続テスト")
            if st.button("yfinance接続確認", use_container_width=True):
                connection_ok = test_yfinance_connection()
                if connection_ok:
                    st.session_state['yfinance_ok'] = True
                else:
                    st.session_state['yfinance_ok'] = False
        
        st.markdown("---")
        
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
        
        if data_source == "🔴 リアルデータ（yfinance）":
            # yfinanceの場合はより広い期間
            min_date = datetime(2010, 3, 1)  # TQQQの開始日
            default_start = datetime(2020, 1, 1)
        else:
            # サンプルデータの場合
            min_date = datetime(2022, 1, 1)
            default_start = datetime(2023, 1, 1)
        
        start_date = st.date_input(
            "開始日",
            value=default_start,
            min_value=min_date,
            max_value=datetime.now()
        )
        end_date = st.date_input(
            "終了日",
            value=datetime.now(),
            min_value=start_date,
            max_value=datetime.now()
        )
        
        # 期間変更の説明
        st.caption("👆 期間を変更したら下のボタンで反映してください")
        
        # 再計算ボタン
        recalculate = st.button("🔄 期間変更を反映", type="primary", use_container_width=True)
        
        if recalculate:
            # キャッシュクリアして最新データで再計算
            st.cache_data.clear()
            # セッション状態をクリアして確実に再計算
            if 'last_calculation' in st.session_state:
                del st.session_state['last_calculation']
            st.success("✅ 期間を更新しました！キャッシュもクリアして最新データで再計算します。")
            st.balloons()
            st.rerun()
        
        # ETF情報
        st.markdown("---")
        st.subheader("📊 ETF情報")
        
        if st.button("ETF詳細を表示"):
            etf_info = get_etf_info()
            for symbol, info in etf_info.items():
                st.write(f"**{symbol}**: {info['name']}")
                st.caption(f"用途: {info['use']}")
    
    # メインコンテンツ
    # 1. 分析期間概要
    st.header("📊 分析期間概要")
    
    # ユーザー選択期間の表示
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())
    analysis_period = f"{start_date.strftime('%Y/%m/%d')} ～ {end_date.strftime('%Y/%m/%d')}"
    
    # データソースに応じて処理を分岐
    if data_source == "🔴 リアルデータ（yfinance）":
        if st.session_state.get('yfinance_ok', False):
            # 分析期間概要を計算
            strategy_summary, period = calculate_period_summary_real(start_datetime, end_datetime)
        else:
            st.warning("⚠️ yfinance接続テストを実行してください")
            strategy_summary = "サンプルデータでの概要"
            period = analysis_period
    else:
        # サンプルデータを使用
        strategy_summary = "サンプルデータでの概要"
        period = analysis_period
    
    # 分析期間情報表示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **📅 分析期間**
        
        {period}
        
        この期間でのトレード戦略を分析
        """)
    
    with col2:
        data_type = "リアルデータ" if data_source == "🔴 リアルデータ（yfinance）" else "サンプルデータ"
        st.info(f"""
        **📊 データソース**
        
        {data_type}
        
        3ヶ月リバランス戦略
        """)
    
    with col3:
        st.info(f"""
        **🎯 戦略概要**
        
        IEFモメンタム判定
        
        TQQQ ⇄ GLD 切り替え
        """)
    
    # 戦略説明
    st.info(f"""
    **📊 戦略ロジック**: 選択した分析期間 **{period}** で3ヶ月ごとにリバランスしてトレードした結果を表示
    """)
    
    # 最新推奨銘柄セクション（現在の市況用）
    if data_source == "🔴 リアルデータ（yfinance）" and st.session_state.get('yfinance_ok', False):
        with st.expander("📈 現在の最新推奨銘柄 (参考)", expanded=False):
            st.caption("分析期間とは別に、現在の市況での推奨銘柄")
            current_etf, current_return, current_period = calculate_ief_momentum_real()
            if current_etf:
                col1, col2 = st.columns(2)
                with col1:
                    if current_etf == "TQQQ":
                        st.success(f"🚀 {current_etf}")
                    else:
                        st.warning(f"🥇 {current_etf}")
                with col2:
                    st.metric("IEF リターン", f"{current_return:+.2f}%")
                st.caption(f"判定期間: {current_period}")
    
    st.markdown("---")
    
    # 2. バックテスト結果
    st.header("📊 バックテスト結果（3ヶ月リバランス）")
    
    # データソースに応じてバックテスト実行
    if data_source == "🔴 リアルデータ（yfinance）" and st.session_state.get('yfinance_ok', False):
        st.info("🚀 リアルデータでバックテストを実行中...")
        
        # リアルデータでバックテスト
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.min.time())
        
        backtest_df = calculate_real_backtest(start_datetime, end_datetime)
        
        if backtest_df is None:
            st.error("❌ リアルデータでのバックテストに失敗しました。サンプルデータを表示します。")
            backtest_df = get_sample_backtest_data(start_date, end_date)
        else:
            st.success(f"✅ リアルデータでバックテスト完了！ {len(backtest_df)}期間を分析")
    else:
        # サンプルデータでバックテスト
        if data_source == "🔴 リアルデータ（yfinance）":
            st.warning("⚠️ yfinance接続テストを先に実行してください")
        backtest_df = get_sample_backtest_data(start_date, end_date)
    
    # 期間に該当するデータがない場合の処理
    if backtest_df.empty:
        st.warning(f"⚠️ 指定期間（{start_date} ～ {end_date}）にデータがありません。期間を調整してください。")
        if data_source == "🔵 サンプルデータ":
            st.info("💡 サンプルデータ利用可能期間: 2022年1月 ～ 2024年10月")
        else:
            st.info("💡 リアルデータ利用可能期間: 2010年3月 ～ 現在")
        return
    
    # 期間情報を表示
    st.info(f"📅 分析期間: {start_date} ～ {end_date} | 該当期間数: {len(backtest_df)}期間")
    
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
    
    # フッター
    st.markdown("---")
    with st.expander("ℹ️ yfinance統合について"):
        st.write("""
        **🚧 開発段階**
        
        **Phase 1✅完了**: 基本データ取得機能
        - yfinance接続テスト
        - リアルタイム推奨銘柄判定
        - エラーハンドリング
        
        **Phase 2✅完了**: モメンタム計算の完全実装
        **Phase 3✅完了**: リアルデータでの完全バックテスト
        **Phase 4（最終）**: 本番デプロイ
        
        現在のデータソース: {data_source}
        """)
    
    st.markdown("🤖 **ETF Momentum Checker v1.1-dev** | 📱 iPhone対応 | 🌐 yfinance統合")

if __name__ == "__main__":
    main()