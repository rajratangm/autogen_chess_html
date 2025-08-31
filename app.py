from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv
from simple_chess_ai import chess_ai

load_dotenv()

app = Flask(__name__)
CORS(app)

# Global variables for game state
game_state = {
    'board': None,
    'current_player': 'white',
    'game_history': [],
    'conversation_history': []  # Track the conversation between AI and human
}

# AutoGen functions removed - using simple AI only

def get_chess_board():
    """Return the initial chess board setup"""
    return [
        ['♜','♞','♝','♛','♚','♝','♞','♜'],
        ['♟','♟','♟','♟','♟','♟','♟','♟'],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        [None,None,None,None,None,None,None,None],
        ['♙','♙','♙','♙','♙','♙','♙','♙'],
        ['♖','♘','♗','♕','♔','♗','♘','♖']
    ]

def convert_move_to_algebraic(from_pos, to_pos, piece, captured=None):
    """Convert board coordinates to algebraic notation"""
    files = 'abcdefgh'
    ranks = '87654321'
    
    from_file = files[from_pos['col']]
    from_rank = ranks[from_pos['row']]
    to_file = files[to_pos['col']]
    to_rank = ranks[to_pos['row']]
    
    # Basic move notation
    move = f"{from_file}{from_rank}{to_file}{to_rank}"
    
    # Add capture symbol if piece was captured
    if captured:
        move += f"x{captured}"
    
    return move

def get_piece_color(piece):
    """Get the color of a chess piece"""
    if not piece:
        return None
    # White pieces: ♔♕♖♗♘♙
    # Black pieces: ♚♛♜♝♞♟
    white_pieces = '♔♕♖♗♘♙'
    return 'white' if piece in white_pieces else 'black'

def get_simple_ai_move(board):
    """Simple AI that makes basic moves for BLACK pieces only"""
    import random
    
    # Find all black pieces
    black_pieces = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and get_piece_color(piece) == 'black':
                black_pieces.append((row, col, piece))
    
    if not black_pieces:
        return "e5"  # Default move
    
    # Try to make a pawn move first (most common opening moves)
    for row, col, piece in black_pieces:
        if piece == '♟':  # Black pawn
            # Try to move forward (black pawns move down the board)
            if row < 7 and board[row + 1][col] is None:
                # Convert to algebraic notation
                files = 'abcdefgh'
                ranks = '87654321'
                to_square = f"{files[col]}{ranks[row + 1]}"
                return to_square
    
    # If no pawn moves, try to move knights or bishops
    for row, col, piece in black_pieces:
        if piece in '♞♝':  # Black knights and bishops
            # Try to move to an empty square in the center
            center_squares = [(3, 3), (3, 4), (4, 3), (4, 4), (2, 2), (2, 5), (5, 2), (5, 5)]
            for new_row, new_col in center_squares:
                if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] is None:
                    # Convert to algebraic notation
                    files = 'abcdefgh'
                    ranks = '87654321'
                    to_square = f"{files[new_col]}{ranks[new_row]}"
                    
                    # Add piece identifier
                    piece_map = {'♞': 'N', '♝': 'B'}
                    piece_id = piece_map.get(piece, '')
                    return f"{piece_id}{to_square}"
    
    # If no center moves, try any empty square
    for row, col, piece in black_pieces:
        if piece in '♞♝♜♛♚':  # Black pieces
            for new_row in range(8):
                for new_col in range(8):
                    if board[new_row][new_col] is None:
                        # Convert to algebraic notation
                        files = 'abcdefgh'
                        ranks = '87654321'
                        to_square = f"{files[new_col]}{ranks[new_row]}"
                        
                        # Add piece identifier
                        piece_map = {'♞': 'N', '♝': 'B', '♜': 'R', '♛': 'Q', '♚': 'K'}
                        piece_id = piece_map.get(piece, '')
                        return f"{piece_id}{to_square}"
    
    # Final fallback - try to move any black pawn
    for row in range(1, 7):  # Check pawn rows
        for col in range(8):
            piece = board[row][col]
            if piece == '♟':  # Black pawn
                if row < 7 and board[row + 1][col] is None:
                    files = 'abcdefgh'
                    ranks = '87654321'
                    to_square = f"{files[col]}{ranks[row + 1]}"
                    return to_square
    
    # Ultimate fallback
    return "e5"

