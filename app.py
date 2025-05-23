import streamlit as st
import matplotlib.pyplot as plt

# 기본 설정
x_range = (-10, 10)
y_range = (-10, 10)
board_bg_color = '#f0d9b5'

# 세션 상태 초기화
if 'stones' not in st.session_state:
    st.session_state.stones = []
if 'current_color' not in st.session_state:
    st.session_state.current_color = 'black'
if 'players' not in st.session_state:
    st.session_state.players = {}
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# 제목
st.markdown("<h1 style='text-align: center; color: brown;'>인디언 오목</h1>", unsafe_allow_html=True)

# 플레이어 입력
with st.sidebar:
    st.header("플레이어 설정")
    p1 = st.text_input("플레이어 1 이름", "Player1")
    p2 = st.text_input("플레이어 2 이름", "Player2")
    if st.button("게임 시작"):
        import random
        if random.choice([True, False]):
            st.session_state.players = {'black': p1, 'white': p2}
        else:
            st.session_state.players = {'black': p2, 'white': p1}
        st.session_state.stones = []
        st.session_state.current_color = 'black'
        st.session_state.game_over = False

# 돌 그리기 함수
def draw_board():
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_facecolor(board_bg_color)
    ax.set_xticks(range(x_range[0], x_range[1]+1))
    ax.set_yticks(range(y_range[0], y_range[1]+1))
    ax.grid(True)
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.set_title("좌표평면 오목판", fontsize=14)

    for x, y, color in st.session_state.stones:
        ax.plot(x, y, 'o', markersize=10, color=color)

    return fig

# 승리 체크 함수
def check_win(x, y, color):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    for dx, dy in directions:
        count = 1
        for dir in [1, -1]:
            nx, ny = x + dx * dir, y + dy * dir
            while (nx, ny, color) in st.session_state.stones:
                count += 1
                nx += dx * dir
                ny += dy * dir
        if count >= 5:
            return True
    return False

# 게임 진행
if st.session_state.players:
    current = st.session_state.current_color
    st.subheader(f"{st.session_state.players[current]}님의 차례입니다! ({current})")

    coord_input = st.text_input("좌표를 (x,y) 형태로 입력하세요 (예: 1,2)")
    if st.button("돌 놓기") and not st.session_state.game_over:
        try:
            x, y = map(int, coord_input.strip("() ").split(","))
            if x < x_range[0] or x > x_range[1] or y < y_range[0] or y > y_range[1]:
                st.warning("범위 내 좌표를 입력하세요!")
            elif any(sx == x and sy == y for sx, sy, _ in st.session_state.stones):
                st.warning("이미 돌이 있는 자리입니다!")
            else:
                st.session_state.stones.append((x, y, current))
                if check_win(x, y, current):
                    st.session_state.game_over = True
                    st.success(f"🎉 {st.session_state.players[current]}님이 승리하셨습니다! 🎉")
                else:
                    st.session_state.current_color = 'white' if current == 'black' else 'black'
        except:
            st.warning("올바른 형식으로 입력해주세요. 예: 2,3")

# 보드 출력
st.pyplot(draw_board())
