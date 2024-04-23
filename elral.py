import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
 
def read_station_file():
    # Opening JSON file
    f = open('stations.json')
     
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data

def read_train_class_file():
    # Opening JSON file
    f = open('train-class.json')
     
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data

def read_track_file():
    # Opening JSON file
    f = open('track.json')
     
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data

def read_line_file():
    # Opening JSON file
    f = open('lines.json')
     
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    return data

def transit_time( lenght, Ta, La, Tf, Lf, vmax ):
    tran_time = 0.0 #seconds
    #caso dove lenght < (La+Lf) allora T = Ta + Tf
    if( lenght < (La+Lf)):
        tran_time = Ta/3600 + Tf/3600
    else:
        #caso dove lenght >= (La+Lf) allora T = (lenght - (La+Lf))/vmax + Ta + Tf
        lenght_c = lenght - (La+Lf)
        tran_time = lenght_c/vmax + Ta/3600 + Tf/3600
    
    return tran_time
    


def select_node_orange(G) :
    # You can select like this
    # selected_data = dict( (n,d['at']) for n,d in P.nodes().items() if d['at'] == 5)
    # Then do what you want to do with selected_data
    # print(f'Node found : {len (selected_data)} : {selected_data}')
    #selected_data = dict( (n,d) for n,d in G.nodes(data=True) if d['color'] == 'orange')
    #print(f'Node found : {len (selected_data)} : {selected_data}')
    selected_edges = [(u,v,e) for u,v,e in G.edges(data=True) if e['name'] == 'Blue']
    #print( selected_edges)
    return selected_edges
    #print(selected_edges)

def timeEdge( Edge ):
    u,v = Edge
    #tracks = Edge['numbers']
    track = G[u][v]
    print( Edge)
    print( track ) 
    #{0: {'color': 'm', 'weight': 3, 'name': 'Orange', 'lenght': 22, 'speed': 140, 'numbers': 1}}
    track_speed = track[0]['speed']
    track_lenght = track[0]['lenght']
    track_numbers = track[0]['numbers']
    
def get_itinerary( lines, line_name):
    itinerary = {}
    nodes_itinerary = {}
    nodes = []

    for aline in lines['lines']:
        line = aline['line']
        if line['name'] == line_name:
            #print( line )
            stations_line = line['track']
            itinerary['stations'] = stations_line

    for node in itinerary['stations']:
        nodes.append(node['node'])
    n_edges = []
    for i in range(0, len(nodes)-1):
        nlist = Blue.get_edge_data(nodes[i],nodes[i+1])
        #print( nlist )
        tmp =  (nodes[i],nodes[i+1]), nlist
        n_edges.append( tmp )
    itinerary['edge'] = n_edges
    #print( itinerary )
    return itinerary

def drawNetworkGraph():
    os = nx.get_node_attributes(AV, 'pos')
    colors = []
    weights = []
    shapes = []
    sizes = []

    for (u,v,attrib_dict) in list(Blue.edges.data()):
        colors.append(attrib_dict['color'])
        weights.append(attrib_dict['weight'])
        
    for (node, attrib_dict) in list(Blue.nodes.data()):
        node_category = attrib_dict['node_category']    
        if node_category == 1:
            shapes.append("s")
        elif node_category == 2:
            shapes.append("s")
        else:
            shapes.append("o")

        sizes.append(attrib_dict['node_size'])

    #selected_edges = select_node_orange(Blue)
    #for edge in selected_edges:
    #    (u,v,e)= edge
    #    track_transit = transit_time(e['lenght'] , 60, 0.917, 70, 1, 110)
    #    print( str(e['lenght']) + '\t' + str(round(track_transit*60 ))+ ' minutes')

    test_itinerary = get_itinerary( lines, 'TEST A')
    edges_itinerary = test_itinerary['edge']
    for edge in edges_itinerary:
        (u,v),attr = edge
        track_transit = transit_time( attr[0]['lenght']  , 60, 0.917, 70, 1, 110)
        print( "(" + str(u) + " -> " + str( v) + " ) \t" + str(round(track_transit*60 ))+ ' minutes')

    nx.draw_networkx(Blue, pos, node_size=sizes, node_shape = 'o', edge_color=colors, width=weights,  with_labels=True)


