import streamlit as st
from pymongo import MongoClient
import pandas as pd
from PIL import Image
import os
import base64

st.set_page_config(
    page_title="İBB Metro Durum Takibi",
    page_icon="🚇",
    layout="wide"
)

# İkon eşleme fonksiyonu

def get_metro_icon_path(line_name):
    icon_map = {

        "TF1": "tf1.png",
        "TF2": "tf2.png",
        
        # Metro hatları
        "M1A": "m1a.png",
        "M1B": "m1b.png",
        "M2": "m2.png",
        "M3": "m3.png",
        "M4": "m4.png",
        "M5": "m5.png",
        "M6": "m6.png",
        "M7": "m7.png",
        "M8": "m8.png",
        "M9": "m9.png",
       
        # Tramvay hatları
        "T1": "t1.png",
        "T3": "t3.png",
        "T4": "t4.png",
        "T5": "t5.png",
        
        # Füniküler hatları
        "F1": "f1.png",
        "F4": "f4.png",
    }
    
    
    line_name_upper = line_name.upper().strip()
    
    for code, icon_file in icon_map.items():
        if line_name_upper.startswith(code):
            path = os.path.join(os.path.dirname(__file__), "assets", "metro_icons", icon_file)
            if os.path.exists(path):
                return path
    
    return None

def play_audio_hidden(audio_file):
    with open(audio_file, 'rb') as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

@st.cache_resource
def get_database():
    MONGO_URI = st.secrets["MONGO_URI"]
    client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    return client["metroapp"]["metroapp"]

# Başlık ve refresh butonu
col1, col2, col3 = st.columns([12, 2, 2])
with col1:
    st.title("🚇 İstanbul Metro Durum Takibi")
with col2:
    st.write("")  
    if st.button("🔄 Yenile"):
        st.cache_resource.clear()
        st.rerun()
with col3:
    st.write("")
    if st.button("🔊"):
        play_audio_hidden("./assets/train_sound.mp3")
        st.image("./assets/metro.gif", width=500)


# Veri çek
try:
    collection = get_database()
    lines = list(collection.find())
except Exception as e:
    st.error(f"Veritabanı bağlantı hatası: {e}")
    lines = []
        
if lines:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Toplam Hat", len(lines))
    with col2:
        problem_count = sum(1 for line in lines if line.get('status'))
        st.metric("Arızalı Hat", problem_count)
    with col3:
        normal_count = len(lines) - problem_count
        st.metric("Aktif Hat", normal_count)

    st.markdown("---")

    # Arızalı hatlar
    st.subheader("🔴 Arızalı Hatlar")
    problem_lines = [line for line in lines if line.get('status')]

    if problem_lines:
        for line in problem_lines:
            icon_path = get_metro_icon_path(line['Name'])
            
            col1, col2 = st.columns([1, 9])
            with col1:
                if icon_path and os.path.exists(icon_path):
                    try:
                        icon = Image.open(icon_path)
                        st.image(icon, width=60)
                    except:
                        st.markdown("### 🚇")
                else:
                    st.markdown("### 🚇")
            
            with col2:
                st.error(f"**{line['Name']}**")
                st.write(f"📝 {line.get('status_description', 'Bilgi yok')}")
                if line.get('update_date'):
                    st.caption(f"🕐 Son güncelleme: {line['update_date']}")
            
            st.markdown("---")
    else:
        st.success("✅ Tüm hatlar aktif çalışıyor!")

    st.markdown("---")

    # Tüm hatlar - Kartlar
    st.subheader("📊 Tüm Metro Hatları")

    cols = st.columns(3)
    for idx, line in enumerate(lines):
        with cols[idx % 3]:
            icon_path = get_metro_icon_path(line['Name'])
            status_icon = "🔴" if line.get('status') else "🟢"
            
            with st.container(border=True):
                # İkonu göster
                if icon_path and os.path.exists(icon_path):
                    try:
                        icon = Image.open(icon_path)
                        st.image(icon, width=60)
                    except:
                        st.markdown("### 🚇")
                else:
                    st.markdown("### 🚇")

                st.markdown(f"**{line['LongDescription'][:50]}**")
                st.markdown(f"{status_icon} **{'ARIZALI' if line.get('status') else 'Aktif'}**")
                
                if line.get('update_date'):
                    st.caption(f"🕐 {line['update_date']}")

    st.markdown("---")


#     # Detaylı Tablo
#     with st.expander("📋 Detaylı Tablo Görünümü"):
#         df = pd.DataFrame([{
#             "Hat": line['Name'],
#             "Durum": "🔴 Arızalı" if line.get('status') else "🟢 Aktif",
#             "Açıklama": line.get('LongDescription', '-'),
#             "Son Güncelleme": line.get('update_date', 'Henüz güncellenmedi')
#         } for line in lines])
        
#         st.dataframe(df, use_container_width=True, hide_index=True)

# else:
#     st.warning("Henüz veri yok veya bağlantı kurulamadı.")
    