def convert_algebraic_to_coords(move, board=None):
    """Convert algebraic notation to board coordinates for BLACK pieces (AI)"""
    files = 'abcdefgh'
    ranks = '87654321'
    
    # Handle standard algebraic notation (e.g., 'e5', 'Nf6', 'O-O')
    move = move.strip().lower()
    
    # Handle castling
    if move in ['o-o', '0-0', 'oo']:
        # Kingside castling for black (AI)
        return {
            'from': {'row': 0, 'col': 4},  # e8
            'to': {'row': 0, 'col': 6}     # g8
        }
    elif move in ['o-o-o', '0-0-0', 'ooo']:
        # Queenside castling for black (AI)
        return {
            'from': {'row': 0, 'col': 4},  # e8
            'to': {'row': 0, 'col': 2}     # c8
        }
    
    # Handle standard moves (e.g., 'e5', 'Nf6', 'exd5')
    if len(move) >= 2:
        # Extract destination square
        if len(move) >= 3 and move[1] in 'x':
            # Capture move (e.g., 'exd5')
            to_file = move[2]
            to_rank = move[3] if len(move) > 3 else '8'
        else:
            # Regular move (e.g., 'e5', 'Nf6')
            to_file = move[-2]
            to_rank = move[-1]
        
        try:
            to_col = files.index(to_file)
            to_row = ranks.index(to_rank)
            
            # Find the source piece based on the move type
            if len(move) == 2 and move[0] in files:
                # Pawn move (e.g., 'e5')
                from_file = move[0]
                from_col = files.index(from_file)
                
                # For black pawns, find the actual pawn on the board
                if board:
                    # Look for a black pawn in the specified file
                    for row in range(8):
                        piece = board[row][from_col]
                        if piece == '♟':  # Black pawn
                            # Check if this pawn can move to the destination
                            if row < to_row:  # Pawn moves down the board
                                return {
                                    'from': {'row': row, 'col': from_col},
                                    'to': {'row': to_row, 'col': to_col}
                                }
                
                # If no pawn found in the file, look for any black pawn that can reach the destination
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece == '♟':  # Black pawn
                            # Check if this pawn can reach the destination
                            if col == to_col and row < to_row:  # Same file, moving down
                                return {
                                    'from': {'row': row, 'col': col},
                                    'to': {'row': to_row, 'col': to_col}
                                }
                            elif abs(col - to_col) == 1 and row == to_row - 1:  # Capture move
                                return {
                                    'from': {'row': row, 'col': col},
                                    'to': {'row': to_row, 'col': to_col}
                                }
                
                # Fallback: assume pawn is at starting position
                from_row = 1  # Black pawns start at row 1
            else:
                # Piece move - find the piece on the board
                piece_type = move[0] if move[0] in 'nbrqk' else None
                if piece_type and board:
                    # Find the piece on the board
                    for row in range(8):
                        for col in range(8):
                            piece = board[row][col]
                            if piece and get_piece_color(piece) == 'black':
                                # Check if it's the right piece type
                                if (piece_type == 'n' and piece in '♞') or \
                                   (piece_type == 'b' and piece in '♝') or \
                                   (piece_type == 'r' and piece in '♜') or \
                                   (piece_type == 'q' and piece in '♛') or \
                                   (piece_type == 'k' and piece in '♚'):
                                    # For now, just return the first matching piece
                                    return {
                                        'from': {'row': row, 'col': col},
                                        'to': {'row': to_row, 'col': to_col}
                                    }
                
                # If no specific piece found, look for any black piece that can reach the destination
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece and get_piece_color(piece) == 'black':
                            # Simple check: if the piece is close to the destination
                            if abs(row - to_row) <= 2 and abs(col - to_col) <= 2:
                                return {
                                    'from': {'row': row, 'col': col},
                                    'to': {'row': to_row, 'col': to_col}
                                }
                
                # Fallback: use simple heuristic for piece moves
                from_col = to_col
                from_row = to_row + 1 if to_row < 4 else to_row - 1
            
            return {
                'from': {'row': from_row, 'col': from_col},
                'to': {'row': to_row, 'col': to_col}
            }
        except (ValueError, IndexError):
            return None
    
    return None

# AutoGen process_ai_move function removed - using simple AI only

@app.route('/')
def index():
    """Serve the main chess game page"""
    return render_template('chess_game.html')

