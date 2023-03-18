import os
import shutil

scriptPath = __file__
source_folder = scriptPath[:-25] + '/data/'

destination_folder = scriptPath[:-25] + '/dashboard/assets/external/copiedData/'

# fetch all files
for file_name in os.listdir(source_folder):
    # construct full file path
    source = source_folder + file_name
    destination = destination_folder + file_name
    # copy only files
    if os.path.isfile(source):
        shutil.copy(source, destination)
        print('copied', file_name)