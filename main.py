import numpy as np
import random

# 보드 만들기
board = np.zeros(9, dtype=int)

# 보드 출력 함수
def show_board(board):
    symbols = {0: '.', 1: 'X', -1: 'O'}
    for i in range(3):
        row = board[i*3:(i+1)*3]
        print(" | ".join(symbols[v] for v in row))
        if i < 2:
            print("-" * 9)
    print()
print("초기:")
show_board(board)

def place_piece(board, position, player):
    """말 두기. 빈칸인지 확인."""
    if board[position] != 0:
        print(f"❌ {position}번 칸 이미 차있음!")
        return False
    
    board[position] = player
    return True

def check_winner(board):
    # 8가지 승리 조합
    lines = [
        [0, 1, 2],  # 가로 1
        [3, 4, 5],  # 가로 2
        [6, 7, 8],  # 가로 3
        [0, 3, 6],  # 세로 1
        [1, 4, 7],  # 세로 2
        [2, 5, 8],  # 세로 3
        [0, 4, 8],  # 대각선 ↘
        [2, 4, 6],  # 대각선 ↙
    ]
    for line in lines:
        # 라인 3칸의 합
        total = board[line[0]] + board[line[1]] + board[line[2]]
        
        if total == 3:
            return 1   # X 승!
        elif total == -3:
            return -1  # O 승!
    
    return 0  # 아직 승부 안 남
# 테스트: X가 가로 한 줄
print("\n=== 승리 테스트 ===")

board = np.zeros(9, dtype=int)
place_piece(board, 0, 1)  # X
place_piece(board, 1, 1)  # X
place_piece(board, 2, 1)  # X

print("X가 첫 가로:")
show_board(board)

result = check_winner(board)
print(f"승자: {result}")
if result == 1:
    print("🏆 X 승!")
elif result == -1:
    print("🏆 O 승!")
else:
    print("아직 승부 X")
    # 테스트 2: O가 대각선
print("\n=== 테스트 2: O 대각선 ===")
board = np.zeros(9, dtype=int)
place_piece(board, 2, -1)  # O
place_piece(board, 4, -1)  # O
place_piece(board, 6, -1)  # O
show_board(board)
print(f"승자: {check_winner(board)}")


# 테스트 3: 진행 중
print("\n=== 테스트 3: 진행 중 ===")
board = np.zeros(9, dtype=int)
place_piece(board, 0, 1)
place_piece(board, 4, -1)
place_piece(board, 8, 1)
show_board(board)
result = check_winner(board)
print(f"승자: {result}")
if result == 0:
    print("아직 승부 X")
    # Q-table
q_table = {}

def get_q(state, action):
    """Q값 가져오기. 없으면 0으로 초기화."""
    if state not in q_table:
        q_table[state] = np.zeros(9)
    return q_table[state][action]
# 테스트
state = (0, 0, 0, 0, 0, 0, 0, 0, 0)  # 빈 보드 튜플
print(f"Q(빈 보드, 4번 칸): {get_q(state, 4)}")
print(f"Q-table 크기: {len(q_table)}")
def choose_action(state, available_actions, epsilon=0.1):
    """행동 선택. 탐험 vs 활용."""
    if random.random() < epsilon:
        # 탐험
        return random.choice(available_actions)
    
    # 활용
    q_values = [get_q(state, a) for a in available_actions]
    max_q = max(q_values)
    best_actions = [a for a, q in zip(available_actions, q_values) if q == max_q]
    return random.choice(best_actions)
# 테스트
print("\n=== 행동 선택 테스트 ===")

board = np.zeros(9, dtype=int)
state = tuple(board)

# 빈 보드에서 행동 선택
available = [0, 1, 2, 3, 4, 5, 6, 7, 8]

for i in range(5):
    action = choose_action(state, available)
    print(f"시도 {i+1}: 선택한 칸 = {action}")


def get_available_actions(board):
    actions = []                # 빈 리스트 (모을 그릇)
    
    for i in range(9):          # ← Q1
        if board[i] == 0:      # ← Q2
            actions.append(i)   # ← Q3
    
    return actions

