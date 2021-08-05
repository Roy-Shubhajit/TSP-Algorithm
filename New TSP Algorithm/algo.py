import datetime
import copy
import networkx as nx
from load import *
from dataclasses import dataclass

#import matplotlib.pyplot as plt

@dataclass
class paths:
	path: []
	cost: float = 0.0

def iscycle(v,path):
	M = nx.empty_graph(v)
	for i in path:
		w = i[2]['weight']
		M.add_edge(i[0],i[1], weight = w)
	try:
		nx.find_cycle(M, orientation="original")
		return True
	except nx.exception.NetworkXNoCycle as err:
		return False

def morethantwo(v,path):
	M = nx.empty_graph(v)
	for i in path:
		w = i[2]['weight']
		M.add_edge(i[0],i[1], weight = w)
	degrees = [val for (node, val) in M.degree()]
	for i in degrees:
		if i > 2:
			return True
	return False

def not_two(v,path):
	M = nx.empty_graph(v)
	for i in path:
		w = i[2]['weight']
		M.add_edge(i[0],i[1], weight = w)
	degrees = [val for (node, val) in M.degree()]
	for i in degrees:
		if i != 2:
			return True
	return False

def cost(path):
	c = 0.0
	for i in range(len(path)):
		c = c + path[i][2]['weight']
	return c

def calc_cost(G,path):
	cost = 0.0
	i = 0
	while i < len(path)-1:
		cost += G[path[i]][path[i+1]]['weight']
		i = i+1
	return cost

def calc_mst(G):
	mst = nx.minimum_spanning_edges(G,algorithm="prim",data=False)
	edgelist = list(mst)
	cost = 0
	for e in edgelist:
		cost += G.edges[e]['weight']
	return cost

def dfs(G,src):
	t1 = datetime.datetime.now()
	tsp = paths([])
	stack = [[src]]
	while len(stack) > 0:
		path = stack.pop()
		v = path[-1]
		for w in nx.all_neighbors(G,v):
			if w not in path:
				next_path = path.copy()
				next_path.append(w);
				stack.append(next_path)
		
				if len(next_path) == G.number_of_nodes():
					if G.has_edge(next_path[-1],src):
						next_path.append(src)
						cost = calc_cost(G,next_path)
						if tsp.cost == 0.0 or cost < tsp.cost:
							tsp.cost = cost
							tsp.path = next_path
	t2 = datetime.datetime.now()
	print("Time taken by DFS (hr:min:sec): ", t2-t1)
	return tsp

def bfs(G,src):
	t1 = datetime.datetime.now()
	tsp = paths([])
	queue = [[src]]
	while len(queue) > 0:
		path = queue.pop(0)
		v = path[-1]
		for w in nx.all_neighbors(G,v):
			if w not in path:
				next_path = path.copy()
				next_path.append(w)
				queue.append(next_path)
				if len(next_path) == G.number_of_nodes():
					if G.has_edge(next_path[-1],src):
						next_path.append(src)
						cost = calc_cost(G,next_path)
						if tsp.cost == 0.0 or cost < tsp.cost:
							tsp.cost = cost
							tsp.path = next_path
	t2 = datetime.datetime.now()
	print("Time taken by BFS (hr:min:sec): ", t2-t1)
	return tsp

def ids(G,src):
	t1 = datetime.datetime.now()
	i = 1
	while i <= G.number_of_nodes():
		tsp = paths([])
		stack = [[src]]
		path = []
		while len(stack) > 0:
			if len(path) == i:
				break
			path = stack.pop()
			v = path[-1]
			for w in nx.all_neighbors(G,v):
				if w not in path:
					next_path = path.copy()
					next_path.append(w);
					stack.append(next_path)
			
					if len(next_path) == G.number_of_nodes():
						if G.has_edge(next_path[-1],src):
							next_path.append(src)
							cost = calc_cost(G,next_path)
							if tsp.cost == 0.0 or cost < tsp.cost:
								tsp.cost = cost
								tsp.path = next_path
		i = i+1
	t2 = datetime.datetime.now()
	print("Time taken by Iterative Deepening (hr:min:sec): ", t2-t1)
	return tsp

def dfbb(G,src):
	t1 = datetime.datetime.now()
	tsp = paths([])
	stack = [[src]]
	while len(stack) > 0:
		path = stack.pop()
		v = path[-1]
		g = calc_cost(G,path)
		H = G.to_undirected()
		for i in range(len(path)-1):
			H.remove_edge(path[i],path[i+1])
		h = calc_mst(H)
		for w in nx.all_neighbors(G,v):
			if w not in path:
				next_path = path.copy()
				next_path.append(w);
				if (g+h) > calc_cost(G,next_path):
					stack.append(next_path)
				else:
					break
		
				if len(next_path) == G.number_of_nodes():
					if G.has_edge(next_path[-1],src):
						next_path.append(src)
						cost = calc_cost(G,next_path)
						if tsp.cost == 0.0 or cost < tsp.cost:
							tsp.cost = cost
							tsp.path = next_path
	t2 = datetime.datetime.now()
	print("Time taken by DFBB (hr:min:sec): ", t2-t1)
	return tsp

