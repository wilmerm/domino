



from typing import Tuple, Union, List, Dict
from exceptions import DominoError, InvalidPiece, InvalidSide
from piece import Piece
from player import ANNOTATOR, Player
from table import Table
from domino import Domino


class Movement(Domino):
    
    def __init__(self, piece: Piece, _from: Union[Player, Table], 
                 to: Union[Player, Table], side: int):
        
        if _from == to:
            raise DominoError("Los parámetros _from y to deben ser distintos.")
        
        self.__piece = Piece.clean_piece(piece)
        self.__from = Player.clean_player(_from) if not isinstance(_from, Table) else _from
        self.__to = Player.clean_player(to) if not isinstance(to, Table) else to
        self.__side = Table.clean_side(side) if side is not None else None
        
    def __str__(self):
        if self.side is None:
            return "%s move %s to %s" % (self._from, self.piece, self.to)
        return "%s move %s to %s in side %s" % (self._from, self.piece, self.to, self.side)
        
    def __repr__(self):
        return "Movement(%s)" % self

    @property
    def _from(self) -> Player:
        return self.__from

    @property
    def to(self) -> Union[Player, Table]:
        return self.__to

    @property
    def piece(self) -> Piece:
        return self.__piece
    
    @property
    def side(self) -> int:
        return self.__side


class GameRecord(Domino):
    
    def __init__(self):
        self.__movements: List[Movement] = []
        # Movimientos agrupados por jugador.
        self.__players_movements: Dict[Player, Movement] = {}
        # Movimientos agrupados por ficha.
        self.__pieces_movements: Dict[Piece, Movement] = {}
        
        # Lleva el control de la poseción actual de la ficha.
        self.__pieces_possession: Dict[Piece, Union[Player, Table, None]] = {}

    def __str__(self):
        return str(self.__movements)
        
    def __iter__(self):
        for movement in self.__movements:
            yield movement 
            
    def __len__(self):
        return len(self.__movements)
    
    @property
    def players_movements(self) -> Dict[Player, Movement]:
        return self.__players_movements
    
    @property
    def pieces_movements(self) -> Dict[Piece, Movement]:
        return self.__pieces_movements

    @property
    def pieces_possession(self) -> Dict[Piece, Union[Player, Table, None]]:
        return self.__pieces_possession
    
    @property
    def a(self) -> Tuple[int, Movement]:
        return self.build_row()[0]
    
    @property
    def b(self) -> Tuple[int, Movement]:
        return self.build_row()[-1]
    
    def get_row_pieces_values_in_correct_alignament(self) -> List[Tuple[int, int]]:
        row = self.build_row()
        out: List[Tuple[int, int]] = []
        pieces_included: List[Piece] = []
        
        n = 1
        for number, movement in row:
            
            # ESto pasa porque build_row contine (a propósito) movimientos 
            # repetidos
            if movement.piece in pieces_included:
                continue
            
            a, b = movement.piece.tuple()
            
            if not out:
                value = (a, b)
                out.append({"turn": n, "value": value, "movement": movement})
                pieces_included.append(movement.piece)
            
            # Si se jugó por el lado izquierdo (A).
            elif movement.side == Table.A:
                if movement.piece.a == number:
                    value = (b, a)
                elif movement.piece.b == number:
                    value = (a, b)
                else:
                    raise InvalidPiece("The piece %s is not valid in movement %s" % 
                                       (movement.piece, movement))
                    
                out.insert(0, {"turn": n, "value": value, "movement": movement})
                pieces_included.append(movement.piece)
            
            # Si se jugó por el lado derecho (B).
            elif movement.side == Table.B:
                if movement.piece.a == number:
                    value = (b, a)
                elif movement.piece.b == number:
                    value = (a, b)
                else:
                    raise InvalidPiece("The piece %s is not valid in movement %s" % 
                                       (movement.piece, movement))

                out.append({"turn": n, "value": value, "movement": movement})
                pieces_included.append(movement.piece)
                
            else:
                raise InvalidSide("The side %s is not valid in movement %s" 
                                  % (movement.side, movement))


            print(n, movement.side, value, movement.piece)
            n += 1
            
        return out
    
    def build_row(self, movement_add: Movement = None) -> List[Tuple[int, Movement]]:
        """Obtiene un listado de números enteros que representan el estado del 
        juego actual.

        Args:
            movement_add (Movement, optional): Si se indica, será agregado al 
            registro como un movimiento más. Defaults to None.

        Raises:
            InvalidPiece: Si se encuentra una pieza que no encaja en el registro.
            InvalidSide: Si se encuentra una pieza válida, pero en el lado incorrecto.

        Returns:
            List[int]: Una lista de enteros.
        """
        row: List[Tuple[int, Movement]] = []
        movements = list(self) + [movement_add] if movement_add else list(self)
        
        for movement in movements:
            
            # Si quien pone la ficha es el anotador, no se contabiliza.
            # El anotador es utilizado para repartir las fichas a los jugadores,
            # y para ponerlas en la mesa inicialmente.
            if movement._from is ANNOTATOR:
                continue 
            
            if movement and isinstance(movement.to, Table):
                a, b = movement.piece.tuple()
                
                if not row:
                    row.append((a, movement))
                    row.append((b, movement))
                
                elif movement.side == Table.A:
                    row_side = row[0][0]
                    if row_side == a:
                        row.insert(0, (b, movement))
                    elif row_side == b:
                        row.insert(0, (a, movement))
                    else:
                        raise InvalidPiece("The piece %s is no valid for side "
                        "A. Piece number must be %d" % (movement.piece, row[0][0]))
                        
                elif movement.side == Table.B:
                    row_side = row[-1][0]
                    if row_side == a:
                        row.append((b, movement))
                    elif row_side == b:
                        row.append((a, movement))
                    else:
                        raise InvalidPiece("The piece %s is no valid for side "
                        "B. Piece number must be %d" % (movement.piece, row_side))
                else:
                    raise InvalidSide("The side %s is not valid" % movement.side)
        
        if movement_add:
            self.__movements.append(movement_add)
        
        return row
            
    def is_piece_played(self, piece: Piece) -> bool:
        for movement in self:
            if (movement.piece is piece) and (isinstance(movement.to, Table)):
                return True
        return False

    def move(self, piece: Piece, _from: Union[Player, Table], 
             to: Union[Player, Table], side: int) -> Movement:            
        
        mov = Movement(piece, _from, to, side)
        
        # Valida que la ficha vaya por el lado especificado.
        # Lanzará un InvalidSide exception si la ficha no va.
        # Se agregará al record si la ficha es correcta.
        self.build_row(mov) 
        
        # Indexamos los datos.
        try:
            self.__players_movements[_from].append(mov)
        except (KeyError):
            self.__players_movements[_from] = [mov]
            
        try:
            self.__players_movements[to].append(mov)
        except (KeyError):
            self.__players_movements[to] = [mov]
            
        try:
            self.__pieces_movements[piece.tuple()].append(mov)
        except (KeyError):
            self.__pieces_movements[piece.tuple()] = [mov]
            
        self.__pieces_possession[piece.tuple()] = to
        
        return mov
    