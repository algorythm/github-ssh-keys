import sys
major = sys.version_info.major
minor = sys.version_info.minor

if major == 3 and minor >= 6:
    pass
else:
    print("This script only works on python 3.6 and up.")
    exit(-1)