# 테스트 1: 빈 보드
board1 = np.zeros(9, dtype=int)
print("빈 보드:", get_available_actions(board1))

# 테스트 2: 아까 그 보드
board2 = np.array([1, 0, -1, 0, 1, 0, -1, 0, 0])
print("아까 그 보드:", get_available_actions(board2))

# 테스트 3: 거의 다 찬 보드
board3 = np.array([1, 1, -1, -1, 1, 1, -1, -1, 0])
print("거의 다 찬 보드:", get_available_actions(board3))


def is_game_over(board):
    """게임이 끝났는지 판정."""
    # 경우 1: 누군가 이김
    if check_winner(board) != 0:
        return True
    
    # 경우 2: 무승부 (빈 칸이 0개)
    if len(get_available_actions(board)) == 0:
        return True
    
    return False  # 둘 다 아니면 진행 중

# 테스트 1: 빈 보드 (진행 중)
board_a = np.zeros(9, dtype=int)
print("빈 보드:", is_game_over(board_a))
# 예상: False

# 테스트 2: X가 가로 승리 (끝남)
board_b = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0])
print("X 가로승:", is_game_over(board_b))
# 예상: True

# 테스트 3: 무승부 (꽉 찼지만 아무도 못 이김)
board_c = np.array([1, -1, 1, 1, -1, -1, -1, 1, 1])
print("무승부:", is_game_over(board_c))
# 예상: True

# 테스트 4: 진행 중 (한 자리 비어있고 아직 안 끝남)
board_d = np.array([1, -1, 1, -1, 1, -1, -1, 1, 0])
print("진행 중:", is_game_over(board_d))
# 예상: False

def play_one_game(epsilon=0.1):
    """한 판 자동으로 두기. epsilon=1.0이면 완전 랜덤."""
    board = np.zeros(9, dtype=int)
    current_player = 1
    while not is_game_over(board):
        show_board(board)

        state = tuple(board)
        available = get_available_actions(board)
        action = choose_action(state, available, epsilon)

        place_piece(board, action, current_player)

        current_player = current_player * -1

    # ↓ 여기부터는 while 밖! 게임 끝난 후
    show_board(board)
    return check_winner(board)


# ↓ 함수 밖! 테스트 코드
print("\n=== 첫 게임 ===")
winner = play_one_game(epsilon=1.0)

print(f"\n승자 코드: {winner}")
if winner == 1:
    print("🏆 X 승!")
elif winner == -1:
    print("🏆 O 승!")
else:
    print("🤝 무승부!")


# Q-update
def update_q(state, action, reward, next_state, alpha=0.1, gamma=0.9):
    """Q값 업데이트 — 벨만 방정식."""

    # Step 1: 옛 예측 (현재 Q값)
    old_q = get_q(state, action)

    # Step 2: 다음 상태에서 최선 가치
    next_board = np.array(next_state)      # tuple → array (함수들이 받게)

    if is_game_over(next_board):
        max_next_q = 0
    else:
        available = get_available_actions(next_board)

        # 빈 칸들의 Q값 다 모으기
        q_values = []
        for a in available:
            q = get_q(next_state, a)
            q_values.append(q)

        # 그 중 최대
        max_next_q = max(q_values)

    # Step 3: target = 실제 가치 (= r + γ × 미래)
    target = reward + gamma * max_next_q   # ← 다음에 채울 빈칸

    # Step 4: new_q = 옛 + α × (실제 - 옛)
    new_q = old_q + alpha *(target - old_q)   # ← 다음에 채울 빈칸

    # Step 5: q_table에 저장
    q_table[state][action] = new_q


# 테스트
print("\n=== update_q 테스트 1: 즉시 승리 ===")
q_table.clear()  # Q-table 깨끗하게 초기화

state = (1, 1, 0, 0, 0, 0, 0, 0, 0)      # X X _ / _ _ _ / _ _ _
action = 2                                # X가 2번 → 가로 승!
reward = 1                                # 이김
next_state = (1, 1, 1, 0, 0, 0, 0, 0, 0)  # 승리 보드

