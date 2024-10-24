from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

class SnakeGame:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.snake = [(10, 10)]
        self.direction = 'right'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        while True:
            food = (random.randint(0, self.width-1), 
                   random.randint(0, self.height-1))
            if food not in self.snake:
                return food
    
    def move(self, direction):
        if self.game_over:
            return
        
        head = self.snake[0]
        if direction == 'right':
            new_head = ((head[0] + 1) % self.width, head[1])
        elif direction == 'left':
            new_head = ((head[0] - 1) % self.width, head[1])
        elif direction == 'up':
            new_head = (head[0], (head[1] - 1) % self.height)
        elif direction == 'down':
            new_head = (head[0], (head[1] + 1) % self.height)
        
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

game = SnakeGame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    game.move(direction)
    return jsonify({
        'snake': game.snake,
        'food': game.food,
        'score': game.score,
        'game_over': game.game_over
    })

@app.route('/reset', methods=['POST'])
def reset():
    global game
    game = SnakeGame()
    return jsonify({
        'snake': game.snake,
        'food': game.food,
        'score': game.score,
        'game_over': game.game_over
    })

if __name__ == '__main__':
    app.run(debug=True)