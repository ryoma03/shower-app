import streamlit as st
import json
import os
from datetime import datetime

FILE_PATH = 'shower_status.json'

# --- データ管理 ---
def init_status():
    if not os.path.exists(FILE_PATH):
        # 単純なON/OFFだけでなく、開始時間も保存できる構造に変更
        default_data = {
            'shower1': {'is_active': False, 'start_time': None},
            'shower2': {'is_active': False, 'start_time': None}
        }
        with open(FILE_PATH, 'w') as f:
            json.dump(default_data, f)

def load_status():
    init_status()
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
        # 過去の古い形式(True/Falseのみ)のファイルが残っていた場合の安全策
        if isinstance(data.get('shower1'), bool):
            data = {
                'shower1': {'is_active': False, 'start_time': None},
                'shower2': {'is_active': False, 'start_time': None}
            }
        return data

def save_status(status):
    with open(FILE_PATH, 'w') as f:
        json.dump(status, f)

# 経過時間を計算する関数
def get_elapsed_time(start_time_str):
    if not start_time_str:
        return ""
    start_time = datetime.fromisoformat(start_time_str)
    now = datetime.now()
    elapsed = now - start_time
    minutes = int(elapsed.total_seconds() // 60)
    return f"（現在 {minutes}分 経過）"


# --- UIデザイン ---
st.set_page_config(page_title="シャワー空き状況", page_icon="🚿", layout="centered")
st.title("🚿 シャワールーム空き状況")
st.write("女子13人専用！使用開始・終了をタップしてね")

status = load_status()

col1, col2 = st.columns(2)

# シャワー1
with col1:
    st.markdown("### 🚪 シャワー 1")
    if status['shower1']['is_active']:
        elapsed_text = get_elapsed_time(status['shower1']['start_time'])
        st.error(f"🔴 使用中です\n\n{elapsed_text}")
        if st.button("使用を終了する", key="end1", use_container_width=True):
            status['shower1']['is_active'] = False
            status['shower1']['start_time'] = None
            save_status(status)
            st.rerun()
    else:
        st.success("🟢 今、空いています")
        if st.button("使用を開始する", key="start1", use_container_width=True):
            status['shower1']['is_active'] = True
            status['shower1']['start_time'] = datetime.now().isoformat() # 開始時間を記録
            save_status(status)
            st.rerun()

# シャワー2
with col2:
    st.markdown("### 🚪 シャワー 2")
    if status['shower2']['is_active']:
        elapsed_text = get_elapsed_time(status['shower2']['start_time'])
        st.error(f"🔴 使用中です\n\n{elapsed_text}")
        if st.button("使用を終了する", key="end2", use_container_width=True):
            status['shower2']['is_active'] = False
            status['shower2']['start_time'] = None
            save_status(status)
            st.rerun()
    else:
        st.success("🟢 今、空いています")
        if st.button("使用を開始する", key="start2", use_container_width=True):
            status['shower2']['is_active'] = True
            status['shower2']['start_time'] = datetime.now().isoformat() # 開始時間を記録
            save_status(status)
            st.rerun()
