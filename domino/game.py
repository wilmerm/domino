

import random
from typing import List, Tuple

from domino import Domino
from table import Table
from piece import Piece, ALL_PIECES
from player import ANNOTATOR, Player, ALL_PLAYERS
from record import GameRecord, Movement
from exceptions import InvalidPiece


class Game(Domino):
    
    def __init__(self, table: Table, pieces: List[Piece], players: List[Player]):
        self.__table = Table.clean_table(table)
        self.__pieces: List[Piece] = [Piece.clean_piece(piece) for piece in pieces]
        self.__pieces_index = {p.tuple():p for p in self.__pieces}
        self.__players = [Player.clean_player(player) for player in players]
        self.__record: GameRecord = GameRecord()
        self.__id = id(self)
        
    def __str__(self):
        return "Game(%s)" % self.__id
    
    @property
    def table(self) -> Table:
        return self.__table 
    
    @property
    def pieces(self) -> List[Piece]:
        return self.__pieces
    
    @property
    def players(self) -> List[Player]:
        return self.__players
    
    @property
    def record(self) -> GameRecord:
        return self.__record

    def get_availables_pieces(self) -> List[Piece]:
        table_pieces = []
        
        for piece_tuple in self.record.pieces_possession:
            if isinstance(self.record.pieces_possession[piece_tuple], Table):
                piece = self.get_piece_from_value(piece_tuple)
                table_pieces.append(piece)
        
        return table_pieces
    
    def get_available_random_piece(self) -> Piece:
        availables = list(self.get_availables_pieces())
        random.shuffle(availables)
        return availables[0]
                   
    def get_piece_from_value(self, value: Tuple) -> Piece:
        return self.__pieces_index[value]
            
    def get_player_pieces(self, player: Player) -> List[Piece]:
        """Obtiene las fichas del jugador."""
        player_pieces = []
        
        for piece_tuple in self.record.pieces_possession:
            if player == self.record.pieces_possession[piece_tuple]:
                piece = self.get_piece_from_value(piece_tuple)
                player_pieces.append(piece)
        
        return player_pieces
    
    def get_player_pieces_for_current_play(self, 
                                    player: Player) -> List[Tuple[Piece, int]]:
        """Obtiene las fichas del jugador, que se puedan jugar actualmente."""
        player_pieces_and_side = []
        
        for piece in self.get_player_pieces(player):
            try:
                side = self.get_correct_side_for_piece(piece)
            except (InvalidPiece):
                continue
            
            player_pieces_and_side.append((piece, side))
        
        return player_pieces_and_side
    
    def play(self, player: Player, piece: Piece, side: int = None) -> Movement:
        
        piece = Piece.clean_piece(piece)
        
        player_pieces = self.get_player_pieces(player)
        
        if not piece in player_pieces:
            raise InvalidPiece("The %s is not %s's" % (piece, player))
        
        if not side:
            side = self.get_correct_side_for_piece(piece)
        
        return self.record.move(piece=piece, _from=player, to=self.table, side=side)
    
    def get_correct_side_for_piece(self, piece: Piece) -> int:
        """Obtiene el side correcto en la que se puede poner la ficha."""
        row = self.record.build_row()
        
        if row:
            a, b = row[0][0], row[-1][0]
        else:
            return Table.A
        
        if a in piece: return Table.A
        if b in piece: return Table.B
        
        raise InvalidPiece("The piece %s is not valid for either side %s or %s" 
                                                                % (piece, a, b))
                
    @classmethod
    def create(cls, *players: Player) -> 'Game':
        
        if not players:
            players = ALL_PLAYERS 
            
        pieces = ALL_PIECES
        random.shuffle(pieces)
        
        game = Game(
            table=Table(),
            pieces=pieces,
            players=players
        )
        
        # Inicialmente todas las piezas están en la mesa.
        for i in range(28):
            piece = pieces[i]
            game.record.move(piece, ANNOTATOR, game.table, None)
        
        i = 0
        for player in game.players:
            for n in range(7):
                piece = pieces[i]
                game.record.move(piece, game.table, player, None)
                i += 1
                
        return game

    
    
    