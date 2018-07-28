import sys
major = sys.version_info.major
minor = sys.version_info.minor

def is_unsupported_python():
    return major == 3 and minor >= 6

# if major == 3 and minor >= 6:
#     pass
# else:
#     print("This script only works on python 3.6 and up.")
#     sys.exit(-1)