import chess
import chess.pgn
import numpy as np
import tensorflow as tf
import os
import random

def board_to_input(board):
    board_state = np.zeros(64, dtype=np.uint8)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            board_state[square] = piece.piece_type + (piece.color == chess.BLACK) * 6
    return board_state.reshape(8, 8, 1)

def move_to_output(move):
    return np.array([ord(move.uci()[0]) - ord('a'), int(move.uci()[1]) - 1])

def create_dataset_from_pgn(pgn_folder):
    dataset = []
    for filename in os.listdir(pgn_folder):
        if filename.endswith('.pgn'):
            pgn_file = os.path.join(pgn_folder, filename)
            with open(pgn_file, 'r') as f:
                while True:
                    game = chess.pgn.read_game(f)
                    if game is None:
                        break
                    board = game.board()
                    for move in game.mainline_moves():
                        input_data = board_to_input(board)
                        output_data = move_to_output(move)
                        dataset.append((input_data, output_data))
                        board.push(move)
    return dataset


model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(8, 8, 1), padding='same'),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(2, activation='linear')
])


model.compile(optimizer='adam', loss='mse')

dataset = create_dataset_from_pgn(r'C:\Users\monke\OneDrive\Desktop\projects\chessgames')

X = np.array([data[0] for data in dataset])
y = np.array([data[1] for data in dataset])

model.fit(X, y, epochs=1)

def play_game_with_ai(model):
    board = chess.Board()
    print("You are playing against the AI. You are White.")

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print(board)
            user_move = input("Enter your move (in UCI format, e.g., 'e2e4'): ")
            try:
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid move format. Try again.")
        else:
            input_data = board_to_input(board).reshape(1, 8, 8, 1)
            predicted_move = model.predict(input_data)
            legal_moves = list(board.legal_moves)
            predicted_move_uci = None

            for legal_move in legal_moves:
                move_uci = legal_move.uci()
                if (
                    ord(move_uci[0]) - ord("a") == int(predicted_move[0][0])
                    and int(move_uci[1]) - 1 == int(predicted_move[0][1])
                ):
                    predicted_move_uci = move_uci
                    break

            if predicted_move_uci is None:
                print("AI failed to generate a legal move. Taking a random legal move.")
                predicted_move_uci = random.choice(legal_moves).uci()

            board.push(chess.Move.from_uci(predicted_move_uci))
            print(f"AI moves: {predicted_move_uci}")

    print("Game Over")
    print("Result: " + board.result())

while True:
    play_again = input("Do you want to play a game against the AI? (yes/no): ")
    if play_again.lower() != "yes":
        break
    play_game_with_ai(model)

sample_board = chess.Board()
input_data = board_to_input(sample_board).reshape(1, 8, 8, 1)
predicted_move = model.predict(input_data)
print("Predicted Move:", predicted_move)
