# llmchess

Now finishing the project today.  

My engine is inside engine.py. I want to send each move to the engine. if the move is the first move i want to return "first move". What do i need to implement in my engine.py for that and what do i habve to add in my app.py?

stephen wolfram has great ambition for his age. respect.


can i use lichess as an wrapper somehow? fuck that i will do it from scratch with python. here the idea is to

- [x] make only legal moves possible
- [x] fix rochade
- [x] send each move to server and log first
- [x] detect if a move was the first move or not.
- [x] if move was first move send request to openai 
- [x] add to prompt the value of the first move 
- [x] create a field for pasting the api key
- [x] choose model options
    - [x] add gpt turbo 
    - [x] add gpt-4
- [x] add start button
- [x] add functionality that game is only starting if start button was clicked 
- [x] on click of start insert api key from input field and also model
    - [x] fix bug of that key gets not inserted correctly 
    - [x] if that works turn start to stop and it should be possible to start the game
- [x] add field for logs
- [x] add model responses in respective colors
- [x] display waiting in log 
- [x] set model according to selected model 
- [x] check not only if key perse is working but make request with selcted model
- [x] add the second move to the board --> generally fix problem that moves are not logged sometimes
- [x] fix problem that if first move is wrong
- [x] make content not overflowing
- [x] check if checkmate is working --> checkmate, stalemate, draw
- [ ] put it online
    - [ ] make sessions working  
    - [ ] make it with a log file working instead of sockets


- [ ] make on click of end button working - to reset all values if this button was clicked (test that in production setting)
- [ ] add link to my twitter
- [ ] add analytics to site  

need to think about the design of the game so that it makes sense. 


next i want to extend the game to next moves.

this is going to be legendary. so much fun. i started becoming a pretty fast typer. 

i make a move 


now chess engine. after each move i need to send fen string to server. 

ich zug --> fen string server --> engine --> mit prompt und game state to gpt --> check if move possible in engine --> move back to js 


What are the next steps??? what can i do now.. what can i dooooo now. i have no plan. i should start with the engine because thatgw



- [ ] analytics!! to see how often the game was played. also save the played games?
- [ ] outreach
    - [ ] lesswrong
    - [ ] reddit  
    - [ ] ynews
    - [ ] twitter 
    - [ ] discord 
    - [ ] freedom slack (before fix bot)
    - [ ] slack channel agi house 
    - [ ] visit show and tell event and present my idea
    - [ ] share with alex mamuleanu
    - [ ] share with berlin chess channel


## Notes

For the mvp user can only insert open ai keys. and there is one basic prompt (that one from from less wrong) in the future the plan is to add more features like adding other language models and also choosing between to benchmark what works better. People can contribute via simple pull request.

I want to create a online chessgame which other people can use for playing chess against and engine. the engine is a simple python script i have. how can i do create such a game for the public?

I make a move and than i send this move to the engine. after that 



i a