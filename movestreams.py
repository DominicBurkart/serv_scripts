import sys
import subprocess
import time
import os

indir = sys.argv[1]
outdir = sys.argv[2]

two_days = 48 * 60 * 60
one_month = two_days * 15

print("Movestreams started. Copying files that haven't been edited for at least 48 hours.")

found = False
for root, dirs, files in os.walk(indir):
    for f in files:
        old = os.path.join(root, f)
        if time.time() - os.path.getmtime(old) > two_days:
            print("Moving file: " + str(old))
            subprocess.run("rsync -a " + old + " " + outdir + "; rm " + old, shell=True)
            found = True

if not found:
    print("No files to copy found.")

print("Movestreams complete.")
