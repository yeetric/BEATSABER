# read from file
with open("abcNotation.txt") as f:
    content = f.readlines()
abcNotation = str(content)
abcNotation = abcNotation.replace(" ", "")
score=[]
for note in abcNotation:
    score.append(note)
number = 1
print(f"{score[1]}.mp3")

