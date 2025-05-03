import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="📧 Email AI Agent Dashboard", layout="wide")

# Load processed emails
try:
    with open("processed_emails.json") as f:
        lines = [json.loads(line) for line in f.readlines()]
except FileNotFoundError:
    lines = []

df = pd.DataFrame(lines)

st.title("📧 Email AI Agent Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", len(df))
col2.metric("High-Quality Leads", len(df[df['lead_score'] >= 7]))
col3.metric("Sales Inquiries", len(df[df['category'] == 'Sales Inquiry']))

st.subheader("📊 Email Categories Over Time")
category_counts = df.groupby(['date', 'category']).size().unstack(fill_value=0)
st.line_chart(category_counts)

st.subheader("📈 Lead Scores Distribution")
st.bar_chart(df['lead_score'].value_counts())

st.subheader("📬 All Leads")
st.dataframe(df[['timestamp', 'sender', 'subject', 'category', 'lead_score']])

# Show details
selected_lead_index = st.selectbox("Select a lead to view details:", df.index.tolist())
selected_lead = df.iloc[selected_lead_index]
st.markdown(f"**From:** {selected_lead['sender']}")
st.markdown(f"**Category:** {selected_lead['category']}")
st.markdown(f"**Lead Score:** {selected_lead['lead_score']}")
st.markdown(f"**Phone Numbers:** {', '.join([p['number'] for p in selected_lead.get('phone_numbers', [])])}")
st.markdown(f"**WhatsApp:** {', '.join(selected_lead.get('whatsapp_numbers', []))}")
st.markdown(f"**Social Links:** {', '.join(selected_lead.get('social_links', []))}")
st.text_area("Email Body", selected_lead['body'], height=200)

# Export button
if st.button("Export to CSV"):
    export_to_csv()
    st.success("✅ Exported to CSV")