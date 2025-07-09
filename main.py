# 자연현상 시각화 웹서비스 - Streamlit 기반
# 필요한 라이브러리: streamlit, matplotlib, plotly, numpy

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="자연 현상 시뮬레이터", layout="wide")
st.title("🌀 자연 현상 시뮬레이션 도구")

# 사이드바 메뉴 구성
category = st.sidebar.selectbox("자연 현상 카테고리 선택", ["판의 경계", "지구 내부 구조", "기상 현상과 대기 순환"])

# 판의 경계 시뮬레이션 함수
def simulate_plate_boundary():
    boundary_type = st.selectbox("판 경계 유형 선택", ["발산형 경계", "수렴형 경계", "보존형 경계"])

    if boundary_type == "발산형 경계":
        st.markdown("### 🟦 발산형 경계: 판이 서로 멀어지는 현상")
        fig, ax = plt.subplots()
        x = np.linspace(-10, 10, 100)
        y1 = np.tanh(x)
        y2 = -np.tanh(x)
        ax.plot(x, y1, 'r', label='판 A')
        ax.plot(x, y2, 'b', label='판 B')
        ax.set_title("발산하는 판의 시각화")
        ax.legend()
        st.pyplot(fig)

    elif boundary_type == "수렴형 경계":
        st.markdown("### 🔻 수렴형 경계: 판이 서로 충돌하여 밀려나는 현상")
        fig, ax = plt.subplots()
        x = np.linspace(-5, 5, 100)
        y1 = -np.abs(x) + 5
        ax.fill_between(x, y1, color='orange')
        ax.set_title("수렴하는 판의 충돌")
        st.pyplot(fig)

    else:
        st.markdown("### ↔ 보존형 경계: 수평으로 이동하는 판")
        angle = st.slider("판 이동 방향 (도)", 0, 360, 45)
        fig, ax = plt.subplots()
        ax.quiver(0, 0, np.cos(np.radians(angle)), np.sin(np.radians(angle)), scale=1, scale_units='xy', angles='xy')
        ax.quiver(0, 0, -np.cos(np.radians(angle)), -np.sin(np.radians(angle)), color='r', scale=1, scale_units='xy', angles='xy')
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_aspect('equal')
        ax.set_title("보존형 경계의 상대 이동 방향")
        st.pyplot(fig)

# 지구 내부 구조 시뮬레이션 함수
def simulate_earth_layers():
    st.markdown("### 🌍 지구 내부 구조 시각화")
    layer_names = ['내핵', '외핵', '맨틀', '지각']
    layer_radii = [1, 2, 3.5, 4]  # 임의 단위
    colors = ['red', 'orange', 'blue', 'gray']

    fig, ax = plt.subplots()
    for i in range(len(layer_radii)-1, -1, -1):
        circle = plt.Circle((0, 0), layer_radii[i], color=colors[i], label=layer_names[i])
        ax.add_artist(circle)
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect('equal')
    ax.set_title("지구 내부 구조 단면도")
    ax.legend()
    st.pyplot(fig)

# 기상 현상 시뮬레이션 함수
def simulate_weather_fronts():
    front_type = st.selectbox("기상 현상 선택", ["온난 전선", "한랭 전선", "정체 전선", "폐색 전선"])

    st.markdown(f"### ☁️ {front_type} 시각화")
    x = np.linspace(0, 10, 100)
    y_hot = np.sin(x)
    y_cold = np.cos(x)

    fig = go.Figure()
    if front_type == "온난 전선":
        fig.add_trace(go.Scatter(x=x, y=y_hot, mode='lines', line=dict(color='red'), name='따뜻한 공기'))
        fig.add_trace(go.Scatter(x=x, y=y_cold - 1, mode='lines', line=dict(color='blue'), name='차가운 공기'))
    elif front_type == "한랭 전선":
        fig.add_trace(go.Scatter(x=x, y=y_cold, mode='lines', line=dict(color='blue'), name='차가운 공기'))
        fig.add_trace(go.Scatter(x=x, y=y_hot + 1, mode='lines', line=dict(color='red'), name='따뜻한 공기'))
    else:
        fig.add_trace(go.Scatter(x=x, y=y_hot, mode='lines', line=dict(color='red', dash='dot'), name='따뜻한 공기'))
        fig.add_trace(go.Scatter(x=x, y=y_cold, mode='lines', line=dict(color='blue', dash='dot'), name='차가운 공기'))

    fig.update_layout(height=400, width=800, title=f"{front_type} 애니메이션 표현", xaxis_title="거리", yaxis_title="고도")
    st.plotly_chart(fig)

# 카테고리에 따른 시뮬레이션 호출
if category == "판의 경계":
    simulate_plate_boundary()
elif category == "지구 내부 구조":
    simulate_earth_layers()
else:
    simulate_weather_fronts()
