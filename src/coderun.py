import sys
from io import StringIO
import pdb

def runCode(codeblock):
    df = None
    fig = None
    plt = None
    exec_globals = {'df':df, 'fig':fig, 'plt':plt}
    exec(codeblock, exec_globals)

    return exec_globals
