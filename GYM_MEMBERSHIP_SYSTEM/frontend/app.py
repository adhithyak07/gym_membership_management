import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="Gym Membership System", layout="centered")

st.title("🏋️ Gym Membership System")

# ------------------ Sidebar Navigation ------------------
menu = st.sidebar.radio("Navigation", ["Members", "Payments"])

# ------------------ Helper Functions ------------------
def safe_id_display(id_value, length=8):
    """Safely display ID whether it's string or integer"""
    if isinstance(id_value, str) and len(id_value) > length:
        return f"{id_value[:length]}..."
    return str(id_value)

def safe_get(dictionary, key, default="N/A"):
    """Safely get value from dictionary"""
    return dictionary.get(key, default)

# ------------------ Members Section ------------------
if menu == "Members":
    st.header("👤 Manage Members")

    with st.form("add_member_form"):
        st.subheader("Add New Member")
        name = st.text_input("Name")
        phone = st.text_input("Phone")
        plan = st.selectbox("Plan", ["Monthly", "Quarterly", "Yearly"])
        end_date = st.date_input("End Date")
        submit = st.form_submit_button("Add Member")

        if submit and name and phone:  # Added validation
            payload = {
                "name": name,
                "phone": phone,
                "plan": plan,
                "end_date": str(end_date),
            }
            try:
                res = requests.post(f"{API_URL}/members/", json=payload)
                if res.status_code == 200:
                    st.success("✅ Member added successfully!")
                    st.rerun()  # Refresh the page
                else:
                    error_detail = res.json().get('detail', 'Unknown error')
                    st.error(f"❌ Error: {error_detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {e}")
        elif submit:
            st.warning("⚠️ Please fill in all required fields")

    st.subheader("📋 Current Members")
    if st.button("Refresh Members"):
        try:
            res = requests.get(f"{API_URL}/members/")
            if res.status_code == 200:
                members = res.json().get("data", [])
                if members:
                    for m in members:
                        # Handle both string and integer IDs
                        member_id_display = safe_id_display(m.get('id', 'Unknown'))
                        with st.expander(f"👤 {safe_get(m, 'name')} - {safe_get(m, 'plan')}"):
                            st.write(f"**ID:** `{m.get('id', 'N/A')}`")
                            st.write(f"**Phone:** {safe_get(m, 'phone')}")
                            st.write(f"**Plan:** {safe_get(m, 'plan')}")
                            st.write(f"**Start Date:** {safe_get(m, 'start_date')}")
                            st.write(f"**End Date:** {safe_get(m, 'end_date')}")
                else:
                    st.info("No members found.")
            else:
                st.error("Error fetching members.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")

# ------------------ Payments Section ------------------
elif menu == "Payments":
    st.header("💰 Manage Payments")

    with st.form("add_payment_form"):
        st.subheader("Record Payment")
        
        # Fetch members for dropdown
        try:
            members_res = requests.get(f"{API_URL}/members/")
            if members_res.status_code == 200:
                members = members_res.json().get("data", [])
                if members:
                    # Create member options with safe ID handling
                    member_options = {}
                    for m in members:
                        member_id = m.get('id', 'Unknown')
                        member_name = m.get('name', 'Unknown')
                        display_id = safe_id_display(member_id, 8)
                        member_options[f"{member_name} ({display_id})"] = str(member_id)
                    
                    selected_member = st.selectbox("Select Member", list(member_options.keys()))
                    member_id = member_options[selected_member]
                    st.info(f"Selected Member ID: `{member_id}`")
                else:
                    st.warning("⚠️ No members found. Please add a member first.")
                    member_id = st.text_input("Member ID (Manual Entry)")
            else:
                st.warning("⚠️ Could not fetch members. Manual entry required.")
                member_id = st.text_input("Member ID")
        except:
            st.warning("⚠️ Could not fetch members. Manual entry required.")
            member_id = st.text_input("Member ID")
        
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        method = st.selectbox("Method", ["Cash", "UPI", "Card"])
        submit = st.form_submit_button("Add Payment")

        if submit and member_id and amount > 0:
            payload = {
                "member_id": str(member_id),  # Ensure it's a string
                "amount": float(amount),
                "method": method,
            }
            
            # Show debug info in an expander
            with st.expander("🔍 Debug Info (Click to expand)"):
                st.json(payload)
            
            try:
                res = requests.post(f"{API_URL}/payments/", json=payload)
                
                if res.status_code == 200:
                    st.success("✅ Payment recorded successfully!")
                    st.rerun()  # Refresh the page
                else:
                    error_detail = res.json().get('detail', 'Unknown error')
                    st.error(f"❌ Error: {error_detail}")
                    
                    # Show response details in expander for debugging
                    with st.expander("🔍 Error Details"):
                        st.write(f"**Status Code:** {res.status_code}")
                        st.json(res.json())
                        
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {e}")
        elif submit:
            st.warning("⚠️ Please fill in all required fields and ensure amount > 0")

    st.subheader("📋 Payment Records")
    if st.button("Refresh Payments"):
        try:
            res = requests.get(f"{API_URL}/payments/")
            if res.status_code == 200:
                payments = res.json().get("data", [])
                if payments:
                    for p in payments:
                        # Safely handle payment ID (could be int or string)
                        payment_id = p.get('id', 'Unknown')
                        payment_id_display = safe_id_display(payment_id, 8)
                        amount = p.get('amount', 0)
                        
                        with st.expander(f"💳 Payment #{payment_id_display} - ₹{amount}"):
                            st.write(f"**Payment ID:** `{payment_id}`")
                            # Handle both 'gymrat_id' and 'member_id' fields
                            member_id = p.get('gymrat_id') or p.get('member_id', 'N/A')
                            member_id_display = safe_id_display(member_id, 8) if member_id != 'N/A' else 'N/A'
                            st.write(f"**Member ID:** `{member_id}` ({member_id_display})")
                            st.write(f"**Amount:** ₹{amount}")
                            st.write(f"**Method:** {safe_get(p, 'method')}")
                            st.write(f"**Date:** {safe_get(p, 'payment_date')}")
                else:
                    st.info("No payments found.")
            else:
                st.error("Error fetching payments.")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")

# ------------------ Debug Section ------------------
st.sidebar.markdown("---")
if st.sidebar.button("🔍 Debug API"):
    st.subheader("🔍 API Debug Info")
    
    try:
        # Test API connection
        res = requests.get(f"{API_URL}/")
        st.write("**API Status:**", "✅ Connected" if res.status_code == 200 else "❌ Error")
        
        if res.status_code == 200:
            st.json(res.json())
        
        # Test model info (if you added the debug endpoint)
        try:
            model_res = requests.get(f"{API_URL}/debug/model-info")
            if model_res.status_code == 200:
                st.write("**PaymentCreate Model Info:**")
                st.json(model_res.json())
        except:
            st.write("Debug endpoint not available")
            
        # Test payment schema
        try:
            schema_res = requests.get(f"{API_URL}/debug/payment-schema")
            if schema_res.status_code == 200:
                st.write("**Payment Schema Test:**")
                st.json(schema_res.json())
        except:
            st.write("Payment schema test not available")
            
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Cannot connect to API: {e}")
        st.info(f"Make sure your FastAPI server is running on {API_URL}")