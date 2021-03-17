# QMUL_Cloud-Computing-Mini-Project

Description to be added
New line from local2

from flask import Flask, jsonify

all_tvshows = [
	{
		"name" : "List1", 
	 	"shows" : [
	 	  	{
	 	  		"title":"Friends",
		   		"movie":[
		   			{"title":"Friends","length":"30:00"},,
				],
				"description":"""\n\Friends is an American television sitcom, created by David Crane and Marta Kauffman,
                which aired on NBC from September 22, 1994, to May 6, 2004, lasting ten seasons. With an ensemble
                cast starring Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry and David Schwimmer,
                the show revolves around six friends in their 20s and 30s who live in Manhattan, New York City.\n      """
			},

	 	  	{
	 	  		"title":"Big Bang Theory",
		   		"movie":[
		   			{"title":"Big Bang Theory","length":"25:00"},
				],
				"description":"""\n\The Big Bang Theory is a comedy series about four young scientists who know all
                about the world of physics, and one girl, who gives the physics world a real spin.\n      """
			},
            
	 	  	{
	 	  		"title":"Game of Thrones",
		   		"movie":[
		   			{"title":"Game of Thrones","length":"25:00"},
				],
				"description":"""\n\Game of Thrones is an American fantasy drama television series created by David
                Benioff and D. B. Weiss for HBO. It is an adaptation of A Song of Ice and Fire, a series of fantasy novels
                by George R. R. Martin, the first of which is A Game of Thrones. The show was shot in the United Kingdom,
                Canada,Croatia, Iceland, Malta, Morocco, and Spain. It premiered on HBO in the United States on April.\n      """
			},
                                    
			{

			}
		]
	},
	
	{
		"name" : "List2", 
	 	"shows" : [
	 	  	{
	 	  		"title":"Breaking Bad",
		   		"show":[
		   			{"title":"Breaking Bad","length":"30:00"},,
				],
				"description":"""\n\Friends is an American television sitcom, created by David Crane and Marta Kauffman,
                which aired on NBC from September 22, 1994, to May 6, 2004, lasting ten seasons. With an ensemble
                cast starring Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry and David Schwimmer,
                the show revolves around six friends in their 20s and 30s who live in Manhattan, New York City.\n      """
			},

	 	  	{
	 	  		"title":"Game of Thrones",
		   		"movie":[
		   			{"title":"Game of Thrones","length":"25:00"},
				],
				"description":"""\n\Game of Thrones is an American fantasy drama television series created by David
                Benioff and D. B. Weiss for HBO. It is an adaptation of A Song of Ice and Fire, a series of fantasy novels
                by George R. R. Martin, the first of which is A Game of Thrones. The show was shot in the United Kingdom,
                Canada,Croatia, Iceland, Malta, Morocco, and Spain. It premiered on HBO in the United States on April.\n      """
			},
            
			{

			}
		]
	},
	
	{            
		"name" : "List3", 
	 	"shows" : [
	 	  	{
	 	  		"title":"Friends",
		   		"movie":[
		   			{"title":"Friends","length":"30:00"},,
				],
				"description":"""\n\Friends is an American television sitcom, created by David Crane and Marta Kauffman,
                which aired on NBC from September 22, 1994, to May 6, 2004, lasting ten seasons. With an ensemble
                cast starring Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matt LeBlanc, Matthew Perry and David Schwimmer,
                the show revolves around six friends in their 20s and 30s who live in Manhattan, New York City.\n      """
			},

	 	  	{

	 	  		"title":"Queen's Gambit",
		   		"movie":[
		   			{"title":"Queen's Gambit","length":"40:00"},
				],
				"description":"""\n\The Queen's Gambit is a 2020 American coming-of-age period drama miniseries based 
                on Walter Tevis 's 1983 novel of the same name. The title refers to " Queen's Gambit ", a chess opening. 
                It was written and directed by Scott Frank, who created it with Allan Scott.\n      """            
			}
                
	 	  		"title":"Better Call Saul",
		   		"movie":[
		   			{"title":"Better Call Saul","length":"25:00"},
				],
				"description":"""\n\Better Call Saul is an American crime drama television series created by Vince
                Gilligan and Peter Gould. It is both a spin-off and a prequel of Gilligan's previous series, Breaking Bad .
                Set in the early to mid-2000s in Albuquerque, New Mexico , the series develops Jimmy McGill,
                an earnest lawyer and former con-man, into a greedy criminal defense attorney known as Saul Goodman .\n      """            
			}
		]
	}
]


app = Flask(__name__)

@app.route('/tvshows', method=['GET'])
def get_all_tvshows_by_tv(tvname):
    albums = [tvtitle['shows'] for tvtitle in all_tvshows if tv['name'] == tvname]
    if len(show)==0:
    return jsonify({'error':'tv name not found!'}), 404
  else:
    response = [shows[title] for show in shows[0]]
    return jsonify(response), 200

@app.route('/tvshows/<tvname>/<showtitle>'), method=['GET'])
def get_show_by_tv_and_show(tvname, showtitle):
    shows = [tv['shows'] for tv in all_tvshows if tv['name'] == tvname]
    if len(shows)==0:
        return jsonify({'error':'tv name not found!'}), 404
    else:
        movie = [show['movie'] for show in shows[0] if shows['title'] == showtitle]
        if len(movie)==0:
            return jsonify({'error':'show title not found!'}), 400
        else:
            return jsonify(movie[0]), 200
        
        
if __name__ == '__main__':
            app.run(host='0,0,0,0')
