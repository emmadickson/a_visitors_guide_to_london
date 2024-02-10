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

for key in structure.keys():
    graph_data['nodes'].append({'name': key+ '.html'})
    
    for child in structure[key]['children']:
        target_index = structure[child['name']]['count']


        graph_data['links'].append({'source': structure[key]['count'], 'target': target_index})
    
print(graph_data)
with open("graph.json", "w") as file:
       json.dump(graph_data, file)


