
ghenv.Component.Name = "File Creator"

import Grasshopper as gh
import os
import io
gh_path = ghdoc.Path # Get GH file path
ext = "ghx"
file = os.path.dirname(os.path.realpath(gh_path)) # Get GH file directory to save to
if "." not in ext: ext = "." + ext
else: pass

if os.path.exists(file) == False: # Test if file already exists; if it doesn't, proceed
    file = name + ext # Set file name and extension
if os.path.exists(file) == True: # If it does exists, follow the next steps
    file_count = len([f for f in os.walk(".").next()[2] if f[-4:] == ext]) # Find all files with the same extension
    file = name + "_" + str(file_count) + ext # Add the number to the new file name as a differentiator
    file_path = file

if write:
    with io.open(file, "w", encoding="utf-8") as file_handle:
        file_handle.write(content)
        file_handle.close()
