



from typing import List, Tuple

from exceptions import InvalidPieceNumber, InvalidPiece


class Piece:
    
    PIECES = (
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
        (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
        (3, 3), (3, 4), (3, 5), (3, 6),
        (4, 4), (4, 5), (4, 6),
        (5, 5), (5, 6),
        (6, 6),
    )
    
    def __init__(self, a: int, b: int):    
        self.__a = self.clean_number(a)
        self.__b = self.clean_number(b)
            
    def __str__(self):
        return "%d:%d" % self.tuple()
    
    def __repr__(self):
        return "Ficha(%s)" % str(self)
    
    def __iter__(self):
        yield self.__a 
        yield self.__b
    
    def __eq__(self, other: 'Piece') -> bool:
        # Se comparán los valores (no el objeto).
        # Para comparar el objeto use 'is', example: piece1 is piece2
        return sum(other) == sum(self)
    
    def __lt__(self, other: 'Piece') -> bool:
        return sum(other) > sum(self)
    
    def __gt__(self, other: 'Piece') -> bool:
        return sum(other) < sum(self)
    
    @property
    def a(self) -> int:
        return self.__a 
    
    @property
    def b(self) -> int:
        return self.__b
    
    def tuple(self) -> Tuple:
        return (self.__a, self.__b)
    
    @classmethod
    def clean_number(cls, number: int) -> int:
        if not isinstance(number, int):
            raise InvalidPieceNumber("The number must be of type integer.")
        
        if not number in (0, 1, 2, 3, 4, 5, 6):
            raise InvalidPieceNumber("The number is outside the range 0-6.")
        
        return number
    
    @classmethod
    def clean_piece(cls, piece: 'Piece') -> 'Piece':
        if not isinstance(piece, Piece):
            raise InvalidPiece("The piece type '%s' is not valid." % str(piece))
        return piece

    
class Piece00(Piece):
    def __init__(self):
        super().__init__(0, 0)
        

class Piece01(Piece):
    def __init__(self):
        super().__init__(0, 1)


class Piece02(Piece):
    def __init__(self):
        super().__init__(0, 2)


class Piece03(Piece):
    def __init__(self):
        super().__init__(0, 3)


class Piece04(Piece):
    def __init__(self):
        super().__init__(0, 4)


class Piece05(Piece):
    def __init__(self):
        super().__init__(0, 5)


class Piece06(Piece):
    def __init__(self):
        super().__init__(0, 6)


class Piece11(Piece):
    def __init__(self):
        super().__init__(1, 1)


class Piece12(Piece):
    def __init__(self):
        super().__init__(1, 2)


class Piece13(Piece):
    def __init__(self):
        super().__init__(1, 3)
        

class Piece14(Piece):
    def __init__(self):
        super().__init__(1, 4)
        

class Piece15(Piece):
    def __init__(self):
        super().__init__(1, 5)
        

class Piece16(Piece):
    def __init__(self):
        super().__init__(1, 6)
        

class Piece22(Piece):
    def __init__(self):
        super().__init__(2, 2)


class Piece23(Piece):
    def __init__(self):
        super().__init__(2, 3)


class Piece24(Piece):
    def __init__(self):
        super().__init__(2, 4)


class Piece25(Piece):
    def __init__(self):
        super().__init__(2, 5)


class Piece26(Piece):
    def __init__(self):
        super().__init__(2, 6)


class Piece33(Piece):
    def __init__(self):
        super().__init__(3, 3)


class Piece34(Piece):
    def __init__(self):
        super().__init__(3, 4)


class Piece35(Piece):
    def __init__(self):
        super().__init__(3, 5)
        

class Piece36(Piece):
    def __init__(self):
        super().__init__(3, 6)


class Piece44(Piece):
    def __init__(self):
        super().__init__(4, 4)
   

class Piece45(Piece):
    def __init__(self):
        super().__init__(4, 5)
   
   
class Piece46(Piece):
    def __init__(self):
        super().__init__(4, 6)
   
   
class Piece55(Piece):
    def __init__(self):
        super().__init__(5, 5)
   

class Piece56(Piece):
    def __init__(self):
        super().__init__(5, 6)
   

class Piece66(Piece):
    def __init__(self):
        super().__init__(6, 6)
        
        
ALL_PIECES: List[Piece] = [
    Piece00(), Piece01(), Piece02(), Piece03(), Piece04(), Piece05(), Piece06(),
    Piece11(), Piece12(), Piece13(), Piece14(), Piece15(), Piece16(),
    Piece22(), Piece23(), Piece24(), Piece25(), Piece26(),
    Piece33(), Piece34(), Piece35(), Piece36(),
    Piece44(), Piece45(), Piece46(),
    Piece55(), Piece56(),
    Piece66(),
]