import json
from statistics import median
import predictor

# Teach count_moves model
f = open('learn.json')
learn_puzzles = json.load(f)
per_moves_count = {}
for p in learn_puzzles:
    moves = p["solution"]
    rating = p["rating"]
    moves_count = len(moves)

    if moves_count not in per_moves_count:
        per_moves_count[moves_count] = {"total": 0, "ratings":[]}

    per_moves_count[moves_count]["total"] += 1
    per_moves_count[moves_count]["ratings"].append(int(rating))

for moves_count in per_moves_count:
    per_moves_count[moves_count]["median_rating"] = median(per_moves_count[moves_count]["ratings"])
#------------------------------------

def method1(fen, solution):
    return 1500

def method2(fen, solution):
    moves_count = len(solution)
    return per_moves_count[moves_count]["median_rating"]

def method3(fen, solution):
    return int(predictor.predict_rating(fen, solution))


#TODO: Specify the number pf puzzles you want to test from the file test.json
f = open('test.json')
puzzles = json.load(f)[0:10]

headers = ["fen", "solution", "rating", "m1 rating", "m1 error", "m2 rating", "m2 error", "m3 rating", "m3 error"]
csv = "{}\n".format("\t".join(headers))
for i in range(len(puzzles)):
    puzzle = puzzles[i]
    fen = puzzle["fen"]
    solution = puzzle["solution"]
    rating = puzzle["rating"]
    m1 = method1(fen, solution)
    m1_error = abs(rating - m1)
    m2 = method2(fen, solution)
    m2_error = abs(rating - m2)
    m3 = method3(fen, solution)
    m3_error = abs(rating - m3)
    values = [fen, " ".join(solution), rating, m1, m1_error, m2, m2_error, m3, m3_error]
    values = [str(value) for value in values]
    csv += "{}\n".format("\t".join(values))

file = open('output.csv', 'w')
file.write(csv)
file.close()

print("DONE")
