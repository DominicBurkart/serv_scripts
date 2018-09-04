import sys
import shutil
import time
import os

indir = sys.argv[1]
outdir = sys.argv[2]

forty_eight = 48 * 60 * 60

print("Movestreams started. Copying files that haven't been edited for at least 48 hours.")

found = False
for root, dirs, files in os.walk(indir):
    for f in files:
        old = os.path.join(root, f)
        if time.time() - os.path.getmtime(old) > forty_eight:
            print("Moving file: " + str(old))
            shutil.move(old, os.path.join(outdir, f))
            found = True

if not found:
    print("No files to copy found.")

print("Movestreams complete.")