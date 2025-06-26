import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="萌宇星球小伙伴", layout="wide")

if "responses" not in st.session_state:
    st.session_state.responses = []

options = [
    "AI 人工智能",
    "生命科学",
    "植物机器人",
    "脑机接口",
    "太空探索",
    "编程与游戏开发",
    "硬核造物",
    "元宇宙与数字创作"
]

col1, col2 = st.columns(2)

with col1:
    st.title("🌟 萌宇星球小伙伴")
    st.write("请选择你最感兴趣的探索方向（可多选）👇")

    selected = st.multiselect("我感兴趣的方向：", options)

    if st.button("提交"):
        if selected:
            st.session_state.responses.extend(selected)
            st.success("提交成功 ✅")
        else:
            st.warning("请至少选择一个方向")

with col2:
    st.title("📊 实时词云展示")
    st.write("大家选择的兴趣方向，看看哪个最受欢迎 👇")

    if st.session_state.responses:
        counter = Counter(st.session_state.responses)
        wordcloud = WordCloud(
            font_path="STHeiti Light.ttc",
            width=800, height=400, background_color="white"
        ).generate_from_frequencies(counter)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("目前还没有数据，请先提交兴趣方向")

