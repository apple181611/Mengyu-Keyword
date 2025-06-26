import streamlit as st
import sqlite3
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import os

st.set_page_config(page_title="关键词词云 - SQLite 版", layout="wide")

DB_PATH = "keywords.db"

# 创建数据库和表（如果尚未存在）
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS keywords (word TEXT)")
    conn.commit()
    conn.close()

def insert_keyword(word):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO keywords (word) VALUES (?)", (word,))
    conn.commit()
    conn.close()

def fetch_keywords():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT word FROM keywords")
    words = [row[0] for row in c.fetchall()]
    conn.close()
    return words

def clear_keywords():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM keywords")
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 页面 UI
st.title("🧠 萌宇星球 · 关键词提交平台（多用户同步）")

st.markdown("每位同学请提交一个你想到的关键词👇")

keyword = st.text_input("请输入你的关键词（只能填写一个）", "")

if st.button("✅ 提交"):
    if keyword.strip():
        insert_keyword(keyword.strip())
        st.success("已提交！等待老师点击生成词云 👀")
    else:
        st.warning("请先输入一个关键词")

st.divider()
st.subheader("🧑‍🏫 老师控制区")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 生成词云图"):
        st.session_state.show_wordcloud = True

with col2:
    if st.button("🗑️ 清空所有数据"):
        clear_keywords()
        st.session_state.show_wordcloud = False
        st.success("✅ 数据已清空")

if st.session_state.get("show_wordcloud", False):
    st.subheader("🌈 关键词词云展示")
    keywords = fetch_keywords()
    if keywords:
        counter = Counter(keywords)
        wordcloud = WordCloud(
            width=800, height=400, background_color="white"
        ).generate_from_frequencies(counter)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("暂无数据，请先提交关键词")
