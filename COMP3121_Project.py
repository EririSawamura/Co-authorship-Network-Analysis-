import networkx as nx
from networkx.algorithms import community
import math
import matplotlib.pyplot as plt

def getGraph():
    Graph = nx.Graph()
    FILE = open("hep-th.txt", "r")
    line_list = FILE.readlines()
    # build up the graph
    for i in range(len(line_list)):
        if i == 0:
            current_line = line_list[i]
            continue
        if i > 0:
            if line_list[i][0].isdigit():
                # do the split for the current_line because the current_line is a complete entry
                attributes = current_line.split(',')
                attributes[3] = attributes[3].replace(" ", "")
                attributes[3] = attributes[3].replace("\\", "")
                attributes[3] = attributes[3].replace(")", "")
                attributes[3] = attributes[3].replace(".", "")
                attributes[3] = attributes[3].replace("\t", "")
                attributes[3] = attributes[3].strip()
                authors = attributes[3].split("&")
                if len(authors) == 1:
                    Graph.add_node(authors[0])
                for j in range(len(authors)):
                    for k in range(j + 1, len(authors)):
                        Graph.add_edge(authors[j], authors[k])
                current_line = line_list[i]
            else:
                # concatenate the line_list[i] to the previous current_line
                current_line = current_line + line_list[i]
                continue
    FILE.close()
    return Graph
## This function returns a bar chart for the degree distribution
def degree_distribution(Graph):
    degree = nx.degree_histogram(Graph)
    x = list(range(len(degree)))
    y = [i for i in degree]
    plt.bar(x, y)
    plt.title('Degree Distribution(Bar chart)')
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    for a, b in zip(x,y):
        plt.text(a, b+8,'%.0f' % b, ha='center')
    plt.savefig("degree_distribution.png")
    plt.show()
    return

## This function returns a scatter plot for the degree distribution
def scatterplot_degree_distribution(Graph):
    degree = nx.degree_histogram(Graph)
    x = list(range(len(degree)))
    y = [i for i in degree]
    a = []                       ##process the data to remove meaningless value
    b = []
    for j in range(len(x)):
        if(x[j] != 0 and y[j] != 0):
            a.append(j)
            b.append(y[j])
    plt.scatter(a, b,s = 15, alpha = 0.4)
    plt.title('Degree Distribution(Scatter plot) with removing 0 values')
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    plt.savefig("scatterplot_degree_distribution.png")
    plt.show()
    return

## This function returns a scatter plot for the Log-Log degree distribution
def log_degree_distribution(Graph):
    degree = nx.degree_histogram(Graph)
    x = list(range(len(degree)))
    y = [i for i in degree]
    a = []
    b = []
    for j in range(len(x)):
        if(x[j] != 0 and y[j] != 0):
            a.append(j)
            b.append(y[j])
    for i in range(len(a)):
        a[i] = math.log(a[i])
    for j in range(len(a)):
        b[j] = math.log(b[j])
    plt.scatter(a, b,s = 15, alpha = 0.4)
    plt.title('Log-log Degree Distribution(Scatter plot) with removing 0 values')
    plt.xlabel('Log of Degree')
    plt.ylabel('Log of Number of Nodes')
    plt.savefig("log-log_degree_distribution.png")
    plt.show()
    return

def clustering_coefficient(Graph):
    d = nx.clustering(Graph)
    sum = 0
    for k in d:
        sum = sum + d[k]
    avg = sum / len(d)
    print("The average clustering is:", avg)

def Node_similarity(G):
    E = G.number_of_edges()
    X = int(E/100)
    component_sizelist = list()
    percent_deletionlist = list()
    # calculate all the edges adj nodes' similarity
    for edge in list(G.edges):
        G.add_edge(edge[0], edge[1], similarity=len(list(nx.common_neighbors(G, edge[0], edge[1]))))

    while(G.number_of_edges()>X):
        # sort edges with similarity
        edges = sorted(G.edges(data=True), key=lambda x: x[2]['similarity'], reverse=True)
        #calculate size of the largest connected component and percentage of the deleted edges repectively
        component_sizelist.append(len(max(nx.connected_components(G), key=len)))
        percent_deletionlist.append((E - G.number_of_edges()) / E)
        for i in range(X):
            G.remove_edge(edges[i][0],edges[i][1])
    component_sizelist.append(0)
    percent_deletionlist.append(1)
    #plot
    plt.plot(percent_deletionlist,component_sizelist)
    plt.xlabel('Percentage of the deleted edges')
    plt.ylabel('Size of largest connected component')
    plt.title('Q6')
    plt.show()

