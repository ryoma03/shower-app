import streamlit as st
import json
import os

# 状態を保存するファイル
# ※Renderの無料枠は15分アクセスがないとスリープし、再起動時にこのファイルがリセットされます。
# ＝「しばらく誰も使っていないと自動で空室に戻る」という便利な仕様として機能します！
FILE_PATH = 'shower_status.json'

def init_status():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            json.dump({'shower1': False, 'shower2': False}, f)

def load_status():
    init_status()
    with open(FILE_PATH, 'r') as f:
        return json.load(f)

def save_status(status):
    with open(FILE_PATH, 'w') as f:
        json.dump(status, f)

st.set_page_config(page_title="シャワー空き状況", page_icon="🚿", layout="centered")
st.title("🚿 シャワールーム空き状況")
st.write("女子13人専用！使用開始・終了をタップしてね")

status = load_status()

# UIデザイン
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚪 シャワー 1")
    if status['shower1']:
        st.error("🔴 現在、使用中です")
        if st.button("使用を終了する", key="end1", use_container_width=True):
            status['shower1'] = False
            save_status(status)
            st.rerun()
    else:
        st.success("🟢 今、空いています")
        if st.button("使用を開始する", key="start1", use_container_width=True):
            status['shower1'] = True
            save_status(status)
            st.rerun()

with col2:
    st.markdown("### 🚪 シャワー 2")
    if status['shower2']:
        st.error("🔴 現在、使用中です")
        if st.button("使用を終了する", key="end2", use_container_width=True):
            status['shower2'] = False
            save_status(status)
            st.rerun()
    else:
        st.success("🟢 今、空いています")
        if st.button("使用を開始する", key="start2", use_container_width=True):
            status['shower2'] = True
            save_status(status)
            st.rerun()
