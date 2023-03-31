
import re
def extract_move(response):
        #print("resonse", response)
        #something wents wrong when trying to extract move from
        #i shouldnt use regex if i dont understand it 
        move_pattern = re.compile(r'[BRQNK][a-h][1-8]|[BRQNK][a-h]x[a-h][1-8]|[BRQNK][a-h][1-8]x[a-h][1-8]|[BRQNK][a-h][1-8][a-h][1-8]|[BRQNK][a-h][a-h][1-8]|[BRQNK]x[a-h][1-8]|[a-h]x[a-h][1-8]=(B+R+Q+N)|[a-h]x[a-h][1-8]|[a-h][1-8]x[a-h][1-8]=(B+R+Q+N)|[a-h][1-8]x[a-h][1-8]|[a-h][1-8][a-h][1-8]=(B+R+Q+N)|[a-h][1-8][a-h][1-8]|[a-h][1-8]=(B+R+Q+N)|[a-h][1-8]|[BRQNK][1-8]x[a-h][1-8]|[BRQNK][1-8][a-h][1-8]')
        match = move_pattern.search(response)
        if match:
            return match.group(1)
        else:
            return "It was not possible to extract a move from the response"
        



'''
...1...e5
1...e5
 Nc6
 e5
i can take Best move: ...Nc6

- take stuff behind: 
- remove all points ...
- remove all 1  
'''
def extract(response):
    response = response.split("Best move:")[1]
    response = response.replace("...","")
    response = response.replace("1.","")
    response = response.replace(".","")
    response = response.replace(" ","")
    return response

sample_response = "resonse PGN of game so far: \n\n1. e4 e5\n\n2. Nf3\n\nBest move: Nc6"

print(extract(sample_response))