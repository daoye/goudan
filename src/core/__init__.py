import os



def PATH():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def FILE(file):
    return os.path.join(PATH(), file)