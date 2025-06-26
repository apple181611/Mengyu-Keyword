import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 页面设置
st.set_page_config(page_title="关键词统计器", layout="wide")

# 初始化状态
if "keywords" not in st.session_state:
    st.session_state.keywords = []
if "show_wordcloud" not in st.session_state:
    st.session_state.show_wordcloud = False

# 页面标题
st.title("🧠 萌宇星球 · 关键词提交平台")

st.markdown("每位同学请提交一个你想到的关键词👇")

# 输入框
keyword = st.text_input("请输入你的关键词（只能填写一个）", "")

# 提交按钮
if st.button("✅ 提交"):
    if keyword.strip():
        st.session_state.keywords.append(keyword.strip())
        st.success("已提交！等待老师点击生成词云 👀")
    else:
        st.warning("请先输入一个关键词")

st.divider()

# 老师控制区
st.subheader("🧑‍🏫 老师控制区")

col1, col2 = st.columns(2)

with col1:
    if st.button("📊 生成词云"):
        if len(st.session_state.keywords) == 0:
            st.warning("还没有学生提交内容哦！")
        else:
            st.session_state.show_wordcloud = True

with col2:
    if st.button("🗑️ 重置所有数据"):
        st.session_state.keywords = []
        st.session_state.show_wordcloud = False
        st.success("已清空所有提交内容")

# 显示词云
if st.session_state.show_wordcloud:
    st.subheader("🌈 关键词词云展示")

    counter = Counter(st.session_state.keywords)
    wordcloud = WordCloud(
        font_path="simhei.ttf",  # 保证你的仓库里有 simhei.ttf 中文字体
        width=800, height=400,
        background_color="white"
    ).generate_from_frequencies(counter)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
