
import sys
import random

from domino.game import Game
from domino.player import PLAYER1, PLAYER2


def main(*args):

    player1 = PLAYER1
    player2 = PLAYER2
    
    game = Game.create(player1, player2)
    print(game)
    
    print(player1, game.get_player_pieces(player1))
    print(player2, game.get_player_pieces(player2))
    print("availables pieces:", game.get_availables_pieces())
    
    for n in range(100):
        # Player1 
        pieces_and_side = game.get_player_pieces_for_current_play(player1)
        
        if pieces_and_side:
            piece = max([item[0] for item in pieces_and_side])
            print(game.play(player1, piece, None))
        
        # Player2
        pieces_and_side = game.get_player_pieces_for_current_play(player2)
        
        if pieces_and_side:
            piece = max([item[0] for item in pieces_and_side])
            print(game.play(player2, piece, None))
    
    
    for e in game.record.build_row():
        print(e)
    
    
    return 0


if __name__ == "__main__":
    main(sys.argv)