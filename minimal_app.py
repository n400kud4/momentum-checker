import streamlit as st
import subprocess
import sys

st.title("🧪 Momentum Checker - Minimal")

if st.button("🚀 データテスト実行"):
    with st.spinner("テスト実行中..."):
        try:
            result = subprocess.run([sys.executable, "direct_test.py"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                st.success("✅ テスト成功!")
                st.code(result.stdout)
            else:
                st.error("❌ テスト失敗")
                st.code(result.stderr)
                
        except Exception as e:
            st.error(f"実行エラー: {str(e)}")

st.info("👆 ボタンを押してETFデータの取得テストを実行します")