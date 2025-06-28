import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 最小限の設定
st.set_page_config(
    page_title="ETF Momentum Checker",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 ETF Momentum Checker")
    st.write("アプリケーションが正常に起動しました！")
    
    # 基本情報表示
    st.header("🎯 現在の推奨銘柄")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("推奨銘柄", "TQQQ", delta="サンプル表示")
    with col2:
        st.metric("IEFリターン", "+0.50%", delta="モメンタム指標")
    with col3:
        st.metric("判定期間", "2024/11/01 ～ 2024/12/01")
    
    # サンプルデータの表示
    st.header("📊 サンプルバックテスト結果")
    
    # 静的サンプルデータ
    sample_data = {
        '開始月': ['2023-01', '2023-04', '2023-07', '2023-10'],
        '保有銘柄': ['TQQQ', 'GLD', 'TQQQ', 'GLD'],
        '保有開始価格': ['$25.50', '$180.20', '$28.90', '$185.50'],
        '保有終了価格': ['$32.10', '$175.80', '$31.40', '$191.20'],
        '損益率(%)': ['+25.9%', '-2.4%', '+8.7%', '+3.1%']
    }
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 統計情報
    st.header("📈 パフォーマンス統計")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総期間数", "4")
    with col2:
        st.metric("平均リターン", "8.8%")
    with col3:
        st.metric("勝率", "75.0%")
    with col4:
        st.metric("最大損失", "-2.4%")
    
    # 情報セクション
    with st.expander("ℹ️ アプリ情報"):
        st.write("""
        **ETF Momentum Checker v1.0.0**
        
        このアプリケーションは、IEFモメンタムに基づくTQQQ/GLD切り替え戦略を分析します。
        
        - **判定指標**: IEF 1ヶ月リターン
        - **選択ルール**: 正→TQQQ、負→GLD
        - **リバランス**: 3ヶ月ごと
        
        現在はサンプルデータを表示しています。
        """)
    
    # フッター
    st.markdown("---")
    st.markdown("🤖 Generated with Claude Code | 📱 iPhone対応")

if __name__ == "__main__":
    main()