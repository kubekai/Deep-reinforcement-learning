from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__)

# 全域變數存儲網格資訊
grid_size = 5
start_cell = None
end_cell = None
obstacles = set()

@app.route('/')
def index():
    return render_template('index.html', grid_size=grid_size)

@app.route('/set_grid_size', methods=['POST'])
def set_grid_size():
    global grid_size, start_cell, end_cell, obstacles
    data = request.get_json()
    grid_size = max(5, min(9, int(data['size'])))
    start_cell = None
    end_cell = None
    obstacles.clear()
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

@app.route('/get_policy_value', methods=['GET'])
def get_policy_value():
    values = np.random.uniform(-4, 2, (grid_size, grid_size))
    policy = np.random.choice(['↑', '↓', '←', '→'], (grid_size, grid_size))
    return jsonify({'values': values.tolist(), 'policy': policy.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
