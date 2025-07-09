import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from io import BytesIO

st.title("자연현상 시뮬레이션 - 판 충돌 예제")

# 1. 사용자 입력
st.sidebar.header("판 충돌 조건 설정")

speed_plate1 = st.sidebar.slider("판 1 속도 (단위: cm/년)", 0.0, 10.0, 5.0)
speed_plate2 = st.sidebar.slider("판 2 속도 (단위: cm/년)", 0.0, 10.0, 5.0)
direction_plate1 = st.sidebar.selectbox("판 1 방향", ["왼쪽 → 오른쪽", "오른쪽 → 왼쪽"])
direction_plate2 = st.sidebar.selectbox("판 2 방향", ["왼쪽 → 오른쪽", "오른쪽 → 왼쪽"])

# 속도 부호 결정
def direction_to_sign(direction):
    return 1 if direction == "왼쪽 → 오른쪽" else -1

v1 = speed_plate1 * direction_to_sign(direction_plate1)
v2 = speed_plate2 * direction_to_sign(direction_plate2)

# 2. 시뮬레이션 파라미터
time_steps = 100
plate1_pos = np.zeros(time_steps)
plate2_pos = np.zeros(time_steps)

# 초기 위치 (판 1은 왼쪽, 판 2는 오른쪽)
plate1_pos[0] = 0
plate2_pos[0] = 10

# 3. 위치 계산
for t in range(1, time_steps):
    plate1_pos[t] = plate1_pos[t-1] + v1 * 0.1  # 0.1은 시간 간격 (가상 단위)
    plate2_pos[t] = plate2_pos[t-1] + v2 * 0.1

# 4. 애니메이션 생성
fig, ax = plt.subplots()
ax.set_xlim(-5, 15)
ax.set_ylim(-1, 1)
plate1_line, = ax.plot([], [], 'b-', linewidth=10, label="판 1")
plate2_line, = ax.plot([], [], 'r-', linewidth=10, label="판 2")
ax.legend()

def init():
    plate1_line.set_data([], [])
    plate2_line.set_data([], [])
    return plate1_line, plate2_line

def update(frame):
    # 판 1 위치
    plate1_x = [plate1_pos[frame], plate1_pos[frame] + 2]  # 판 길이 2 단위
    plate1_y = [0.5, 0.5]
    plate1_line.set_data(plate1_x, plate1_y)
    
    # 판 2 위치
    plate2_x = [plate2_pos[frame], plate2_pos[frame] + 2]
    plate2_y = [-0.5, -0.5]
    plate2_line.set_data(plate2_x, plate2_y)
    
    return plate1_line, plate2_line

ani = FuncAnimation(fig, update, frames=time_steps, init_func=init, blit=True, interval=100)

# 5. Streamlit에서 애니메이션 출력하기 (GIF로 변환 필요)
import matplotlib.animation as animation
import tempfile

with tempfile.NamedTemporaryFile(suffix='.gif') as tmpfile:
    ani.save(tmpfile.name, writer='pillow')
    st.image(tmpfile.name, caption="판 충돌 시뮬레이션")

st.markdown("""
판 1과 판 2의 속도 및 이동 방향을 조절하여 두 판이 어떻게 충돌하거나 멀어지는지 시뮬레이션할 수 있습니다.
""")
