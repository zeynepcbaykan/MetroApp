import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime


st.set_page_config(
    page_title="İstanbul Metro Durum",
    page_icon="🚇",
    layout="wide"
)

# MongoDB bağlantısı
@st.cache_resource
def get_database():
    MONGO_URI = st.secrets["MONGO_URI"]
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    return client["metroapp"]["metroapp"]


st.title("🚇 İstanbul Metro Durum Takibi")
st.markdown("---")

collection = get_database()
lines = list(collection.find())

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Toplam Hat", len(lines))
with col2:
    problem_count = sum(1 for line in lines if line.get('status'))
    st.metric("Arızalı Hat", problem_count, delta=f"-{len(lines)-problem_count} Normal")
with col3:
    normal_count = len(lines) - problem_count
    st.metric("Normal Hat", normal_count)

st.markdown("---")

st.subheader("🔴 Arızalı Hatlar")
problem_lines = [line for line in lines if line.get('status')]

if problem_lines:
    for line in problem_lines:
        with st.expander(f"⚠️ {line['Name']}", expanded=True):
            st.error(f"**Durum:** {line.get('status_description', 'Bilgi yok')}")
            if line.get('update_date'):
                st.caption(f"Son güncelleme: {line['update_date']}")
else:
    st.success("✅ Tüm hatlar normal çalışıyor!")

st.markdown("---")


st.subheader("📊 Tüm Hatlar")
df = pd.DataFrame([{
    "Hat": line['Name'],
    "Hat Adı": line.get('LongDescription', '-'),
    "Durum": "🔴 Arızalı" if line.get('status') else "🟢 Normal",
    "Son Güncelleme": line.get('update_date', 'Henüz güncellenmedi')
} for line in lines])

st.dataframe(df, use_container_width=True)

if st.button("🔄 Yenile"):
    st.rerun()