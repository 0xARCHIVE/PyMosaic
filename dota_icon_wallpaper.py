from lib import fetch_icons
from lib import process_icons

subdir_name = 'Dota2_icons'
#fetch_icons.fetch_icons(subdir_name) #fetch_icons.fetch_icons(subdir_name) downloads a bunch of Dota 2 icons and sticks them into './subdir_name/'
#process_icons.dota_process_icons(subdir_name)

process_icons.image_replicate(subdir_name)  #the actual mosaic generating function. It duplicates "./collage_target.png", so make sure to create one!

print('Complete')
