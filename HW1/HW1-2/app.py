from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

directions = ['↑', '↓', '←', '→']
move_offsets = {'↑': (-1, 0), '↓': (1, 0), '←': (0, -1), '→': (0, 1)}

def initialize_grid(size):
    return np.zeros((size, size))

def generate_policy(grid_size, start, end, obstacles):
    policy = {}
    direction_count = {d: 0 for d in directions}
    total_cells = grid_size ** 2 - len(obstacles) - 2
    avg_count = total_cells // 4
    
    for i in range(grid_size):
        for j in range(grid_size):
            key = f"{i},{j}"
            if key in obstacles or key == start or key == end:
                continue
            
            available_dirs = directions[:]
            available_dirs.sort(key=lambda d: np.abs((i + move_offsets[d][0]) - int(end.split(',')[0])) + 
                                            np.abs((j + move_offsets[d][1]) - int(end.split(',')[1])))
            
            selected_dir = next((d for d in available_dirs if direction_count[d] < avg_count), available_dirs[0])
            direction_count[selected_dir] += 1
            policy[key] = selected_dir
    
    return policy

def evaluate_policy(grid_size, policy, obstacles, end):
    gamma = 0.7
    threshold = 0.00001
    value_grid = np.zeros((grid_size, grid_size))
    delta = float('inf')
    
    while delta > threshold:
        delta = 0
        new_value_grid = value_grid.copy()
        
        for i in range(grid_size):
            for j in range(grid_size):
                key = f"{i},{j}"
                if key in obstacles or key == end:
                    continue
                
                action = policy.get(key)
                if action:
                    di, dj = move_offsets[action]
                    ni, nj = i + di, j + dj
                    reward = 10 if key == end else -1
                    expected_value = -5 if (ni < 0 or ni >= grid_size or nj < 0 or nj >= grid_size or f"{ni},{nj}" in obstacles) else reward + gamma * value_grid[ni, nj]
                    new_value_grid[i, j] = expected_value
                    delta = max(delta, abs(new_value_grid[i, j] - value_grid[i, j]))
        
        value_grid = new_value_grid
    
    return value_grid.tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_policy', methods=['POST'])
def generate_policy_route():
    data = request.json
    grid_size = data['gridSize']
    start = data['start']
    end = data['end']
    obstacles = set(data['obstacles'])
    
    policy = generate_policy(grid_size, start, end, obstacles)
    return jsonify(policy)

@app.route('/evaluate_policy', methods=['POST'])
def evaluate_policy_route():
    data = request.json
    grid_size = data['gridSize']
    policy = data['policy']
    obstacles = set(data['obstacles'])
    end = data['end']
    
    value_grid = evaluate_policy(grid_size, policy, obstacles, end)
    return jsonify(value_grid)

if __name__ == '__main__':
    app.run(debug=True)
