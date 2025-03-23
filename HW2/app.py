from flask import Flask, render_template, request, jsonify
import math
import copy

app = Flask(__name__)

# 全域變數：網格設定與模擬狀態
grid_size = 5
start_cell = None       # tuple (row, col)
end_cell = None         # tuple (row, col)
obstacles = set()       # set of (row, col)

value_grid = []         # 2D list of V(s)
simulation_finished = False
tracking_pos = None     # tuple (row, col)
tracking_path = []      # list of (row, col)
gamma = 0.7

# 定義移動方向與偏移量
directions = ['↑', '↓', '←', '→']
move_offsets = {
    '↑': (-1, 0),
    '↓': (1, 0),
    '←': (0, -1),
    '→': (0, 1)
}

def init_simulation():
    global value_grid, simulation_finished, tracking_pos, tracking_path
    value_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    simulation_finished = False
    tracking_pos = None
    tracking_path = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_grid_size', methods=['POST'])
def set_grid_size():
    global grid_size, start_cell, end_cell, obstacles
    data = request.get_json()
    grid_size = max(5, min(9, int(data['size'])))
    start_cell = None
    end_cell = None
    obstacles = set()
    init_simulation()
    return jsonify({'status': 'success', 'grid_size': grid_size})

@app.route('/set_cell', methods=['POST'])
def set_cell():
    global start_cell, end_cell, obstacles
    data = request.get_json()
    cell = tuple(data['cell'])
    cell_type = data['type']
    if cell_type == 'start':
        start_cell = cell
    elif cell_type == 'end':
        end_cell = cell
    elif cell_type == 'obstacle' and len(obstacles) < grid_size - 2:
        obstacles.add(cell)
    return jsonify({'status': 'success'})

@app.route('/simulate_step', methods=['GET'])
def simulate_step():
    global value_grid, simulation_finished, tracking_pos, tracking_path
    # 若尚未開始模擬且起點已設定，初始化追蹤位置
    if tracking_pos is None and start_cell is not None:
        tracking_pos = start_cell
        tracking_path.append(tracking_pos)
    # 進行一次 value iteration 更新
    new_value_grid = copy.deepcopy(value_grid)
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in obstacles or (end_cell is not None and (i, j) == end_cell):
                continue
            best_value = -math.inf
            for action in directions:
                di, dj = move_offsets[action]
                ni, nj = i + di, j + dj
                reward = -1
                if 0 <= ni < grid_size and 0 <= nj < grid_size:
                    if (ni, nj) in obstacles:
                        reward = -5
                        value_next = value_grid[i][j]
                    elif end_cell is not None and (ni, nj) == end_cell:
                        reward = 10
                        value_next = 0
                    else:
                        value_next = value_grid[ni][nj]
                else:
                    reward = -5
                    value_next = value_grid[i][j]
                q_value = reward + gamma * value_next
                if q_value > best_value:
                    best_value = q_value
            new_value_grid[i][j] = best_value
    value_grid = new_value_grid

    # 模擬移動：若尚未完成，從 tracking_pos 選擇 Q-value 最高的鄰格
    if not simulation_finished and tracking_pos is not None and end_cell is not None:
        current_row, current_col = tracking_pos
        if (current_row, current_col) == end_cell:
            simulation_finished = True
        else:
            best_value = -math.inf
            next_pos = None
            for action in directions:
                di, dj = move_offsets[action]
                ni, nj = current_row + di, current_col + dj
                if 0 <= ni < grid_size and 0 <= nj < grid_size and (ni, nj) not in obstacles:
                    reward = 10 if (ni, nj) == end_cell else -1
                    q_value = reward + gamma * value_grid[ni][nj]
                    if q_value > best_value:
                        best_value = q_value
                        next_pos = (ni, nj)
            if next_pos is not None:
                tracking_pos = next_pos
                tracking_path.append(tracking_pos)
                if tracking_pos == end_cell:
                    simulation_finished = True

    # 若模擬完成，計算最終路徑各格應顯示的箭頭（從當前格指向下一格）
    final_arrows = {}
    if simulation_finished:
        for i in range(len(tracking_path) - 1):
            cur = tracking_path[i]
            nxt = tracking_path[i+1]
            r, c = cur
            nr, nc = nxt
            if nr < r:
                arrow = '↑'
            elif nr > r:
                arrow = '↓'
            elif nc < c:
                arrow = '←'
            elif nc > c:
                arrow = '→'
            else:
                arrow = ''
            final_arrows[f"{r},{c}"] = arrow

    return jsonify({
        'status': 'success',
        'valueGrid': value_grid,
        'trackingPath': tracking_path,
        'simulationFinished': simulation_finished,
        'finalPathArrows': final_arrows
    })

if __name__ == '__main__':
    app.run(debug=True)
