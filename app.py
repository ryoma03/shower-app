import streamlit as st
import json
import os
from datetime import datetime

FILE_PATH = 'shower_status.json'

# --- データ管理 ---
def init_status():
    if not os.path.exists(FILE_PATH):
        default_data = {
            'shower1': {'is_active': False, 'start_time': None},
            'shower2': {'is_active': False, 'start_time': None},
            'waiting_count': 0  # 順番待ちの人数を追加
        }
        with open(FILE_PATH, 'w') as f:
            json.dump(default_data, f)

def load_status():
    init_status()
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
        # 古いデータ形式のアップデート用（エラー回避）
        if 'waiting_count' not in data:
            data['waiting_count'] = 0
            save_status(data)
        return data

def save_status(status):
    with open(FILE_PATH, 'w') as f:
        json.dump(status, f)

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

status = load_status()

# --- 🙋‍♀️ 順番待ちセクション ---
st.markdown("---")
st.subheader("🙋‍♀️ 順番待ち")

wait_col1, wait_col2 = st.columns([2, 1])

with wait_col1:
    if status['waiting_count'] > 0:
        st.warning(f"**現在、{status['waiting_count']}人 が順番待ちしています**")
    else:
        st.info("**現在、順番待ちはありません**")

with wait_col2:
    if st.button("➕ 待ちに追加", use_container_width=True):
        status['waiting_count'] += 1
        save_status(status)
        st.rerun()
    if status['waiting_count'] > 0:
        if st.button("➖ 待ちを減らす", use_container_width=True):
            status['waiting_count'] -= 1
            save_status(status)
            st.rerun()
            
st.markdown("---")


# --- 🚪 シャワーセクション ---
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
            status['shower1']['start_time'] = datetime.now().isoformat()
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
            status['shower2']['start_time'] = datetime.now().isoformat()
            save_status(status)
            st.rerun()
