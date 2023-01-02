from tkinter import messagebox


class ErreurClicCoup(Exception):
    '''
    Une exception indiquant qu'un clic a eu lieu sur un coup déjà joué.
    '''
    pass
