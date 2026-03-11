import streamlit as st
import requests

API_URL="http://127.0.0.1:8000/predict"

st.set_page_config(page_icon= "📰",
                   layout="wide")
st.title("AI vs Human Misinformation Detection")
st.write("Enter text below to check whether it is AI-generated or Human-written" 
          "and whether it is Real or Fake"
          )
st.sidebar.title("About")

st.sidebar.info(
"""
This AI model detects:

• AI vs Human text  
• Fake vs Real information  

Model: BERT Transformer
"""
)

user_input = st.text_area("Enter Content:")
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #1E90FF;
    color: black;
    font-size: 16px;
    border-radius: 8px;
    height: 3em;
    width: 120px;
}
</style>
""", unsafe_allow_html=True)

if st.button("Predict"):
   if user_input.strip() == "":
       st.warning("Please enter some text")
   else:
         with st.spinner("Analyzing text..."):
               try:
                  response=requests.post(API_URL,json={"text":user_input})
        
                  if response.status_code == 200:
                     result = response.json()
                     source = result["source"]
                     truth = result["truth"]

                     st.subheader("Prediction Result:")

                     if source.lower() == "ai":
                        st.write("Source: AI Generated 🤖")
                     else:
                        st.write("Source: Human Written 👤")
                     if truth.lower() == "real":
                        st.markdown("<h3 style='color:green;'>This content appears to be Real ✅</h3>", unsafe_allow_html=True)
                     else:
                        st.markdown("<h3 style='color:red;'>This content contains misinformation ❌</h3>", unsafe_allow_html=True)
                     if st.button("Clear"):
                        st.experimental_rerun()
                  else:
                     st.error("API not running")
               except:
                  st.error("Cannot connect to FastAPI. Make sure the server is running.")  
   if st.button("submit",key="Clear"):
      st.experimental_rerun()