print(f"학습 전 Q값: {get_q(state, action)}")
update_q(state, action, reward, next_state)
print(f"학습 후 Q값: {get_q(state, action)}")
print("예상: 0.1")


print("\n=== update_q 테스트 2: 같은 경험 5번 반복 ===")
q_table.clear()

state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
action = 0
next_state = (1, 0, 0, 0, 0, 0, 0, 0, 0)

print(f"초기 Q값: {get_q(state, action):.4f}")
for i in range(5):
    update_q(state, action, reward=1, next_state=next_state)
    print(f"  {i+1}번째 학습 후: {get_q(state, action):.4f}")
print("예상: 0 → 0.1 → 0.19 → 0.271 → 0.3439 → 0.4095")
print("(천천히 1.0(=reward)에 수렴)")


# RL Training Loop
def play_and_learn(epsilon=0.1):
    """한 판 두면서 학습까지."""
    board = np.zeros(9, dtype=int)
    current_player = 1
    history = []                              # ① 빈 노트

    while not is_game_over(board):
        state = tuple(board)
        available = get_available_actions(board)
        action = choose_action(state, available, epsilon)

        history.append((state, action, current_player))  # ② 노트에 기록

        place_piece(board, action, current_player)
        current_player = current_player * -1

    # 게임 끝
    winner = check_winner(board)
    final_state = tuple(board)

    # history 쭉 돌면서 학습
    for state, action, player in history:
        if winner == 0:
            reward = 0
        elif winner == player:
            reward = 1
        else:
            reward = -1

        update_q(state, action, reward, final_state)

    return winner

def train(num_games=10000):
    """반복적으로 play_and_learn 호출 = AI 학습."""
    wins = {1: 0, -1: 0, 0: 0}   # X승, O승, 무

    for i in range(num_games):
        winner = play_and_learn(epsilon=0.1)
        wins[winner] += 1

        if (i + 1) % 1000 == 0:
            print(f"{i+1}판 | X승: {wins[1]}, O승: {wins[-1]}, 무: {wins[0]} | q_table: {len(q_table)}")

    return wins


print("\n=== 학습 시작 ===")
q_table.clear()
results = train(num_games=10000)
print(f"\n최종: X승 {results[1]}, O승 {results[-1]}, 무 {results[0]}")
print(f"q_table 학습된 상태 수: {len(q_table)}")


def play_vs_human(human_player=1):
    """사람 vs AI.
    human_player=1이면 사람이 X(선공), -1이면 사람이 O(후공)."""
    board = np.zeros(9, dtype=int)
    current_player = 1   # X 항상 선공

    print("\n=== 사람 vs AI ===")
    print(f"사람: {'X (선공)' if human_player == 1 else 'O (후공)'}")
    print(f"AI:   {'O (후공)' if human_player == 1 else 'X (선공)'}")

    while not is_game_over(board):
        show_board(board)

        if current_player == human_player:
            # 사람 차례
            available = get_available_actions(board)
            print(f"빈 칸: {available}")
            while True:
                try:
                    action = int(input("어디에 둘래요? (0-8): "))
                    if action in available:
                        break
                    print(f"❌ {action}번엔 못 둠. 다시.")
                except ValueError:
                    print("❌ 숫자만 입력.")
        else:
            # AI 차례
            state = tuple(board)
            available = get_available_actions(board)
            action = choose_action(state, available, epsilon=0)   # 완전 활용
            print(f"🤖 AI가 {action}번에 둠")

        place_piece(board, action, current_player)
        current_player *= -1

    show_board(board)
    winner = check_winner(board)
    if winner == 0:
        print("🤝 무승부!")
    elif winner == human_player:
        print("🎉 사람 승!")
    else:
        print("🤖 AI 승!")
    return winner


# 게임 시작
play_vs_human(human_player=1)   # 사람이 X (선공). -1로 바꾸면 후공.
