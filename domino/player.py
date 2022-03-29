


from typing import Union, Type
from exceptions import InvalidPlayerNumber, InvalidPlayer


_Movement = Type


class Person():
    pass 


class Annotator(Person):
    
    def __str__(self):
        return "Annotator"


class Player(Person):
    
    def __init__(self, number: int, name: str = None):
        self.__number = self.clean_number(number)
        self.__name = str(name or ("Player %s" % self.number))
        
    def __str__(self):
        return self.name
        
    @property
    def number(self) -> int:
        return self.__number
    
    @property
    def name(self) -> str:
        return self.__name 
        
    @classmethod
    def clean_number(cls, number: int) -> int:
        
        if not isinstance(number, int):
            raise InvalidPlayerNumber("The number must be of type integer.")
        
        if not number in (1, 2, 3, 4):
            raise InvalidPlayerNumber("The number is outside the range 1-4.")
        
        return number
    
    @classmethod
    def clean_player(cls, player: 'Player') -> 'Player':
        if not isinstance(player, (Player, Annotator)):
            raise InvalidPlayer("The player is not valid.")
        return player 
    
    def play(self, game) -> Union[_Movement, None]:
        pieces_and_side = game.get_player_pieces_for_current_play(self)
        
        if not pieces_and_side:
            return
        
        piece = max([e[0] for e in pieces_and_side])
        return game.play(player=self, piece=piece)
        

class Player1(Player):
    def __init__(self, name: str = None):
        super().__init__(1, name)
        

class Player2(Player):
    def __init__(self, name: str = None):
        super().__init__(2, name)
        

class Player3(Player):
    def __init__(self, name: str = None):
        super().__init__(3, name)
        

class Player4(Player):
    def __init__(self, name: str = None):
        super().__init__(4, name)


ANNOTATOR = Annotator()
PLAYER1 = Player1()
PLAYER2 = Player2()
PLAYER3 = Player3()
PLAYER4 = Player4()

ALL_PLAYERS = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]