from flask_restx import Api, Resource, fields, marshal
from flask import Blueprint
import game_controller
from game_controller import GameError

# Create a blueprint for the API
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp,
          title='Games API',
          version='1.0',
          description='A simple Games API for managing video games',
          doc='/docs')

# Define models for request/response
game_model = api.model('Game', {
    'id': fields.Integer(readonly=True, description='The game unique identifier'),
    'name': fields.String(required=True, description='The game name'),
    'price': fields.Float(required=True, description='The game price'),
    'rate': fields.Integer(required=True, description='The game rating (1-5)'),
    'created_at': fields.String(readonly=True, description='Creation timestamp'),
    'updated_at': fields.String(readonly=True, description='Last update timestamp')
})

game_input = api.model('GameInput', {
    'name': fields.String(required=True, description='The game name'),
    'price': fields.Float(required=True, description='The game price'),
    'rate': fields.Integer(required=True, description='The game rating (1-5)')
})

# Error messages model
error_model = api.model('Error', {
    'error': fields.String(required=True, description='Error message')
})

@api.errorhandler(GameError)
def handle_game_error(error):
    return {'error': str(error)}, error.code

@api.errorhandler(Exception)
def handle_general_error(error):
    return {'error': str(error)}, 500

@api.route('/games')
class GameList(Resource):
    @api.doc('list_games')
    @api.marshal_list_with(game_model)
    def get(self):
        """List all games"""
        return game_controller.get_games()

    @api.doc('create_game')
    @api.expect(game_input)
    @api.response(201, 'Game created successfully', game_model)
    @api.response(400, 'Validation Error', error_model)
    def post(self):
        """Create a new game"""
        try:
            result = game_controller.insert_game(
                api.payload['name'],
                api.payload['price'],
                api.payload['rate']
            )
            return marshal(result, game_model), 201
        except GameError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': str(e)}, 400

@api.route('/games/<int:id>')
@api.param('id', 'The game identifier')
class Game(Resource):
    @api.doc('get_game')
    @api.response(200, 'Success', game_model)
    @api.response(404, 'Game not found', error_model)
    def get(self, id):
        """Fetch a game by ID"""
        try:
            result = game_controller.get_by_id(id)
            return marshal(result, game_model)
        except GameError as e:
            return {'error': str(e)}, 404

    @api.doc('update_game')
    @api.expect(game_input)
    @api.response(200, 'Success', game_model)
    @api.response(400, 'Validation Error', error_model)
    @api.response(404, 'Game not found', error_model)
    def put(self, id):
        """Update a game"""
        try:
            result = game_controller.update_game(
                id,
                api.payload['name'],
                api.payload['price'],
                api.payload['rate']
            )
            return marshal(result, game_model)
        except GameError as e:
            return {'error': str(e)}, e.code
        except Exception as e:
            return {'error': str(e)}, 400

    @api.doc('delete_game')
    @api.response(204, 'Game deleted')
    @api.response(404, 'Game not found', error_model)
    def delete(self, id):
        """Delete a game"""
        try:
            game_controller.delete_game(id)
            return '', 204
        except GameError as e:
            return {'error': str(e)}, 404 