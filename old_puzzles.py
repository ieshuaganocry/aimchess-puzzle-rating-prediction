import predictor
from chess.pgn import Game, GameNode
import chess.engine
import pymongo

mongo = pymongo.MongoClient()
db = mongo['lichess']
puzzle_coll = db['puzzle_rnn']

for doc in puzzle_coll.find({"rating":{"$exists":False}}):
    board = chess.Board(doc["fen"])
    node: GameNode = Game.from_board(board)
    for uci in doc["moves"]:
        move = chess.Move.from_uci(uci)
        node = node.add_main_variation(move)
    init = node.game().next()
    assert init;
    fen = init.board().fen()
    solution = [move.san() for move in init.mainline()]
    print(f'{doc["_id"]} {len(solution)} {solution}')
    try:
        puzzle_rating = int(predictor.predict_rating(fen, solution))
        puzzle_coll.update_one({"_id":doc["_id"]},{"$set":{"rating": puzzle_rating}})
    except Exception as err:
        print(err)
