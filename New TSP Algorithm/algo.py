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

def edge_cost(G,u,v):
	if G.has_edge(u,v):
		return G[u][v]['weight']
	else:
		return 0

def heuristic(G):
	path = nx.algorithms.approximation.traveling_salesman.christofides(G)
	ub = calc_cost_subs(G,path,1)
	return ub

def calc_cost_subs(G,path,flag=0):
	cost = 0.0
	i = 0
	while i < len(path)-1:
		cost += edge_cost(G,path[i],path[i+1])
		i = i+1
	if flag == 0:
		print(Fore.GREEN +"Found path " + str(path) + " with cost " + str(cost) + ".")
	return cost

def findpath(v,path):
	M = nx.empty_graph(v)
	for i in path:
		w = i[2]['weight']
		M.add_edge(i[0],i[1], weight = w)
	M.remove_node(0)
	return nx.cycle_basis(M)

def iscycle(v,path):
	M = nx.empty_graph(v)
	for i in path:
		w = i[2]['weight']
		M.add_edge(i[0],i[1], weight = w)
	M.remove_node(0)
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
	M.remove_node(0)
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
	M.remove_node(0)
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
	edge_repeat = []
	back_track = []
	checked_list = []
	error_list = []
	explored_list = []
	path_list = []
	repeat = []
	tsp = paths([])
	path = []
	func = "1"
	Bound = 0
	for i in range(v):
		Bound = Bound + edge_list[e-i-1][2]['weight']
	#print(edge_list)
	#Bound = heuristic(G)
	while len(edge_list) >= v:
		if func == "1":
			ed = []
			ed = copy.deepcopy(edge_list)
			while len(ed) != 0 and len(edge_stack) < v:
				x = ed.pop(0)
				if x not in edge_stack and x not in error_list:
					path.append(x)
					if path not in explored_list and path not in path_list:
						if iscycle(v,path) == False and morethantwo(v,path) == False and cost(path) <= Bound:
							print("Edge added from ",x[0],"to ",x[1],"with weight ",x[2]['weight'])
							edge_stack.append(x)
							explored_list.append(copy.deepcopy(edge_stack))
							if len(ed) == 0:
								func = "2"
								break
						elif iscycle(v,path) == True and len(path) == v and cost(path) <= Bound and not_two(v,path) == False:
							print("Edge added from ",x[0],"to ",x[1],"with weight ",x[2]['weight'])
							print("Cycle Found: ",findpath(v,path),", Cost: ",cost(path))
							edge_stack.append(x)
							explored_list.append(copy.deepcopy(edge_stack))
							path_list.append(copy.deepcopy(edge_stack))
							tsp.path = findpath(v,edge_stack)
							tsp.cost = cost(edge_stack)
							Bound = cost(edge_stack)
							for i in edge_stack:
								if i not in edge_repeat:
									edge_repeat.append(copy.deepcopy(i))
							func = "2"
							break
						elif len(path) == v-1 and len(ed) == 0 and cost(path) <= Bound and iscycle(v,path) == False and morethantwo(v,path) == False:
							#print("3rd check")
							edge_stack.append(x)
							explored_list.append(copy.deepcopy(edge_stack))
							path_list.append(copy.deepcopy(edge_stack))
							#print(edge_stack)
							func = "2"
							break
						else:
							#print("Edge from ",x[0],"to ",x[1],"with weight ",x[2]['weight'],"added to error_list")
							error_list.append(x)
							explored_list.append(copy.deepcopy(path))
							path.pop()
							if len(ed) == 0:
								func = "2"
								break
					else:
						print("path already there")
						path.pop()
						if len(ed) == 0:
							func = "2"
							break
			if len(ed) == 0:
				func = "2"
				#if len(ed)-len(error_list)-len(edge_stack) == 0 or len(path) == v:
			#print("Current cost = ",cost(path), "vertex in path = ",len(path))
		elif func == "2":
			#print("Entered Function 2")
				
			while len(edge_stack) > 0:
				temp = copy.deepcopy(edge_list)	
				popped = edge_stack.pop()
				checked_list.append(copy.deepcopy(popped))
				path.pop()
				print("Edge removed from ",popped[0],"to ",popped[1],"with weight ",popped[2]['weight'])
				for i in range(len(temp)):
					something = temp.pop(0)

					#print(something)
					if something not in edge_stack and something not in checked_list and something not in edge_repeat and something not in repeat:
						path.append(something)
						if path not in explored_list and path not in path_list  and path not in back_track:
							if iscycle(v,path) == False and morethantwo(v,path) == False and cost(path) <= Bound:
								
								print("Edge added from ",something[0],"to ",something[1],"with weight ",something[2]['weight'],"\n")
								edge_stack.append(something)
								explored_list.append(copy.deepcopy(edge_stack))
								for i in edge_stack:
									if i not in repeat:
										repeat.append(copy.deepcopy(i))
								error_list = []
								checked_list = []
								func = "1"
								break
							else:
								#print("Edge from ",x[0],"to ",x[1],"with weight ",x[2]['weight'],"added to error_list")
								explored_list.append(copy.deepcopy(path))
								path.pop(-1)
							back_track.append(copy.deepcopy(path))
						else:
							path.pop(-1)
					elif len(edge_stack) == 0 and len(temp) == 0:
						func = "3"
						break
						
				if func == "1":
					break
			if len(edge_stack) == 0:
				func == "3"
			#print("Function 2 Finished")
			
		elif func == "3":
			print("Entered function 3")
			edge_list.pop(0)
			repeat = []
			error_list = []
			checked_list = []
			edge_repeat = []
			print(edge_list)
			func = "1"
			print("Function 3 Finished")
	t2 = datetime.datetime.now()
	print("Time taken by New algorithm (hr:min:sec): ", t2-t1)
	return tsp
