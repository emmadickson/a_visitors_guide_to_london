import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
import json 

directory = './ maps'
structure = {}
graph_data = {"nodes": [], "links": []}
count = 0
for file in os.listdir('./ maps'):
    filename = os.fsdecode(file)
    if filename.endswith(".map"):
        filename_formal = (os.path.join(str(directory), str(filename)))
        fileimage_formal = (os.path.join(str('./ images'), str(filename).split('.map')[0] + '.gif'))
        final_file_name = './annotated_images/' + str(filename).split('.map')[0] + '.png'
       
        structure[str(filename).split('.map')[0]] = {'count': count, 'filename': final_file_name, 'children': []}
        count += 1
        filedata = open(filename_formal, 'r')
        im = Image.open(fileimage_formal)

        fig, ax = plt.subplots()
        ax.imshow(im)

        plt.axis('off')
        for lines in filedata.readlines():
                if 'rect' in lines:
                    coordinates = lines.split('.html')[1].strip()
                    name = lines.split('.html')[0].split(' ')[1]
                    x1 = coordinates.split(' ')[0].split(',')[0]
                    y1 = coordinates.split(' ')[0].split(',')[1]
                    x2 = coordinates.split(' ')[1].split(',')[0]
                    y2 = coordinates.split(' ')[1].split(',')[1]
                    
                    # Create a Rectangle patch
                    rect = patches.Rectangle((int(x1), int(y1)), int(x2), int(y2), linewidth=1, edgecolor='r', facecolor='none')
                    structure[str(filename).split('.map')[0]]['children'].append({'name': name, 'coordinates': [x1,x2,y1,y2]})
                    # Add the patch to the Axes
                    ax.add_patch(rect)
                
                    t = plt.text(int(x1),int(y1),name + '.html', color='white', fontsize='6')
                    t.set_bbox(dict(facecolor='red', alpha=0.5, edgecolor='red'))

        plt.savefig(final_file_name, bbox_inches='tight')
        


        continue
    else:
        continue

# Open and read the JSON file
f = open('user_paths.json', 'r') 
data = json.load(f)


for key in structure.keys():
    users = []

    for user in data['users']:
        for path in user['path']:
            #print(f"comparing: {path[0]} to {key}")
            if (path[0] == key):
                users.append(user['name'])
                print(users)
    graph_data['nodes'].append({'name': key+ '.html', 'image': 'annotated_images/' + key+ '.png', 'users': users})
 
      
    for child in structure[key]['children']:
        target_index = structure[child['name']]['count']


        graph_data['links'].append({'id':f"{ structure[key]['count']}-{target_index}", 'source': structure[key]['count'], 'target': target_index, 'users': []})

# Iterate through users and their paths
def search_by_id(graph_data, target_id):
    for link in graph_data['links']:
        if link['id'] == target_id:
            return link
    return None 

for user in data['users']:
    for path in user['path']:
        id = f"{structure[path[0]]['count']}-{structure[path[1]]['count']}"
  
        result = search_by_id(graph_data, id)
        if result:
            result['users'].append(user['name'])

        
with open("graph.json", "w") as file:
       json.dump(graph_data, file)


