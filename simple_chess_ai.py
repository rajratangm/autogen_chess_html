#!/usr/bin/env python3
"""
Simple Chess AI that ensures proper turn-based gameplay
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class SimpleChessAI:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history = []
        
    def get_move(self, board, last_move, move_history):
        """Get AI move based on current position"""
        try:
            # Build context for the AI
            context = f"""
            You are playing Black in a chess game against White.
            
            Current board position:
            {board}
            
            White's last move: {last_move}
            Move history: {move_history}
            
            It's your turn (Black). Analyze the position and respond with your next move in standard algebraic notation.
            Examples: 'e5', 'Nf6', 'O-O', 'exd5', 'Qe7'
            
            IMPORTANT: Only make valid moves with Black pieces. Make sure the piece you want to move actually exists on the board.
            
            Respond with just the move notation, no explanations.
            """
            
            # Add conversation history
            if self.conversation_history:
                context += "\n\nPrevious moves:\n"
                for msg in self.conversation_history[-5:]:
                    context += f"{msg}\n"
            
            # Get AI response
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a chess AI playing as Black. Always respond with just the move notation. Only make valid moves with pieces that exist on the board."},
                    {"role": "user", "content": context}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            ai_move = response.choices[0].message.content.strip()
            print(f"AI suggested move: {ai_move}")
            
            # Validate the move before returning
            if self._is_valid_move(ai_move, board):
                # Add to conversation history
                self.conversation_history.append(f"Human: {last_move} -> AI: {ai_move}")
                return ai_move
            else:
                print(f"AI suggested invalid move: {ai_move}, using fallback")
                fallback_move = self._get_fallback_move(board)
                self.conversation_history.append(f"Human: {last_move} -> AI: {fallback_move} (fallback)")
                return fallback_move
            
        except Exception as e:
            print(f"AI move generation failed: {e}")
            fallback_move = self._get_fallback_move(board)
            return fallback_move
    
    def _is_valid_move(self, move, board):
        """Check if the AI move is valid"""
        if not move or len(move) < 2:
            return False
        
        # Basic validation - check if the move format is reasonable
        move = move.strip().lower()
        
        # Handle castling
        if move in ['o-o', '0-0', 'oo', 'o-o-o', '0-0-0', 'ooo']:
            return True
        
        # Check if it's a reasonable chess move format
        files = 'abcdefgh'
        ranks = '12345678'
        
        # For pawn moves (e.g., 'e5')
        if len(move) == 2 and move[0] in files and move[1] in ranks:
            return True
        
        # For piece moves (e.g., 'Nf6', 'Bxe5')
        if len(move) >= 3:
            if move[0] in 'nbrqk' and move[1] in files and move[2] in ranks:
                return True
            if len(move) >= 4 and move[1] == 'x' and move[2] in files and move[3] in ranks:
                return True
        
        return False
    
    def _get_fallback_move(self, board):
        """Get a fallback move when AI fails"""
        # Find any black pawn that can move
        for row in range(1, 7):  # Check pawn rows
            for col in range(8):
                piece = board[row][col]
                if piece == '♟':  # Black pawn
                    if row < 7 and board[row + 1][col] is None:
                        # Convert to algebraic notation
                        files = 'abcdefgh'
                        ranks = '87654321'
                        to_square = f"{files[col]}{ranks[row + 1]}"
                        return to_square
        
        # If no pawn moves, try any black piece
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and self._get_piece_color(piece) == 'black':
                    # Try to move to an empty square
                    for new_row in range(8):
                        for new_col in range(8):
                            if board[new_row][new_col] is None:
                                files = 'abcdefgh'
                                ranks = '87654321'
                                to_square = f"{files[new_col]}{ranks[new_row]}"
                                return to_square
        
        return "e5"  # Ultimate fallback
    
    def _get_piece_color(self, piece):
        """Get the color of a chess piece"""
        if not piece:
            return None
        white_pieces = '♔♕♖♗♘♙'
        return 'white' if piece in white_pieces else 'black'
    
    def reset_conversation(self):
        """Reset conversation history for new game"""
        self.conversation_history = []

# Global AI instance
chess_ai = SimpleChessAI()
