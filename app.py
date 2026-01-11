import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# --- AYARLAR ---
ARAC_DOSYASI = "arac_randevulari.csv"
KULLANICI_DOSYASI = "kullanicilar.csv"
LOGO_DOSYASI = "logo.png"  # <-- Masaüstündeki resmin adı bu olmalı

# Sayfa Ayarları
st.set_page_config(page_title="Ex Motors", page_icon="🚗", layout="wide")

# --- CSS İLE GÖRÜNÜM İYİLEŞTİRME ---
st.markdown("""
<style>
    .stDataFrame { font-size: 1.1rem; }
    .stButton button { width: 100%; border-radius: 10px; height: 3em; }
    .css-1r6slb0 { border: 1px solid #ddd; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- DİL SÖZLÜĞÜ ---
LANG = {
    "TR": {
        "login_title": "Ex Motors Giriş",
        "sidebar_title": "Ex Motors",
        "login_user": "Kullanıcı Adı",
        "login_pass": "Şifre",
        "login_btn": "Giriş Yap",
        "login_error": "Hatalı giriş!",
        "logout": "Çıkış",
        "nav_dashboard": "🏠 Ana Sayfa",
        "nav_waiting": "⏳ Bekleyenler",
        "nav_new": "➕ Yeni Ekle",
        "nav_list": "📋 Liste/Yönet",
        "nav_users": "👥 Personel",
        "view_mode": "Görünüm:",
        "view_card": "📱 Kart",
        "view_table": "💻 Tablo",
        "dash_title": "İşletme Özeti",
        "total_rec": "Toplam",
        "today_job": "Bugün",
        "pending_job": "Bekleyen",
        "waiting_title": "Sıradaki Araçlar",
        "new_title": "Yeni Araç Kaydı",
        "lbl_plate": "Plaka",
        "lbl_name": "Müşteri",
        "lbl_phone": "Telefon",
        "lbl_date": "Tarih",
        "lbl_time": "Saat",
        "lbl_type": "İşlem",
        "lbl_price": "Ücret",
        "btn_save": "Kaydet",
        "success_save": "Kaydedildi!",
        "list_title": "Araç Yönetimi",
        "tab_active": "Aktif",
        "tab_history": "Geçmiş",
        "search_lbl": "Ara:",
        "update_header": "Düzenle",
        "select_car": "Araç Seç:",
        "new_status": "Durum:",
        "btn_update": "Güncelle",
        "btn_delete": "Sil",
        "status_options": ["Bekliyor", "İşlemde", "Tamamlandı", "İptal"],
        "service_types": ["Periyodik Bakım", "Yağ Değişimi", "Lastik", "Fren", "Motor", "Temizlik"],
        "user_page_title": "Personel Yönetimi",
        "user_new_header": "Yeni Kullanıcı",
        "user_update_header": "Şifre Değiştir",
        "user_list_header": "Kullanıcılar",
        "btn_add_user": "Ekle",
        "btn_del_user": "Sil",
        "msg_user_exists": "Kullanıcı var!",
        "msg_user_added": "Eklendi.",
        "msg_pass_updated": "Güncellendi."
    },
    "EN": {
        "login_title": "Ex Motors Login",
        "sidebar_title": "Ex Motors",
        "login_user": "Username",
        "login_pass": "Password",
        "login_btn": "Login",
        "login_error": "Error!",
        "logout": "Logout",
        "nav_dashboard": "🏠 Dashboard",
        "nav_waiting": "⏳ Waiting",
        "nav_new": "➕ New Entry",
        "nav_list": "📋 List/Manage",
        "nav_users": "👥 Staff",
        "view_mode": "View:",
        "view_card": "📱 Card",
        "view_table": "💻 Table",
        "dash_title": "Summary",
        "total_rec": "Total",
        "today_job": "Today",
        "pending_job": "Pending",
        "waiting_title": "Waiting Cars",
        "new_title": "New Car Reg.",
        "lbl_plate": "Plate",
        "lbl_name": "Name",
        "lbl_phone": "Phone",
        "lbl_date": "Date",
        "lbl_time": "Time",
        "lbl_type": "Type",
        "lbl_price": "Price",
        "btn_save": "Save",
        "success_save": "Saved!",
        "list_title": "Management",
        "tab_active": "Active",
        "tab_history": "History",
        "search_lbl": "Search:",
        "update_header": "Edit",
        "select_car": "Select Car:",
        "new_status": "Status:",
        "btn_update": "Update",
        "btn_delete": "Delete",
        "status_options": ["Pending", "In Progress", "Completed", "Cancelled"],
        "service_types": ["Maintenance", "Oil Change", "Tire", "Brake", "Engine", "Cleaning"],
        "user_page_title": "Staff Management",
        "user_new_header": "New User",
        "user_update_header": "Change Pass",
        "user_list_header": "Users",
        "btn_add_user": "Add",
        "btn_del_user": "Delete",
        "msg_user_exists": "Exists!",
        "msg_user_added": "Added.",
        "msg_pass_updated": "Updated."
    },
    "AL": {
        "login_title": "Hyrje Ex Motors",
        "sidebar_title": "Ex Motors",
        "login_user": "Përdoruesi",
        "login_pass": "Fjalëkalimi",
        "login_btn": "Hyr",
        "login_error": "Gabim!",
        "logout": "Dil",
        "nav_dashboard": "🏠 Paneli",
        "nav_waiting": "⏳ Në Pritje",
        "nav_new": "➕ E Re",
        "nav_list": "📋 Menaxho",
        "nav_users": "👥 Stafi",
        "view_mode": "Pamja:",
        "view_card": "📱 Kartelë",
        "view_table": "💻 Tabelë",
        "dash_title": "Përmbledhje",
        "total_rec": "Gjithsej",
        "today_job": "Sot",
        "pending_job": "Pritje",
        "waiting_title": "Makinat në Pritje",
        "new_title": "Regjistrim i Ri",
        "lbl_plate": "Targa",
        "lbl_name": "Emri",
        "lbl_phone": "Tel",
        "lbl_date": "Data",
        "lbl_time": "Ora",
        "lbl_type": "Lloji",
        "lbl_price": "Çmimi",
        "btn_save": "Ruaj",
        "success_save": "U Ruajt!",
        "list_title": "Menaxhimi",
        "tab_active": "Aktive",
        "tab_history": "Historia",
        "search_lbl": "Kërko:",
        "update_header": "Përditëso",
        "select_car": "Zgjidh:",
        "new_status": "Statusi:",
        "btn_update": "Përditëso",
        "btn_delete": "Fshij",
        "status_options": ["Në Pritje", "Në Proces", "Përfunduar", "Anuluar"],
        "service_types": ["Mirëmbajtje", "Vaj", "Goma", "Frenat", "Motor", "Pastrim"],
        "user_page_title": "Menaxhimi Stafit",
        "user_new_header": "Përdorues i Ri",
        "user_update_header": "Ndrysho Kodin",
        "user_list_header": "Përdoruesit",
        "btn_add_user": "Shto",
        "btn_del_user": "Fshij",
        "msg_user_exists": "Ekziston!",
        "msg_user_added": "U shtua.",
        "msg_pass_updated": "U ndryshua."
    }
}

# --- FONKSİYONLAR ---
def veri_yukle():
    if not os.path.exists(ARAC_DOSYASI):
        df = pd.DataFrame(columns=["Tarih", "Saat", "Plaka", "Müşteri", "Telefon", "İşlem", "Durum", "Ücret"])
        df.to_csv(ARAC_DOSYASI, index=False)
        return df
    return pd.read_csv(ARAC_DOSYASI)

def veri_kaydet(df):
    df.to_csv(ARAC_DOSYASI, index=False)

def kullanici_yukle():
    if not os.path.exists(KULLANICI_DOSYASI):
        df = pd.DataFrame([{"Kullanici": "admin", "Sifre": "12345"}])
        df.to_csv(KULLANICI_DOSYASI, index=False)
        return df
    return pd.read_csv(KULLANICI_DOSYASI, dtype=str)

def kullanici_kaydet(df):
    df.to_csv(KULLANICI_DOSYASI, index=False)

# LOGO GÖSTERME FONKSİYONU (BÜYÜTÜLDÜ)
def logo_goster(yer="sidebar"):
    # Eğer logo.png dosyası varsa onu kullan, yoksa internetten araba simgesi çek
    varsayilan_logo = "https://cdn-icons-png.flaticon.com/512/295/295128.png"
    resim_kaynagi = varsayilan_logo
    
    if os.path.exists(LOGO_DOSYASI):
        resim_kaynagi = LOGO_DOSYASI
    
    if yer == "sidebar":
        # Yan menüdeki logo (300px yapıldı - BÜYÜDÜ)
        st.sidebar.image(resim_kaynagi, width=300) 
    else:
        # Giriş ekranındaki logo (600px yapıldı - KOCAMAN OLDU)
        st.image(resim_kaynagi, width=600)

def render_mobile_cards(df, T):
    if df.empty:
        st.info("Liste boş.")
        return
    for index, row in df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([2, 1])
            c1.markdown(f"### 🚗 {row['Plaka']}")
            durum_renk = "blue"
            if row['Durum'] in ["Tamamlandı", "Completed", "Përfunduar"]: durum_renk = "green"
            elif row['Durum'] in ["İptal", "Cancelled", "Anuluar"]: durum_renk = "red"
            elif row['Durum'] in ["İşlemde", "In Progress", "Në Proces"]: durum_renk = "orange"
            c2.markdown(f":{durum_renk}[**{row['Durum']}**]")
            st.write(f"👤 {row['Müşteri']} | 📞 {row['Telefon']}")
            st.write(f"🔧 {row['İşlem']} | 💰 {row['Ücret']}")
            st.caption(f"📅 {row['Tarih']} ⏰ {row['Saat']}")

# --- SESSION STATE ---
if 'giris_yapildi' not in st.session_state:
    st.session_state['giris_yapildi'] = False
if 'aktif_kullanici' not in st.session_state:
    st.session_state['aktif_kullanici'] = ""

# ==========================================
# 🔐 GİRİŞ EKRANI
# ==========================================
if not st.session_state['giris_yapildi']:
    dil = st.selectbox("Language / Dil", ["TR", "EN", "AL"])
    T = LANG[dil]
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 8, 1]) 
    
    with col2:
        # LOGO BURAYA GELİYOR
        logo_goster(yer="main")
        st.title(T["login_title"])
        
        user_input = st.text_input(T["login_user"])
        pass_input = st.text_input(T["login_pass"], type="password")
        
        if st.button(T["login_btn"], type="primary"):
            users_df = kullanici_yukle()
            kullanici_bulundu = users_df[(users_df["Kullanici"] == user_input) & (users_df["Sifre"] == pass_input)]
            if not kullanici_bulundu.empty:
                st.session_state['giris_yapildi'] = True
                st.session_state['aktif_kullanici'] = user_input
                st.session_state['dil_kodu'] = dil
                st.rerun()
            else:
                st.error(T["login_error"])

# ==========================================
# 🚗 ANA UYGULAMA
# ==========================================
else:
    secilen_dil_kodu = st.session_state.get('dil_kodu', "TR")
    T = LANG[secilen_dil_kodu]
    aktif_user = st.session_state['aktif_kullanici']
    
    # MENÜ LOGOSU BURAYA GELİYOR
    logo_goster(yer="sidebar")
    st.sidebar.title(T["sidebar_title"])
    st.sidebar.write(f"👤 **{aktif_user}**")
    
    if st.sidebar.button(f"🚪 {T['logout']}"):
        st.session_state['giris_yapildi'] = False
        st.session_state['aktif_kullanici'] = ""
        st.rerun()
        
    st.sidebar.markdown("---")
    
    menu_listesi = [T["nav_dashboard"], T["nav_waiting"], T["nav_new"], T["nav_list"]]
    if aktif_user == "admin":
        menu_listesi.append(T["nav_users"])
        
    secim = st.sidebar.radio("Menu", menu_listesi)
    df = veri_yukle()

    # --- 1. DASHBOARD ---
    if secim == T["nav_dashboard"]:
        st.header(T["dash_title"])
        col1, col2, col3 = st.columns(3)
        toplam = len(df)
        bugun = len(df[df["Tarih"] == datetime.now().strftime("%Y-%m-%d")])
        bekleyen = len(df[df["Durum"].isin(["Bekliyor", "Pending", "Në Pritje"])])
        col1.metric(T["total_rec"], f"{toplam}")
        col2.metric(T["today_job"], f"{bugun}")
        col3.metric(T["pending_job"], f"{bekleyen}", delta_color="inverse")

    # --- 2. BEKLEYENLER ---
    elif secim == T["nav_waiting"]:
        st.header(T["waiting_title"])
        gorunum = st.radio(T["view_mode"], [T["view_card"], T["view_table"]], horizontal=True)
        bekleyen_df = df[df["Durum"].isin(["Bekliyor", "Pending", "Në Pritje"])]
        if bekleyen_df.empty:
            st.success("✅")
        else:
            if gorunum == T["view_card"]:
                render_mobile_cards(bekleyen_df, T)
            else:
                st.dataframe(bekleyen_df, use_container_width=True, hide_index=True)

    # --- 3. YENİ KAYIT ---
    elif secim == T["nav_new"]:
        st.header(T["new_title"])
        with st.form("randevu_formu"):
            plaka = st.text_input(T["lbl_plate"], placeholder="34 ABC 123").upper()
            musteri = st.text_input(T["lbl_name"])
            tel = st.text_input(T["lbl_phone"])
            c1, c2 = st.columns(2)
            tarih = c1.date_input(T["lbl_date"])
            saat = c2.time_input(T["lbl_time"])
            islem = st.selectbox(T["lbl_type"], T["service_types"])
            ucret = st.number_input(T["lbl_price"], min_value=0, step=50)

            if st.form_submit_button(T["btn_save"]):
                if plaka and musteri:
                    yeni_veri = {
                        "Tarih": str(tarih), "Saat": str(saat), "Plaka": plaka,
                        "Müşteri": musteri, "Telefon": tel, "İşlem": islem,
                        "Durum": T["status_options"][0], "Ücret": ucret
                    }
                    df = pd.concat([df, pd.DataFrame([yeni_veri])], ignore_index=True)
                    veri_kaydet(df)
                    st.success(f"✅ {plaka}")

    # --- 4. LİSTE VE YÖNETİM ---
    elif secim == T["nav_list"]:
        st.header(T["list_title"])
        arama = st.text_input(T["search_lbl"])
        gorunum = st.radio(T["view_mode"], [T["view_card"], T["view_table"]], horizontal=True)

        gecmis_durumlar = ["Tamamlandı", "Completed", "Përfunduar", "İptal", "Cancelled", "Anuluar"]
        aktif_df = df[~df["Durum"].isin(gecmis_durumlar)] if not df.empty else pd.DataFrame()
        gecmis_df = df[df["Durum"].isin(gecmis_durumlar)] if not df.empty else pd.DataFrame()

        if arama and not df.empty:
            aktif_df = aktif_df[aktif_df["Plaka"].str.contains(arama) | aktif_df["Müşteri"].str.contains(arama, case=False)]
            gecmis_df = gecmis_df[gecmis_df["Plaka"].str.contains(arama) | gecmis_df["Müşteri"].str.contains(arama, case=False)]

        tab1, tab2 = st.tabs([T["tab_active"], T["tab_history"]])
        with tab1:
            if not aktif_df.empty:
                with st.expander(T["update_header"], expanded=False):
                    secilen_plaka = st.selectbox(T["select_car"], aktif_df["Plaka"].unique())
                    yeni_durum = st.selectbox(T["new_status"], T["status_options"])
                    c_btn1, c_btn2 = st.columns(2)
                    if c_btn1.button(T["btn_update"], type="primary"):
                        df.loc[df["Plaka"] == secilen_plaka, "Durum"] = yeni_durum
                        veri_kaydet(df)
                        st.rerun()
                    if c_btn2.button(T["btn_delete"]):
                        df = df[df["Plaka"] != secilen_plaka]
                        veri_kaydet(df)
                        st.rerun()
                if gorunum == T["view_card"]:
                    render_mobile_cards(aktif_df, T)
                else:
                    st.dataframe(aktif_df, use_container_width=True, hide_index=True)
            else:
                st.info("---")
        with tab2:
            if gorunum == T["view_card"]:
                render_mobile_cards(gecmis_df, T)
            else:
                st.dataframe(gecmis_df, use_container_width=True, hide_index=True)

    # --- 5. PERSONEL (SADECE ADMIN) ---
    elif secim == T.get("nav_users"):
        st.header(T["user_page_title"])
        users_df = kullanici_yukle()
        with st.expander(T["user_new_header"]):
            new_user = st.text_input("Kullanıcı Adı")
            new_pass = st.text_input("Şifre", type="password")
            if st.button(T["btn_add_user"]):
                if new_user not in users_df["Kullanici"].values:
                    users_df = pd.concat([users_df, pd.DataFrame([{"Kullanici": new_user, "Sifre": new_pass}])], ignore_index=True)
                    kullanici_kaydet(users_df)
                    st.success(T["msg_user_added"])
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(T["msg_user_exists"])
        
        with st.expander(T["user_update_header"]):
            selected_user = st.selectbox("Personel", users_df["Kullanici"].tolist())
            pass_update = st.text_input("Yeni Şifre", type="password")
            if st.button("Güncelle"):
                users_df.loc[users_df["Kullanici"] == selected_user, "Sifre"] = pass_update
                kullanici_kaydet(users_df)
                st.success(T["msg_pass_updated"])

        st.markdown("---")
        st.subheader(T["user_list_header"])
        for i, row in users_df.iterrows():
            c1, c2 = st.columns([3, 1])
            c1.write(f"👤 {row['Kullanici']}")
            if row['Kullanici'] != "admin":
                if c2.button(T["btn_del_user"], key=f"del_{i}"):
                    users_df = users_df.drop(i)
                    kullanici_kaydet(users_df)
                    st.rerun()