def Network_connectivity(G):
    #get componnetn set from G
    component = nx.connected_components(G)
    # get component size and num dictionary
    component_dict = dict()
    for subgraph in component:
        if len(subgraph) not in component_dict:
            component_dict[len(subgraph)]=0
        component_dict[len(subgraph)]+=1
    # get log(size) and log(num) list
    size_list = sorted(list(component_dict.keys()))
    num_list = list()
    for size in size_list:
        num_list.append(component_dict[size])
    size_list = list(map(lambda x: math.log(x,2), size_list))
    num_list = list(map(lambda x: math.log(x,2), num_list))
    #scatter
    plt.scatter(size_list, num_list)
    plt.xlabel('log(size)')
    plt.ylabel('log(num)')
    plt.title('Q5')
    plt.show()

def draw_scatterplotQ4(Graph):
    subgraphs = list(nx.connected_component_subgraphs(Graph))
    centrilist = centricnode(Graph)
    fig = plt.figure(num = 1, figsize=(10,6))
    plt.xlabel('j')
    plt.ylabel('Rj')
    j = []
    Rj = []
    #draw
    for i in range(0, len(subgraphs)):
        dict1= num_nodes_from_centric(subgraphs[i], centrilist[i])
        j = j + list(dict1.keys())
        Rj = Rj + list(dict1.values())
    plt.scatter(j, Rj, s =15)
    plt.title('Scatter plot of J: length from centric node, Rj: number of nodes reached at length j ')
    plt.show()

#return a dictionary storing the average shortest path length for each connected subgraph
def average_shortest_path_length_graph(Graph):
    print("The average shortest path length for each connected subgraph:")
    dict1 = {}
    i = 0
    graphs = list(nx.connected_component_subgraphs(Graph))
    for C in graphs:
        #The default method is Dijkstra (BFS is a special Dijkstra with each edge'weight equal to 1)
        dict1[i] = nx.average_shortest_path_length(C)
        i = i + 1
    print(dict1)
    return dict1

#return a dictionary keyed by the subgraphs'number, valued by a dictionary which is keyed by the nodes in subgraph and valued by the average shortest path length of the keyed node in subgraph
def shortest_path_length_node(Graph):
    dict_all = {}
    i = 0
    graphs = list(nx.connected_component_subgraphs(Graph))
    for C in graphs:
        #keyed by node and valued by the average shortest path
        dict_sub = {}
        iterator = dict(nx.shortest_path_length(C))
        n = len(iterator)
        
        #if n == 1, it means that the whole subgraph contains one node, iterator = {node_name : 0}
        if n == 1:
            dict_all[i] = list(iterator.values())[0]
            i = i + 1
            continue
        
        for key1 in iterator:
            key1_total_path_length = 0
            key1_avg_path_length = 0
            for key2 in iterator[key1]:
                key1_total_path_length = key1_total_path_length + iterator[key1][key2]
            key1_avg_path_length = key1_total_path_length / (n -1)
            dict_sub[key1] = key1_avg_path_length
        dict_all[i] = dict_sub
        i = i + 1
    return dict_all

#return a dictionary keyed by the subgraphs'number, valued by the centric node of the subgraph
def centricnode(Graph):
    dict1 = shortest_path_length_node(Graph)
    dict2 = {}
    for key1 in dict1:
        #the subgraph has at least 2 nodes
        if len( dict1[key1]) > 1:
            small = list(dict1[key1])[0]
            for key2 in dict1[key1]:
                if dict1[key1][key2] < dict1[key1][small]:
                    #key2 is a node name, the value of dict1[key1][key2] indicates the average shortest path of key2 in subgraph "key1"
                    small = key2
            dict2[key1] = small
        else:
            #the centric node for a one node subgraph is itself
            dict2[key1] = list(dict1[key1])[0]
    return dict2

