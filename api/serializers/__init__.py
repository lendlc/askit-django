import os

FILE_LOC = os.path.dirname(os.path.abspath(__file__))
MODULE_NAME = FILE_LOC.split("/")[-2:]

# Dynamically import all python files in api.serializers
for filename in sorted(os.listdir(FILE_LOC)):
    if filename.endswith(".py") and filename != "__init__.py":
        filename = filename[:filename.index(".py")]
        # module =  "." + filename
        module = "." + filename
        try:
            exec("from " + module + " import *")
        except ImportError as e:
            import sys
            error_msg = "Failed to import %s. %s" % (filename, e)
            sys.stderr.write("\x1b[1;31m" + error_msg + "\x1b[0m \n")
