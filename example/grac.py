
import sys
sys.path.insert(0,"../")
from grammar import gracgrammar
gracParser = gracgrammar.getParser()

gracCode = ""

#Por si el usuario para la data como un file 
if len(sys.argv) > 1:
    try:
        f = open(sys.argv[1], 'r')
        gracCode = f.read()
    except:
        sys.exit("Invalid path or file is corrupt.")
gracParser.parse(gracCode)       

    