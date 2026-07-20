import streamlit as st
import numpy as np
import pickle
import base64
st.set_page_config(page_title="Dream House", layout="centered")
st.markdown("""
<style>
/* Force all the text black */
body, .stApp, label, h1, h2, h3, p {color: black !important; }

/* Force inputs white bg + black text */
div[data-baseweb="input"] input {
    color: black !important;
    background-color: white !important;
}

div[data-baseweb="input"] {background-color: white !important;}

/* Force button - works in both modes */
div.stButton > button,
div[data-tested="stFormSubmitButton"] > button {
    background: white !important;
    background-color: black !important;
    border: 1px solid #cccccc !important;
    border_radius: 8px;
    font-weight: bold;
}
div.stButton > button:hover 
div[data-tested="stFormSumitButton"] > button:hover {
    background: #f5f5f5 !important;
    backgroun-color: #f5f5f5 !important;
}
</style>
""", unsafe_allow_html=True)
try:
    model=pickle.load(open("house_model.pkl","rb"))
except Exception as e:
    st.error(f"Error loading model: {e}")

 # keeping background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
          encoded=base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:url("data:image/jpeg;base64,{encoded}");
            background-size:cover; 
            color: black !important;
        }}
        label, h1, h2, h3, p{{
            color: black !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local("Houseimage.jpeg")

st.title("🏡Dream House")
st.subheader("House Price Prediction App")
st.markdown("This app predicts the price of your Dream House using Machine Learning Algorithm, LinearRegression")
st.divider()
st.markdown("<p style='font-size:25px;'>Enter the details below.</p>", unsafe_allow_html=True)
st.markdown(""" 
<style> 
label {
    font-size: 30px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)
area=st.number_input("**Area in sqft**", step=1, min_value=0, format="%d")
area=int(area)
bedrooms=st.number_input("**Number Of Bedrooms**", step=1, min_value=0, format="%d")
bedrooms=int(bedrooms)
bathrooms=st.number_input("**Number Of Bathrooms**", step=1, min_value=0, format="%d")
bathrooms=int(bathrooms)
stories=st.number_input("**Number Of Stories**", step=1, min_value=0, format="%d")
stories=int(stories)
parking=st.number_input("**Number Of Parking area**", step=1, min_value=0, format="%d")
parking=int(parking)
feature=[[area , bedrooms , bathrooms , stories , parking]]

# Initialize session state
with st.form("predicted_form"):
    submitted = st.form_submit_button("💰**Predict Price**", type="primary")

if submitted:
    if area > 0:  #if statement to check whether the input is valid or not.
        Prediction=model.predict(feature)
        st.session_state['predicted']=True
        st.session_state['price']=Prediction[0]
    else:
        st.error("Oops😟, Try Again")
        st.session_state['predicted'] = False

# 2. Show result + slider only if we have predicted
if st.session_state.get('predicted', False):
        st.success(f"**Your Predicted Price will be: ₹{st.session_state['price']:,.2f}**")
        st.write("**Thank You for spending your time with us🙏.**")

        # 4. Slider with key + f-string to show stars
        rating=st.slider("**Rate this Prediction**", 1, 5, value=1, step = 1, key="rating_slider")
        st.write(f"**Your Rating:** ","⭐" * rating)   # <- f before " is important
    

    