@app.route('/api/initialize', methods=['POST'])
def initialize_game():
    """Initialize a new chess game"""
    try:
        game_state['board'] = get_chess_board()
        game_state['current_player'] = 'white'
        game_state['game_history'] = []
        game_state['conversation_history'] = []  # Reset conversation history
        
        # Reset AI conversation history
        chess_ai.reset_conversation()
        
        return jsonify({
            'success': True,
            'board': game_state['board'],
            'current_player': game_state['current_player'],
            'message': 'Game initialized successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/move', methods=['POST'])
def make_move():
    """Process a chess move and get AI response"""
    try:
        data = request.get_json()
        from_pos = data['from']
        to_pos = data['to']
        piece = data['piece']
        captured = data.get('captured')
        
        # Update game state
        if game_state['board'] is None:
            game_state['board'] = get_chess_board()
        
        # Make the move
        game_state['board'][to_pos['row']][to_pos['col']] = piece
        game_state['board'][from_pos['row']][from_pos['col']] = None
        
        # Record move
        move_record = {
            'from': from_pos,
            'to': to_pos,
            'piece': piece,
            'captured': captured,
            'player': game_state['current_player']
        }
        game_state['game_history'].append(move_record)
        
        # Convert move to algebraic notation
        move_notation = convert_move_to_algebraic(from_pos, to_pos, piece, captured)
        
        # Add human move to conversation history
        game_state['conversation_history'].append(f"Human (White): {move_notation}")
        
        # Prepare context for AI
        game_context = {
            'board': game_state['board'],
            'last_move': move_notation,
            'current_player': 'black',  # AI plays black
            'history': [convert_move_to_algebraic(m['from'], m['to'], m['piece'], m['captured']) 
                       for m in game_state['game_history']]
        }
        
        # Get AI move - ONLY use simple AI, no AutoGen
        try:
            print(f"Requesting AI move for position: {game_context['board']}")
            
            # Use ONLY simple AI approach - no AutoGen
            ai_move = chess_ai.get_move(
                game_context['board'], 
                game_context['last_move'], 
                game_context['history']
            )
            print(f"AI suggested move: {ai_move}")
            
            ai_coords = convert_algebraic_to_coords(ai_move, game_state['board'])
            print(f"Converted to coordinates: {ai_coords}")
            
            if ai_coords:
                # Validate that the AI move is legal
                from_row = ai_coords['from']['row']
                from_col = ai_coords['from']['col']
                to_row = ai_coords['to']['row']
                to_col = ai_coords['to']['col']
                
                print(f"AI move coordinates: from ({from_row},{from_col}) to ({to_row},{to_col})")
                
                # Check if the source square has a black piece
                ai_piece = game_state['board'][from_row][from_col]
                print(f"AI piece at source: {ai_piece}, color: {get_piece_color(ai_piece)}")
                
                if ai_piece and get_piece_color(ai_piece) == 'black':
                    ai_captured = game_state['board'][to_row][to_col]
                    print(f"AI captured piece: {ai_captured}")
                    
                    # Update board with AI move
                    game_state['board'][to_row][to_col] = ai_piece
                    game_state['board'][from_row][from_col] = None
                    
                    # Record AI move
                    ai_move_record = {
                        'from': ai_coords['from'],
                        'to': ai_coords['to'],
                        'piece': ai_piece,
                        'captured': ai_captured,
                        'player': 'black'
                    }
                    game_state['game_history'].append(ai_move_record)
                    
                    # Switch back to white (human player)
                    game_state['current_player'] = 'white'
                    
                    ai_response = f"AI responds with {ai_move}"
                    print(f"AI move executed: {ai_move}")
                else:
                    print(f"Invalid AI move - no black piece at source: {ai_coords}")
                    print(f"Board at source: {game_state['board'][from_row][from_col]}")
                    print("Using fallback AI move...")
                    
                    # Try fallback move
                    fallback_move = get_simple_ai_move(game_state['board'])
                    print(f"Fallback move: {fallback_move}")
                    
                    fallback_coords = convert_algebraic_to_coords(fallback_move, game_state['board'])
                    if fallback_coords:
                        from_row = fallback_coords['from']['row']
                        from_col = fallback_coords['from']['col']
                        to_row = fallback_coords['to']['row']
                        to_col = fallback_coords['to']['col']
                        
                        fallback_piece = game_state['board'][from_row][from_col]
                        if fallback_piece and get_piece_color(fallback_piece) == 'black':
                            fallback_captured = game_state['board'][to_row][to_col]
                            
                            # Update board with fallback move
                            game_state['board'][to_row][to_col] = fallback_piece
                            game_state['board'][from_row][from_col] = None
                            
                            # Record fallback move
                            fallback_move_record = {
                                'from': fallback_coords['from'],
                                'to': fallback_coords['to'],
                                'piece': fallback_piece,
                                'captured': fallback_captured,
                                'player': 'black'
                            }
                            game_state['game_history'].append(fallback_move_record)
                            
                            # Switch back to white (human player)
                            game_state['current_player'] = 'white'
                            
                            ai_response = f"AI responds with {fallback_move} (fallback)"
                            print(f"Fallback move executed: {fallback_move}")
                        else:
                            ai_response = "AI move failed - no valid fallback"
                            game_state['current_player'] = 'white'
                    else:
                        ai_response = "AI move failed - no valid fallback"
                        game_state['current_player'] = 'white'
            else:
                print(f"Could not convert AI move to coordinates: {ai_move}")
                ai_response = "AI move parsing failed"
                game_state['current_player'] = 'white'
        except Exception as e:
            print(f"AI move generation failed: {e}")
            ai_response = "AI move generation failed"
            game_state['current_player'] = 'white'
        
        return jsonify({
            'success': True,
            'board': game_state['board'],
            'current_player': game_state['current_player'],
            'move_notation': move_notation,
            'ai_response': ai_response,
            'ai_move': ai_move if 'ai_move' in locals() else None,
            'ai_coords': ai_coords if 'ai_coords' in locals() else None,
            'game_history': game_state['game_history']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Removed unused /api/ai-move endpoint - AI moves are handled in /api/move

@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    """Get current game state"""
    return jsonify({
        'board': game_state['board'],
        'current_player': game_state['current_player'],
        'game_history': game_state['game_history']
    })

if __name__ == '__main__':
    # Initialize game state
    game_state['board'] = get_chess_board()
    print("Chess game initialized with simple AI")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
