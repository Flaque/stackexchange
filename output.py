import sys

def update(text):
    sys.stdout.write('\r' + text)
    sys.stdout.flush()