#for each subgraph, calculate the number of nodes that can reached by centric node; return a dictionary keyed by length from the centric node, valued by the number of nodes that can be reached
def num_nodes_from_centric(subgraph, cen_node):
    dict1 = {}
    j, count = 0, 0
    visited, queue = [], [cen_node]
    
    while queue:
        dict1[j] = count
        for i in range(0, count):
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                neigh = list(subgraph.neighbors(vertex))
                subgraph.remove_node(vertex)
                for n in neigh:
                    if n not in queue:
                        queue.append(n)
        count =  len(queue)
        j = j + 1
    return dict1

def Modularity_Maximization(Graph):
    """Use greedy_modularity_communities(Graph) to create communites"""
    Communities = community.greedy_modularity_communities(Graph)
    community_size = {}
    NewGraph = nx.Graph()
    count = 0
    DensitySum = 0

    """Use iterations to make graph of communities and calculate average density"""
    for i in range(len(Communities)):
        EdgeCount = 0
        Component = Communities[i]
        NewGraph.add_nodes_from(Component)
        if len(Component) not in community_size.keys():
            community_size[len(Component)] = 1
        else:
            community_size[len(Component)] += 1
        for i in Component:
            for j in Component:
                if i in Graph.neighbors(j) and i not in NewGraph.neighbors(j):
                    EdgeCount += 1
                    NewGraph.add_edge(i, j)
        if len(Component) > 1:
            DensitySum += EdgeCount / (len(Component) * (len(Component) - 1) / 2)
        count += 1

    """Print result"""
    print("------------------------------------------------------------")
    print("The community detection by Modularity_Maximization")
    nx.draw(NewGraph, node_size = [1]*NewGraph.number_of_nodes())
    plt.show()
    print("The number of communities: " + str(count))
    print("The average density of communities: " + str(DensitySum / count))
    print("------------------------------------------------------------")
    CreateScatterChart(community_size)
    labels = 'size:1', 'size:2', 'size:3', 'size:4', 'size:>5'
    sizes = [0, 0, 0, 0, 0]
    for key, value in community_size.items():
        if key == 1:
            sizes[0] += value
        elif key == 2:
            sizes[1] += value
        elif key == 3:
            sizes[2] += value
        elif key == 4:
            sizes[3] += value
        else:
            sizes[4] += value
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("The distribution of communities")
    plt.savefig('Pie.png', bbox_inches='tight')
    plt.show()

def K_clique(Graph, k):
    """Use k_clique_communities(Graph, k) to create communites"""
    community_generator = community.k_clique_communities(Graph, k)
    community_size = {}
    NewGraph = nx.Graph()
    count = 0
    DensitySum = 0

    """Use iterations to make graph of communities and calculate average density"""
    while (True):
        try:
            EdgeCount = 0
            Component = next(community_generator)
            NewGraph.add_nodes_from(Component)
            if len(Component) not in community_size.keys():
                community_size[len(Component)] = 1
            else:
                community_size[len(Component)] += 1
            for i in Component:
                for j in Component:
                    if i in Graph.neighbors(j) and i not in NewGraph.neighbors(j):
                        EdgeCount += 1
                        NewGraph.add_edge(i, j)
            if len(Component) > 1:
                DensitySum += EdgeCount / (len(Component) * (len(Component) - 1) / 2)
            count += 1
        except StopIteration:
            break

    """Print result"""
    print("------------------------------------------------------------")
    print("The community detection by k-clique algorithm with k="+str(k))
    nx.draw(NewGraph, node_size=[1]*NewGraph.number_of_nodes())
    plt.savefig('NewGraph.png', bbox_inches='tight')
    plt.show()
    print("The number of communities: " + str(count))
    print("The average density of communities: " + str(DensitySum / count))
    print("------------------------------------------------------------")
    CreateScatterChart(community_size)
    labels = 'size:1~3', 'size:4', 'size:5~7', 'size:>7'
    sizes = [0, 0, 0, 0]
    for key, value in community_size.items():
        if key <= 3:
            sizes[0] += value
        elif key == 4:
            sizes[1] += value
        elif key >= 5 and key <= 7:
            sizes[2] += value
        else:
            sizes[3] += value
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("The distribution of communities")
    plt.savefig('Pie.png', bbox_inches='tight')
    plt.show()

