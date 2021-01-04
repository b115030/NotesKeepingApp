class NotesError(Exception):
    """[summary]
        Custom exception.
    Args:
        Exception ([Class]): [Exception]
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message