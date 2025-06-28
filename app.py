import streamlit as st

def main():
    st.title("ETF Momentum Checker")
    st.write("Hello from ETF Momentum Checker!")
    
    if st.button("Test Button"):
        st.success("Success! App is working correctly.")
        st.balloons()

if __name__ == "__main__":
    main()