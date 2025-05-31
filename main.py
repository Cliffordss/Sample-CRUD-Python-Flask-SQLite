from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import game_controller
from game_controller import GameError
from db import create_tables
from api import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Required for flash messages
app.config['DATABASE_NAME'] = 'games.db'  # Set default database name

# Register the API blueprint
app.register_blueprint(api_bp)

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return {'error': 'Resource not found'}, 404
    flash('Page not found', 'error')
    return redirect(url_for('list_games'))

@app.errorhandler(GameError)
def handle_game_error(error):
    if request.path.startswith('/api/'):
        return {'error': str(error)}, error.code
    flash(str(error), 'error')
    return redirect(url_for('list_games'))

@app.route('/')
def index():
    return redirect(url_for('list_games'))

@app.route('/games', methods=["GET"])
def list_games():
    try:
        games = game_controller.get_games()
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"games": games, "count": len(games)}), 200
        return render_template('index.html', games=games)
    except GameError as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": str(e)}), e.code
        flash(str(e), 'error')
        return render_template('index.html', games=[])

@app.route('/games/new', methods=['GET', 'POST'])
def create_game_form():
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            rate = int(request.form['rate'])
            
            result = game_controller.insert_game(name, price, rate)
            flash('Game created successfully!', 'success')
            return redirect(url_for('list_games'))
        except (ValueError, KeyError) as e:
            flash('Invalid input data. Please check your form.', 'error')
            return render_template('create.html'), 400
    
    return render_template('create.html')

@app.route('/games/<id>/edit', methods=['GET', 'POST'])
def edit_game_form(id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            price = float(request.form['price'])
            rate = int(request.form['rate'])
            
            result = game_controller.update_game(id, name, price, rate)
            flash('Game updated successfully!', 'success')
            return redirect(url_for('list_games'))
        except (ValueError, KeyError) as e:
            flash('Invalid input data. Please check your form.', 'error')
            return render_template('edit.html', game=game_controller.get_by_id(id)), 400
    
    game = game_controller.get_by_id(id)
    return render_template('edit.html', game=game)

@app.route("/game/<id>", methods=["DELETE", "POST"])
def delete_game(id):
    try:
        game_controller.delete_game(id)
        if request.method == "DELETE":
            return '', 204
        flash('Game was successfully deleted!', 'success')
        return redirect(url_for('list_games'))
    except GameError as e:
        if request.method == "DELETE":
            return jsonify({"error": str(e)}), e.code
        flash(str(e), 'error')
        return redirect(url_for('list_games'))

@app.route("/game/<id>", methods=["GET"])
def get_game_by_id(id):
    try:
        game = game_controller.get_by_id(id)
        if request.headers.get('Accept') == 'application/json':
            return jsonify(game), 200
        return render_template('game.html', game=game)
    except GameError as e:
        if request.headers.get('Accept') == 'application/json':
            return jsonify({"error": str(e)}), e.code
        flash('Game not found', 'error')
        return redirect(url_for('list_games'))

"""
Enable CORS. Disable it if you don't need CORS
"""
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

if __name__ == "__main__":
    with app.app_context():
        create_tables()
    """
    Here you can change debug and port
    Remember that, in order to make this API functional, you must set debug in False
    """
    app.run(host='0.0.0.0', port=8000, debug=True)
