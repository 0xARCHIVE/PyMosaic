# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:33:42 2016

@author: Steven
"""

from lib import fetch_icons
from lib import process_icons

subdir_name = 'Dota2_icons'
#fetch_icons.fetch_icons(subdir_name)
#process_icons.dota_process_icons(subdir_name)

process_icons.image_replicate(subdir_name)

print('Complete')