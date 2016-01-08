from lib import fetch_icons
from lib import process_icons

## CONFIGURATION SETTINGS (you can change these) ##
icons_subdir = 'Dota2_icons' #subdirectory containing all of the icons to use in the mosaicing process
size_mod = 1    #changing this reduces the size of the final mosaic by a factor of 1/size_mod in both directions (default = 1)
## END CONFIGURATION SETTINGS (don't change anything below this) ##

fetch_icons.fetch_icons(icons_subdir) #downloads icons and save them in './icons_subdir/'
loaded_icons = process_icons.process_icons(icons_subdir) #preload the icons

while True:    
    input_file_path = input('Location of input file: ')
    
    #strip speech marks from start/end if they've been added by accident
    if (input_file_path[0] == '"'):
        input_file_path = input_file_path[1:]
    if (input_file_path[-1] == '"'):
        input_file_path = input_file_path[:-1]
    
    print('Working...')
    process_icons.image_replicate(input_file_path,icons_subdir,loaded_icons,size_mod)  #mosaic-ify the inputted file location
    print('Complete')

while True:
    continue