def a_star(G,src):
	t1 = datetime.datetime.now()
	tsp = paths([])
	open_list = [[src]]
	closed_list =[]
	node_g = []
	node_h = []
	node_f = []

	for i in range(G.number_of_nodes()):
		H = G.to_undirected()
		k = nx.shortest_path(G, source=src, target=i+1, weight='weight', method='dijkstra')
		node_g.append(calc_cost(G,k))
		#print("Path",i,k)
		#for j in range(len(k)-1):
		#		H.remove_edge(k[j],k[j+1])
		for j in range(len(k)):
				H.remove_node(k[j])
		'''
		pos=nx.spring_layout(H)
		nx.draw_networkx(H,pos)
		labels = nx.get_edge_attributes(H,'weight')
		nx.draw_networkx_edge_labels(H,pos,edge_labels=labels)
		plt.show()
		'''		
		node_h.append(calc_mst(H))
	for i in range(G.number_of_nodes()):
		node_f.append(node_g[i] + node_h[i])

	#print("f: ",node_f)
	#print("g: ",node_g)
	#print("h: ",node_h)

	while True:
		if len(open_list) == 0:
			print("Failed.\n")
		else:
			f = 0
			path = open_list[0]
			for i in open_list:
				n = i[-1]
				if ((node_g[n-1]+node_h[n-1]) < f) or f == 0:
					f = node_g[n-1]+node_h[n-1]
					path = i
			if len(path) == G.number_of_nodes():
				if G.has_edge(path[-1],src):
					path.append(src)
					cost = calc_cost(G,path)
					if tsp.cost == 0.0 or cost < tsp.cost:
						tsp.cost = cost
						tsp.path = path
						break
			closed_list.append(path)
			open_list.remove(path)
			v = path[-1]
			for w in nx.all_neighbors(G,v):
				if not w in path:
					flag_o = 0
					flag_c = 0
					for x in open_list:
						if x[-1] == w:
							if node_g[w-1] > node_g[v-1]+G[v][w]['weight']:
								node_g[w-1] = node_g[v-1]+G[v][w]['weight']
								node_f[w-1] = node_g[w-1] + node_h[w-1]
							flag_o = 1
							break
					for x in closed_list:
						if x[-1] == w:
							flag_c = 1
							break
					if flag_c*flag_o == 0:
						node_g[w-1] = node_g[v-1]+G[v][w]['weight']
						node_f[w-1] = node_g[w-1]+node_h[w-1]
						next_path = path.copy()
						next_path.append(w)
						open_list.append(next_path)

	t2 = datetime.datetime.now()
	print("Time taken by A* (hr:min:sec): ", t2-t1)
	return tsp

def sr_alg(G):
	t1 = datetime.datetime.now()
	edge_list = sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1))
	v = G.number_of_nodes()
	e = G.number_of_edges() - v
	for i in range(v):
		edge_list.pop(0)	
	edge_stack = []
	edge_repeat = set()
	checked_list = []
	error_list = []
	explored_list = []
	path_list = []
	tsp = paths([])
	path = []
	func = "1"
	Bound = 0
	for i in range(v):
		Bound = Bound + edge_list[e-i-1][2]['weight']
	print(edge_list)
	while len(edge_list) >= v:
		if func == "1":
			ed = copy.deepcopy(edge_list)
			while len(ed)-len(error_list)-len(edge_stack) > 0 or len(edge_stack) < v:
				print("\n")
				x = ed.pop(0)
				print(x)
				if x not in edge_stack and x not in error_list:
					print("not in path and not in error_list")
					path.append(x)
					
					if path not in explored_list:
						print("path not explored")
						if iscycle(v,path) == False and morethantwo(v,path) == False and cost(path) <= Bound:
							print("Edge added")
							edge_stack.append(x)
							print(edge_stack)
							print("Explored List is ")
							explored_list.append(edge_stack)
							print(explored_list)
							print(cost(path))
						elif iscycle(v,path) == True and len(path) == v and cost(path) <= Bound and not_two(v,path) == False:
							print("Cycle Found!!!")
							edge_stack.append(x)
							explored_list.append(edge_stack)
							path_list.append(edge_stack)
							tsp.path = edge_stack
							tsp.cosr = cost(edge_stack)
							Bound = cost(edge_stack)
							print(edge_stack)
							print("Cost = ",Bound)
							adding_elements = set(edge_stack)
							for i in adding_elements:
								edge_repeat.add(i)
							func = "2"
						elif len(path) == v-1 and (len(ed)-len(error_list)-len(path)) == 0:
							print("Check")
							edge_stack.append(x)
							explored_list.append(edge_stack)
							path_list.append(edge_stack)
						else:
							print("Added in error_list")
							error_list.append(x)
							print("Path before:")
							print(path)
							explored_list.append(path)
							print("Path after;")
							path.pop()
							print(path)
							print("Explored List: ")
							print(explored_list)
					else:
						print("edge removed")
						path.pop()
			if len(ed)-len(error_list)-len(edge_stack) == 0 or len(path) == v:
				func = "2"
		elif func == "2":
			temp = copy.deepcopy(edge_list)		
			while len(edge_stack) > 0:
				checked_list.append(edge_stack.pop())
				path.pop()
				something = temp.pop(0)
				if something not in edge_stack and something not in error_list and something not in checked_list:
					path.append(something)
					if path not in explored_list:
						if iscycle(v,path) == False and morethantwo(v,path) == False and cost(path) <= Bound:
							explored_list.append(path)
							error_list = []
							checked_list = []
							path.pop()
							func = "1"
			if len(edge_stack) == 0:
				edge_list.pop(0)
				error_list = []
				checked_list = []
				func == "3"
			
		elif func == "3":
			edge_repeat.clear()
			func = "1"
	t2 = datetime.datetime.now()
	print("Time taken by New algorithm (hr:min:sec): ", t2-t1)
	return tsp
