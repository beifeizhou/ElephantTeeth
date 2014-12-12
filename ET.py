#This script is used to calculate the relationship between the stockfish score and the elo rating

import re

#define class of each game
class GAME():
	def __init__(self, number):
		self.Number = number
		self.Stockfish = ''
		self.moves = []
		self.WhiteElo = 0
		self.BlackElo = 0
		self.Result = ''

#Read the stockfish file and elo file, assgin all the games as class:
def stockfish(stockfish_file, elo_file):
	games = []
	input1 = open(stockfish_file)
	i = -1
	for line in input1.readlines():
		line_split = line.split(',')
		try:
			int(line_split[0])
		except ValueError:
			pass
		else:
			i = i+1
			games.append(GAME(int(line_split[0])))
			games[i].Stockfish = line_split[1]

	re_WhiteElo = re.compile('\[WhiteElo\s+"(\d+)"\]')
	re_BlackElo = re.compile('\[BlackElo\s+"(\d+)"\]')
	re_Result = re.compile('\[Result\s+"(.+)"\]')

	i = -1
	l_index = -1
	input2 = open(elo_file)
	lines = input2.readlines()
	
	while l_index < (len(lines)-3):
		l_index = l_index + 1
		if re_Result.search(lines[l_index]):
			i = i + 1
			games[i].Result = re_Result.findall(lines[l_index])[0]
			if re_WhiteElo.search(lines[l_index+1]):
				games[i].WhiteElo = re_WhiteElo.findall(lines[l_index+1])[0]
				games[i].BlackElo = re_BlackElo.findall(lines[l_index+2])[0]
				games[i].moves = lines[l_index+4].strip()
				l_index = l_index + 5
			else:
				games[i].moves = lines[l_index+2].strip()
				l_index = l_index + 1
	return games


#################Run the function###################
all_games = stockfish('stockfish.csv','data_uci.pgn')

################Plot###############################
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('multipage_pdf.pdf')
games_f = []
for game in all_games:
	if 'NA' not in game.Stockfish:
		games_f.append(game)
		if int(game.WhiteElo) > 2700 and int(game.BlackElo) > 2700:
			stockfish = map(int, game.Stockfish.split())
			plt.figure(figsize=(3, 2)) #figure size
			plt.plot(stockfish)
			plt.title(str(game.Number)+'_'+game.WhiteElo+'_'+game.BlackElo)
			plt.savefig(pp,bbox_inches='tight',format='pdf')  #set margin
pp.close()
