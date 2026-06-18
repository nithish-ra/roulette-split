import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import random
import time

# ==========================================
# CONFIGURATION
# ==========================================
genai.configure(api_key="ur api key") 

st.set_page_config(page_title="Roulette Split", page_icon="💸", layout="centered")
st.title("💸 Roulette Split & Tracker")

# App Memory (Session State)
if "bill_data" not in st.session_state:
    st.session_state.bill_data = None
if "loser" not in st.session_state:
    st.session_state.loser = None

tab1, tab2 = st.tabs(["📸 Take Photo", "📁 Upload File"])
receipt_image = None

with tab1:
    camera_image = st.camera_input("Snap a picture of the receipt")
    if camera_image: receipt_image = camera_image

with tab2:
    uploaded_file = st.file_uploader("Upload a receipt image", type=["png", "jpg", "jpeg"])
    if uploaded_file: receipt_image = uploaded_file

# ==========================================
# Phase 2: AI EXTRACTION
# ==========================================
if receipt_image:
    st.image(Image.open(receipt_image), caption="Your Receipt", width=250)
    
    if st.button("Extract Bill Data 🧠", type="primary"):
        with st.spinner("Reading the receipt with AI..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = """
                Analyze this receipt carefully. Return a strictly formatted JSON object containing:
                1. "store_name": The name of the store.
                2. "items": A list of objects, each with "name" (string) and "price" (number).
                3. "total": The final total amount paid (number).
                Do not include markdown.
                """
                response = model.generate_content([prompt, Image.open(receipt_image)])
                
                # Save data to the app's memory so it survives button clicks
                st.session_state.bill_data = json.loads(response.text.strip())
                st.session_state.loser = None # Reset game on new bill
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# ==========================================
# Phase 3: BILL ROULETTE GAME
# ==========================================
if st.session_state.bill_data:
    data = st.session_state.bill_data
    total_bill = data.get("total", 0)
    
    st.divider()
    st.header(f"🎯 Bill Roulette: {data.get('store_name', 'Store')}")
    st.subheader(f"Total on the line: ₹{total_bill}")
    
    # Game Inputs
    friends_input = st.text_input("Who is splitting? (Separate names by commas)", "Nithish, Alice, Bob, Charlie")
    friends_list = [name.strip() for name in friends_input.split(",") if name.strip()]
    
    multiplier = st.selectbox("Select the Penalty 😈", ["2x Share", "3x Share", "Fully (100%)"])
    
    # Spin Button
    if st.button("🎰 Spin the Wheel!", use_container_width=True):
        if len(friends_list) < 2:
            st.warning("You need at least 2 people to play Roulette!")
        else:
            with st.spinner("Spinning the wheel of destiny..."):
                time.sleep(1.5) # Add a little dramatic suspense
                st.session_state.loser = random.choice(friends_list)
    
    # Display Results if a loser has been chosen
    if st.session_state.loser:
        loser = st.session_state.loser
        st.error(f"### 🎯 The wheel stopped on: {loser}!")
        
        # --- The Math Logic ---
        num_people = len(friends_list)
        base_share = total_bill / num_people
        
        if multiplier == "Fully (100%)":
            loser_pays = total_bill
            others_pay = 0
        else:
            # Extract the number from "2x Share" or "3x Share"
            mult_value = int(multiplier[0]) 
            loser_pays = min(base_share * mult_value, total_bill)
            remaining_bill = total_bill - loser_pays
            others_pay = remaining_bill / (num_people - 1)
        
        # --- Display Final Split ---
        st.write("#### Final Payouts:")
        
        # Create visual metric cards for the results
        cols = st.columns(min(num_people, 4)) # display up to 4 columns nicely
        for i, friend in enumerate(friends_list):
            col = cols[i % len(cols)]
            if friend == loser:
                col.metric(label=f"🚨 {friend} (Penalty)", value=f"₹{loser_pays:.2f}")
            else:
                col.metric(label=f"✅ {friend}", value=f"₹{others_pay:.2f}")