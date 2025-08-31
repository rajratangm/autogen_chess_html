# Chess Game with AI Backend Integration

![Demo](asset/demo.gif)

This project integrates a chess game frontend with an AI-powered backend using AutoGen agents. The system provides a web-based chess interface that communicates with a Flask server running AI agents for intelligent gameplay.


## Features

- **Human vs AI Chess**: Play against an intelligent AutoGen AI opponent
- **Turn-based Gameplay**: You play as White, AI plays as Black with automatic responses
- **Interactive Chess Board**: Full-featured chess game with move validation
- **AI Backend**: Powered by AutoGen agents using OpenAI's GPT models
- **Real-time Communication**: Frontend-backend integration via REST API
- **Move History**: Track all moves and captured pieces
- **Game Controls**: New game, undo, and resign functionality
- **Connection Status**: Visual indicators for backend connectivity

## Project Structure

```
DSA_solver/
├── app.py                 # Flask web server with AI integration
├── team_example.py        # Original AutoGen chess agent example
├── team_exmaple.html      # Original HTML chess interface
├── templates/
│   └── chess_game.html    # Updated HTML with backend integration
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── venv/                 # Virtual environment
```

## Setup Instructions

### 1. Environment Setup

Make sure you have Python 3.8+ installed. Then set up the virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Key Configuration

Create a `.env` file in the project root with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Running the Application

Start the chess game using the startup script:

```bash
python start_game.py
```

Or start the Flask server directly:

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 4. Accessing the Game

Open your web browser and navigate to:
```
http://localhost:5000
```

## How It Works

### Frontend (HTML/JavaScript)
- **Chess Board**: Interactive 8x8 grid with piece movement
- **Move Validation**: Basic chess rules implementation
- **API Communication**: Sends moves to backend and receives AI responses
- **Game State Management**: Tracks board state, moves, and captures

### Backend (Flask + AutoGen)
- **Flask Server**: RESTful API endpoints for game operations
- **AutoGen Agents**: AI-powered chess assistant using OpenAI models
- **Game Logic**: Server-side move processing and AI response generation
- **State Management**: Maintains game state and history

### API Endpoints

- `POST /api/initialize` - Initialize a new game
- `POST /api/move` - Process a chess move
- `POST /api/ai-move` - Request AI move for current position
- `GET /api/game-state` - Get current game state

## Game Features

### Chess Rules Implementation
- **Piece Movement**: All standard chess piece movements
- **Capture Logic**: Proper piece capture and removal
- **Turn Management**: Alternating white/black turns
- **Game End Detection**: King capture detection

### AI Integration
- **Turn-based Play**: AI automatically responds after each human move
- **Strategic Analysis**: AI analyzes board position and makes intelligent moves
- **Context Awareness**: AI considers game history and current position
- **Standard Notation**: AI uses proper chess algebraic notation

### User Interface
- **Visual Feedback**: Selected pieces, possible moves, and last move highlighting
- **Move History**: Scrollable list of all moves made
- **Captured Pieces**: Display of pieces captured by each player
- **Connection Status**: Real-time backend connectivity indicator

## Usage

1. **Starting a Game**: Click "New Game" to begin
2. **Making Moves**: Click on a piece to select it, then click on a valid destination square
3. **AI Response**: The AI will automatically respond with its move after you make yours
4. **Game Controls**: Use Undo, Resign, or New Game buttons as needed
5. **Game Flow**: You play as White, AI plays as Black - take turns until checkmate or resignation

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Ensure Flask server is running (`python app.py`)
   - Check if port 5000 is available
   - Verify API key is set in `.env` file

2. **AI Not Responding**
   - Check OpenAI API key validity
   - Ensure internet connection for API calls
   - Check browser console for error messages

3. **Move Validation Issues**
   - Game runs in offline mode if backend is unavailable
   - Basic chess rules are implemented in frontend

### Debug Mode

The Flask server runs in debug mode by default. Check the terminal for detailed error messages and API request logs.

## Development

### Adding New Features

1. **Frontend**: Modify `templates/chess_game.html`
2. **Backend**: Update `app.py` with new API endpoints
3. **AI Logic**: Enhance AutoGen agent configuration in `app.py`

### Extending AI Capabilities

The AI system can be enhanced by:
- Adding more sophisticated chess engines
- Implementing opening book databases
- Adding position evaluation algorithms
- Supporting different AI difficulty levels

## Dependencies

- **Flask**: Web framework for backend API
- **Flask-CORS**: Cross-origin resource sharing support
- **AutoGen**: AI agent framework
- **OpenAI**: Language model integration
- **python-dotenv**: Environment variable management

## License

This project is for educational and demonstration purposes. Please ensure you comply with OpenAI's usage terms when using their API.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chess game integration.