node_sizes = []
#G = nx.MultiGraph()   
AV = nx.MultiGraph() # AV yellow line
Blue = nx.MultiGraph() # Blu line

stations = read_station_file()
track = read_track_file()
train_class = read_train_class_file()
lines = read_line_file()

#print( lines )

for station in stations['stations']:
    node_cat = station['CAT']

    if node_cat == 1:
        size = 300
        shape = 's'
    elif node_cat == 2:
        size = 200
        shape = 's'
    else:
        size = 150
        shape = 'o'

    AV.add_node(station['CODE'], node_size = size, node_shape = shape, node_color="black", pos=(station['X'], station['Y']), name=station['NAME'], node_category=station['CAT'])   
    Blue.add_node(station['CODE'], node_size = size, node_shape = shape, node_color="black", pos=(station['X'], station['Y']), name=station['NAME'], node_category=station['CAT'])   
    
    #print(station)

for aline in track['lines']:
    line = aline['line']
    #print( line )
    line_name = line['name']
    #print( line_name )
    line_color = line['color']
    line_weight = line['weight']

    for line_edge in line['edge']:
        #print( line_edge )
        track_from = line_edge['from']
        track_to =  line_edge['to']
        track_lenght = line_edge['lenght']
        track_speed = line_edge['speed']
        track_numbers = line_edge['tracks']  
        #print( G.nodes[ from_node])
        if line_name == 'AV':
            AV.add_edge(track_from, track_to, color=line_color, weight= line_weight ,name=line_name, lenght=track_lenght, speed = track_speed, numbers = track_numbers )    
        elif line_name == 'Blue':
            Blue.add_edge(track_from, track_to, color=line_color, weight= line_weight ,name=line_name, lenght=track_lenght, speed = track_speed, numbers = track_numbers )
        
     #   G.add_edge(track_from, track_to, color=line_color, weight= line_weight ,name=line_name, lenght=track_lenght, speed = track_speed, numbers = track_numbers )


pos = nx.get_node_attributes(AV, 'pos')


#test_itinerary = get_itinerary( lines, 'TEST A')

#for edge in list(G.edges()):
#    timeEdge(edge)
#colors = [G[u][v]['color'] for u,v in edges]
#weights = [G[u][v]['weight'] for u,v in edges]

colors = []
weights = []
shapes = []
sizes = []

for (u,v,attrib_dict) in list(Blue.edges.data()):
    colors.append(attrib_dict['color'])
    weights.append(attrib_dict['weight'])
        
for (node, attrib_dict) in list(Blue.nodes.data()):
    node_category = attrib_dict['node_category']    
    if node_category == 1:
        shapes.append("s")
    elif node_category == 2:
        shapes.append("s")
    else:
        shapes.append("o")

    #shapes.append(attrib_dict['node_shape'])
    sizes.append(attrib_dict['node_size'])

#print( train_class)

#selected_edges = select_node_orange(Blue)
#for edge in selected_edges:
#    (u,v,e)= edge
#    track_transit = transit_time(e['lenght'] , 60, 0.917, 70, 1, 110)
#    print( str(e['lenght']) + '\t' + str(round(track_transit*60 ))+ ' minutes')

#test_itinerary = get_itinerary( lines, 'TEST A')
#edges_itinerary = test_itinerary['edge']
#for edge in edges_itinerary:
#    (u,v),attr = edge
#    track_transit = transit_time( attr[0]['lenght']  , 60, 0.917, 70, 1, 110)
#    print( "(" + str(u) + " -> " + str( v) + " ) \t" + str(round(track_transit*60 ))+ ' minutes')

#nx.draw_networkx(Blue, pos, node_size=sizes, node_shape = 'o', edge_color=colors, width=weights,  with_labels=True)
# utilizza drawNode per disegnare i nodi

# utilizza drawLabel per disegnare le etichette
drawNetworkGraph()
plt.savefig("filename.png")
plt.draw()  # pyplot draw()
plt.show()  # pyplot show()
    