def Girvan_newman(Graph):
    """Use Girvan_newman(Graph) to create communites"""
    community_generator = community.girvan_newman(Graph)
    communities = tuple(sorted(c) for c in next(community_generator))
    community_size = {}
    NewGraph = nx.Graph()
    count = len(communities)
    DensitySum = 0

    """Use iterations to make graph of communities and calculate average density"""
    for component in communities:
        EdgeCount = 0
        NewGraph.add_nodes_from(component)
        if len(component) not in community_size.keys():
            community_size[len(component)] = 1
        else:
            community_size[len(component)] += 1
        for i in component:
            for j in component:
                if i in Graph.neighbors(j) and i not in NewGraph.neighbors(j):
                    EdgeCount += 1
                    NewGraph.add_edge(i, j)
        if len(component) > 1:
            DensitySum += EdgeCount / (len(component) * (len(component) - 1) / 2)

    """Print result"""
    print("------------------------------------------------------------")
    print("The community detection by Girvan_newman algorithm")
    nx.draw(NewGraph, node_size=[1]*NewGraph.number_of_nodes())
    plt.savefig("Girvan_newman.png")
    plt.show()
    print("The number of communities: " + str(count))
    print("The average density of communities: " + str(DensitySum / count))
    print("------------------------------------------------------------")
    CreateScatterChart(community_size)
    labels = 'size:1', 'size:2', 'size:3', 'size:4', 'size:>5'
    sizes = [0, 0, 0, 0, 0]
    for key, value in community_size.items():
        if key == 1:
            sizes[0] += value
        elif key == 2:
            sizes[1] += value
        elif key == 3:
            sizes[2] += value
        else:
            sizes[3] += value
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("The distribution of communities")
    plt.savefig('Pie.png', bbox_inches='tight')
    plt.show()

def CreateScatterChart(community_size):
    plt.scatter(list(community_size.keys()), list(community_size.values()))
    endx = max(list(community_size.keys())) - max(list(community_size.keys()))%10 + 10
    endy = max(list(community_size.values())) - max(list(community_size.values())) % 10 + 10
    plt.axis([0, endx, 0, endy])
    plt.title("The distribution of communities")
    plt.xlabel("The size of communities")
    plt.ylabel("The number of communities")
    plt.savefig('Bar.png', bbox_inches='tight')
    plt.show()

def main():
    Graph = getGraph()
    while(True):
        print('======== COMP3121 Project ========')
        print('Task 1: Network degree distribution\nTask 2: Clustering co-efficiency\n'
              'Task 3: Shortest path length\nTask 4: Network centrality\n'
              'Task 5: Network connectivity\nTask 6: Node similarity\n'
              'Task 7: Community discovery\n')
        choice = input("Please input the task number:  ")
        while(len(choice)>1 or choice>'7' or choice<'1'):
            choice = input("Wrong input! Please input the task number again:")
        if choice == '1':
            degree_distribution(Graph)
            scatterplot_degree_distribution(Graph)
            log_degree_distribution(Graph)
        elif choice == '2':
            clustering_coefficient(Graph)
        elif choice == '3':
            average_shortest_path_length_graph(Graph)
        elif choice == '4':
            draw_scatterplotQ4(Graph)
        elif choice == '5':
            Network_connectivity(Graph)
        elif choice == '6':
            Node_similarity(Graph)
        else :
            print('Community detection 1: K_clique detection algorithm\n'
                  'Community detection 2: Modularity_Maximization detection algorithm\n'
                  'Community detection 3: Girvan_newman detection algorithm\n')
            CommunityChoice = input("Please input the community detection number: ")
            while (len(CommunityChoice) > 1 or CommunityChoice > '3' or CommunityChoice < '1'):
                CommunityChoice = input("Wrong input! Please input the community detection number again:  ")
            if CommunityChoice == '1':
                Number_k = eval(input("Please enter number k:"))
                K_clique(Graph, Number_k)
            elif CommunityChoice == '2':
                Modularity_Maximization(Graph)
            else:
                Girvan_newman(Graph)
        choice = input("Please input 1 to exit or input 2 to go back to main menu:  ")
        while (len(choice)>1 or choice > '2' or choice < '1'):
            choice = input("Wrong input! Please input the task number again:")
        if choice == '1':
            exit(0)
        else:
            pass


main()
