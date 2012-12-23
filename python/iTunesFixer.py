#############################################################################
#  iTunes Fixer                                                             #
# --------------------------------------------------------------------------#
# Simple script that iterates the collection and deletes duplicated files   #
# based on their MD5 checksum                                               #
#                                                                           # 
# --------------------------------------------------------------------------#
#                    Miguel Carranza 22 Dec 2012                            # 
#############################################################################

from sys import argv
import sys 
import os
import hashlib

# Main function
def main ():
  checkArgs()
  libraryPath = argv[1]
  print "Cleaning iTunes Library: %s" % libraryPath 
  cleanLibrary(libraryPath)
  print "The library is now fixed! Go and listen to some good music ;)"

# Recursive function to clean the library
def cleanLibrary (path):
  for root, dirs, files in os.walk(path):
    # recursive call 
    for dir in dirs:
      cleanLibrary(os.path.join(root, dir)) 

    # process its own files
    mp3s = []
    hashes = []
    duplicates = 0
    
    # filter mp3s
    for file in files:
      if os.path.splitext(file)[1].lower() == '.mp3':
        mp3s.append(file)

    # look for duplicates
    for mp3 in mp3s:
      mp3path = os.path.join(root, mp3)
      hash = md5sum(mp3path)
      if hash in hashes:
        # Duplicate!
        os.remove(mp3path)
        duplicates += 1
      else:
        # Store md5
        hashes.append(hash)
    
    if duplicates > 0:
      print "  %s cleant. %d duplicated songs has been deleted" % (os.path.basename(root), duplicates)
    
    # Stop walking
    break

# Calculate md5sum 
def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
             md5.update(chunk)
    return md5.hexdigest()

# Check input sanity
def checkArgs():
  scriptName = argv[0]
  if len(argv) != 2:
    sys.stderr.write("Usage: %s <iTunes Library Path>\n" % scriptName)
    sys.exit()

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()