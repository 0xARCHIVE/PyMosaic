from urllib.request import urlopen
import json
import os

icon_blacklist = ['Power_Treads.gif','Stats.png','NoItem.png','Invoker_empty1.png','Invoker_empty2.png','Doom_bringer_empty1.png','Doom_bringer_empty2.png']

def fetch_icons_category(subdir_loc,icon_category):
    if (icon_category == None):
        return
    
    print('Fetching list of icons')
    response = urlopen('http://wiki.teamliquid.net/commons/api.php?format=json&action=query&list=categorymembers&cmtype=file&cmlimit=max&cmtitle=Category:' + icon_category) #dota icons
    response_json = response.read()
    response_data = json.loads(response_json.decode())
    
    print('Fetching individual icons')
    for member in response_data['query']['categorymembers']:
        pageid = str(member['pageid'])   #pageID of the page containing the full image URL
        
        response = urlopen('http://wiki.teamliquid.net/commons/api.php?format=json&action=query&prop=info&pageids=' + pageid + '&prop=imageinfo&iiprop=url') #dota icons
        response_json = response.read()
        response_data = json.loads(response_json.decode())
        
        icon_url = response_data['query']['pages'][pageid]['imageinfo'][0]['url']
        if (icon_url != None):
            icon_name = os.path.basename(icon_url)
            if (icon_name in icon_blacklist):
                print('Skipped blacklisted icon ' + icon_name)
                continue
            
            #download image data
            print('Downloading ' + icon_name)
            response = urlopen(icon_url)
            response_img = response.read()
            
            #write image data to file
            impath = os.path.join(subdir_loc,icon_name)
            imfile = open(impath,'wb')
            imfile.write(response_img)
            imfile.close()
            
def fetch_icons(subdir_name):
    subdir_loc = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', subdir_name))
    
    #check if subdirectory exists to put icons in
    if not os.path.exists(subdir_loc):
        print('Creating subdirectory ' + subdir_name + ' (' + subdir_loc + ')')
        os.makedirs(subdir_loc)
    
    #check if subdirectory has any icons in it
    if not os.listdir(subdir_loc):
        print('Fetching item icons')
        fetch_icons_category(subdir_loc,'Item_Icons')
        print('Complete')
        
        print('Fetching spell icons')
        fetch_icons_category(subdir_loc,'Spell_Icons')
        print('Complete')

if '__main__' == __name__:
    fetch_icons("Dota2_icons")
