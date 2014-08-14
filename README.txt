zsearch

This is a stupid little tool I wrote because I screwed up in Git, and
needed to recover a file. Turns out in a lot of cases, the object will
still exist in .git/objects, but those files are zlib compressed. The
original program was:

$ cat ~/bin/zcat.py 
#!/usr/bin/env python

import re
import sys
import zlib

for arg in sys.argv[2:]:
    decompressed = zlib.decompress(open(arg).read())
    if re.search(sys.argv[1], decompressed):
        print decompressed

This is barely more than that, but it does a little better job with
error handling and parsing arguments. Presented in Go and Python.
