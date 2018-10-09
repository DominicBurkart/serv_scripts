import os
import subprocess
import sys
import time

indir = sys.argv[1]
outdir = sys.argv[2]

TIME = 25 * 60 * 60

print("Movestreams started. Copying files that were last updated more than " + str(TIME) + " seconds (" +
      str(float(TIME) / (24 * 60 * 60)) + " days) ago.")

found = False
for root, dirs, files in os.walk(indir):
    for f in files:
        old = os.path.join(root, f)
        if time.time() - os.path.getmtime(old) > TIME:
            print("Moving file: " + str(old))
            subprocess.run("rsync -a " + old + " " + outdir + "; rm " + old, shell=True)
            found = True

if not found:
    print("No files to copy found.")

print("Movestreams complete.")
