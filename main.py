import streamlit as st
import pydeck as pdk
import numpy as np
import time

st.title("3D 판 구조론 시뮬레이션")

# 사용자 입력
st.sidebar.header("판 이동 조건 설정")

speed1 = st.sidebar.slider("판 1 속도 (cm/년)", 0.0, 10.0, 5.0)
speed2 = st.sidebar.slider("판 2 속도 (cm/년)", 0.0, 10.0, 5.0)

direction1 = st.sidebar.selectbox("판 1 방향", ["왼쪽 → 오른쪽", "오른쪽 → 왼쪽"])
direction2 = st.sidebar.selectbox("판 2 방향", ["왼쪽 → 오른쪽", "오른쪽 → 왼쪽"])

boundary_type = st.sidebar.selectbox("판 경계 유형", ["발산", "수렴", "보존"])

def dir_to_sign(d):
    return 1 if d == "왼쪽 → 오른쪽" else -1

v1 = speed1 * dir_to_sign(direction1)
v2 = speed2 * dir_to_sign(direction2)

# 초기 위치 (x좌표 기준)
pos1 = 0
pos2 = 10

# 판 크기
plate_length = 4
plate_height = 1
plate_depth = 2

# 판을 나타내는 박스 생성 함수
def create_plate(x, color):
    # pydeck의 CubeLayer에 맞게 박스 좌표 설정
    return {
        "position": [x, 0, 0],
        "color": color,
        "dimensions": [plate_length, plate_height, plate_depth]
    }

# 애니메이션 프레임 생성 함수
def generate_frames(frames=100):
    positions1 = np.zeros(frames)
    positions2 = np.zeros(frames)
    positions1[0] = pos1
    positions2[0] = pos2

    dt = 0.1
    for t in range(1, frames):
        positions1[t] = positions1[t-1] + v1 * dt
        positions2[t] = positions2[t-1] + v2 * dt
    return positions1, positions2

positions1, positions2 = generate_frames()

# Deck.gl CubeLayer 설정
def create_deck_layer(x1, x2):
    data = [
        create_plate(x1, [0, 128, 255]),  # 파란 판 1
        create_plate(x2, [255, 64, 64])    # 빨간 판 2
    ]

    layer = pdk.Layer(
        "CubeLayer",
        data=data,
        get_position="position",
        get_color="color",
        get_dimensions="dimensions",
        pickable=True,
        auto_highlight=True,
        opacity=0.8,
        wireframe=True,
    )
    return layer

# 뷰 설정 (3D 카메라)
view_state = pdk.ViewState(
    longitude=0,
    latitude=0,
    zoom=12,
    pitch=45,
    bearing=0
)

# 시뮬레이션 애니메이션
plot_placeholder = st.empty()

for t in range(len(positions1)):
    layer = create_deck_layer(positions1[t], positions2[t])

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style=None,
        tooltip={"text": "판 구조 시뮬레이션"}
    )

    plot_placeholder.pydeck_chart(r)

    # 충돌 간단 감지 및 진동 효과 (수렴 경계일 때)
    if boundary_type == "수렴":
        dist = abs(positions2[t] - positions1[t])
        if dist < plate_length:
            # 진동 애니메이션 (판 위치 약간 흔들기)
            offset = 0.1 * np.sin(t * 10)
            positions1[t] += offset
            positions2[t] -= offset

    time.sleep(0.05)

st.markdown("""
### 판 경계 유형 설명
- 발산: 판들이 서로 멀어지는 경계
- 수렴: 판들이 서로 충돌하는 경계 (진동, 지진 효과 포함)
- 보존: 판들이 옆으로 미끄러지듯 움직이는 경계
""")
