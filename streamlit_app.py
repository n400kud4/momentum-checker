import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ETF Momentum Checker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=1800)  # 30分キャッシュ
def get_monthly_data(symbol, start_date, end_date):
    """ETFの月次データを取得"""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date, interval="1mo")
        
        if data.empty:
            return None
            
        # タイムゾーン正規化
        if data.index.tz is not None:
            data.index = data.index.tz_localize(None)
            
        return data
        
    except Exception as e:
        st.error(f"❌ {symbol} データ取得エラー: {str(e)}")
        return None

def calculate_momentum_signal():
    """現在のモメンタムシグナルを計算"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    ief_data = get_monthly_data("IEF", start_date, end_date)
    
    if ief_data is None or len(ief_data) < 2:
        return None, None, None
    
    # 最新の1ヶ月リターン
    latest_return = ((ief_data['Open'].iloc[-1] - ief_data['Open'].iloc[-2]) / ief_data['Open'].iloc[-2]) * 100
    recommended_etf = "TQQQ" if latest_return > 0 else "GLD"
    period = f"{ief_data.index[-2].strftime('%Y/%m/%d')} ～ {ief_data.index[-1].strftime('%Y/%m/%d')}"
    
    return recommended_etf, latest_return, period

def perform_backtest(start_date, end_date):
    """バックテストを実行"""
    # プログレスバー
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # データ取得
    status_text.text("📊 IEFデータ取得中...")
    ief_data = get_monthly_data("IEF", start_date, end_date)
    progress_bar.progress(25)
    
    if ief_data is None:
        st.error("IEFデータの取得に失敗しました")
        return None
    
    time.sleep(1)
    status_text.text("📊 TQQQデータ取得中...")
    tqqq_data = get_monthly_data("TQQQ", start_date, end_date)
    progress_bar.progress(50)
    
    if tqqq_data is None:
        st.error("TQQQデータの取得に失敗しました")
        return None
    
    time.sleep(1)
    status_text.text("📊 GLDデータ取得中...")
    gld_data = get_monthly_data("GLD", start_date, end_date)
    progress_bar.progress(75)
    
    if gld_data is None:
        st.error("GLDデータの取得に失敗しました")
        return None
    
    status_text.text("📊 バックテスト計算中...")
    
    # バックテスト計算
    results = []
    current_date = pd.to_datetime(start_date).normalize()
    end_date_pd = pd.to_datetime(end_date).normalize()
    
    while current_date < end_date_pd:
        next_date = current_date + pd.DateOffset(months=3)
        if next_date > end_date_pd:
            next_date = end_date_pd
        
        # 期間内のデータを取得
        period_ief = ief_data[(ief_data.index >= current_date) & (ief_data.index < next_date)]
        
        if len(period_ief) >= 2:
            # IEFリターンで判定
            ief_return = ((period_ief['Open'].iloc[1] - period_ief['Open'].iloc[0]) / period_ief['Open'].iloc[0]) * 100
            selected_etf = "TQQQ" if ief_return > 0 else "GLD"
            
            # 対応するETFデータ
            if selected_etf == "TQQQ":
                etf_data = tqqq_data[(tqqq_data.index >= current_date) & (tqqq_data.index < next_date)]
            else:
                etf_data = gld_data[(gld_data.index >= current_date) & (gld_data.index < next_date)]
            
            if len(etf_data) >= 2:
                start_price = etf_data['Open'].iloc[0]
                end_price = etf_data['Open'].iloc[-1]
                returns = ((end_price - start_price) / start_price) * 100
                
                results.append({
                    'date': current_date,
                    'period': current_date.strftime('%Y-%m'),
                    'etf': selected_etf,
                    'start_price': start_price,
                    'end_price': end_price,
                    'return_pct': returns,
                    'ief_signal': ief_return
                })
        
        current_date = next_date
    
    progress_bar.progress(100)
    status_text.text("✅ 完了!")
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()
    
    return pd.DataFrame(results)

def create_performance_chart(backtest_df):
    """パフォーマンスチャートを作成"""
    if backtest_df.empty:
        return None
    
    # 累積リターンを計算
    backtest_df['cumulative_return'] = (1 + backtest_df['return_pct'] / 100).cumprod()
    
    fig = go.Figure()
    
    # 累積リターンライン
    fig.add_trace(go.Scatter(
        x=backtest_df['date'],
        y=backtest_df['cumulative_return'],
        mode='lines+markers',
        name='累積リターン',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # ETF切り替えポイントの色分け
    colors = {'TQQQ': '#ff7f0e', 'GLD': '#2ca02c'}
    for etf in ['TQQQ', 'GLD']:
        etf_data = backtest_df[backtest_df['etf'] == etf]
        if not etf_data.empty:
            fig.add_trace(go.Scatter(
                x=etf_data['date'],
                y=etf_data['cumulative_return'],
                mode='markers',
                name=f'{etf} 保有期間',
                marker=dict(color=colors[etf], size=12, symbol='square'),
                showlegend=True
            ))
    
    fig.update_layout(
        title='📈 累積パフォーマンス',
        xaxis_title='期間',
        yaxis_title='累積リターン（倍率）',
        hovermode='x unified',
        height=500
    )
    
    return fig

def main():
    # ヘッダー
    st.title("📈 ETF Momentum Checker")
    st.markdown("IEFモメンタムに基づくTQQQ/GLD切り替え戦略")
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # 期間設定
        st.subheader("📅 バックテスト期間")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "開始日",
                value=datetime(2020, 1, 1),
                min_value=datetime(2010, 1, 1),
                max_value=datetime.now()
            )
        with col2:
            end_date = st.date_input(
                "終了日",
                value=datetime.now(),
                min_value=start_date,
                max_value=datetime.now()
            )
        
        # 実行ボタン
        run_backtest = st.button("🚀 バックテスト実行", type="primary")
        
        # 情報表示
        st.markdown("---")
        st.subheader("ℹ️ 戦略情報")
        st.write("**判定指標**: IEF 1ヶ月リターン")
        st.write("**選択ルール**: 正→TQQQ、負→GLD")
        st.write("**リバランス**: 3ヶ月ごと")
        st.write("**データ**: 月次始値")
    
    # メインコンテンツ
    # 現在の推奨銘柄
    st.header("🎯 現在の推奨銘柄")
    
    with st.spinner("最新データを取得中..."):
        recommended_etf, ief_return, period = calculate_momentum_signal()
    
    if recommended_etf:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if recommended_etf == "TQQQ":
                st.success(f"### 🚀 {recommended_etf}")
                st.write("**3倍レバレッジNASDAQ**")
            else:
                st.warning(f"### 🥇 {recommended_etf}")
                st.write("**ゴールドETF**")
        
        with col2:
            delta_color = "normal" if ief_return > 0 else "inverse"
            st.metric(
                "IEFリターン",
                f"{ief_return:+.2f}%",
                delta="モメンタム指標",
                delta_color=delta_color
            )
        
        with col3:
            st.info(f"**判定期間**\n{period}")
    else:
        st.error("現在のデータを取得できませんでした")
    
    st.markdown("---")
    
    # バックテスト結果
    if run_backtest:
        st.header("📊 バックテスト結果")
        
        backtest_df = perform_backtest(start_date, end_date)
        
        if backtest_df is not None and not backtest_df.empty:
            # パフォーマンスチャート
            fig = create_performance_chart(backtest_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            
            # 統計情報
            st.subheader("📈 パフォーマンス統計")
            
            returns = backtest_df['return_pct']
            total_return = ((1 + returns / 100).prod() - 1) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("総期間数", len(backtest_df))
            with col2:
                st.metric("平均リターン", f"{returns.mean():.2f}%")
            with col3:
                st.metric("勝率", f"{(returns > 0).mean() * 100:.1f}%")
            with col4:
                st.metric("総リターン", f"{total_return:.1f}%")
            
            # 詳細テーブル
            st.subheader("📋 詳細履歴")
            
            # 表示用データフレーム
            display_df = backtest_df.copy()
            display_df['開始月'] = display_df['period']
            display_df['保有銘柄'] = display_df['etf']
            display_df['保有開始価格'] = display_df['start_price'].apply(lambda x: f"${x:.2f}")
            display_df['保有終了価格'] = display_df['end_price'].apply(lambda x: f"${x:.2f}")
            display_df['損益率(%)'] = display_df['return_pct'].apply(lambda x: f"{x:+.2f}%")
            
            st.dataframe(
                display_df[['開始月', '保有銘柄', '保有開始価格', '保有終了価格', '損益率(%)']],
                use_container_width=True,
                hide_index=True
            )
            
            # CSV出力
            csv = display_df[['開始月', '保有銘柄', '保有開始価格', '保有終了価格', '損益率(%)']].to_csv(index=False)
            st.download_button(
                label="📥 CSV形式でダウンロード",
                data=csv,
                file_name=f"momentum_backtest_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
        else:
            st.error("バックテストの実行に失敗しました")
    
    else:
        st.info("👈 サイドバーの「バックテスト実行」ボタンを押してください")
    
    # フッター
    st.markdown("---")
    with st.expander("ℹ️ 免責事項"):
        st.write("""
        このアプリケーションは教育・研究目的で作成されています。
        投資判断は自己責任で行ってください。過去のパフォーマンスは将来の結果を保証するものではありません。
        """)

if __name__ == "__main__":
    main()