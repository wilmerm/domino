


class DominoError(Exception):
    """Domino base error."""


class InvalidTable(DominoError):
    """When table is not valid."""


class InvalidPlayer(DominoError):
    """When player is not valid."""
    

class InvalidPlayerNumber(DominoError):
    """When trying to set an invalid player number."""
    

class InvalidPiece(DominoError):
    """When the piece is not valid."""
        

class PieceIsPlayed(DominoError):
    """When piece is played, not available for new movement."""


class InvalidPieceNumber(DominoError):
    """When trying to set invalid piece number."""
    

class InvalidSide(DominoError):
    """When trying to set invalid side movement."""
    
