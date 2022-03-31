
from .exceptions import InvalidTable, InvalidSide


class Table():
    
    # Lados de la fila jugada en la tabla.
    A = 0
    B = -1
    
    def __init__(self):
        pass 
    
    def __str__(self):
        return "Table"
    
    @classmethod
    def clean_table(cls, table: 'Table') -> 'Table':
        if not isinstance(table, Table):
            raise InvalidTable("The table is not valid.")
        
        return table 
    
    @classmethod
    def clean_side(cls, side: int) -> int:
        if not isinstance(side, int):
            raise InvalidSide("The must be integer type")
        
        if not side in (Table.A, Table.B):
            raise InvalidSide("The side must be %d or %d." % Table.A, Table.B)
        
        return side
    