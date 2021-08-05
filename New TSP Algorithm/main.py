from algo import *

choice = 0
while choice < 1 or choice > 2:
	choice = int(input("1. Input TSP file\n2.Load a graph manually\nEnter your choice. "))
	if choice < 1 or choice > 2:
		print("Sorry, choice not recognized! Enter again.")
if choice == 1:
	G = load()
else:
	G = graph()

choice = 0
while choice < 1 or choice > 6:
	print("1. Depth-First Search\n2.Breadth-First Search\n3. Iterative Deepening\n4. DFBB\n5. A*\n6. New Algorithm\n7. Exit")
	choice = int(input("Enter your choice. "))
	if choice < 1 or choice > 6:
		print("Sorry, choice not recognized! Enter again.")
if choice == 1:
	tsp = dfs(G,1)
elif choice == 2:
	tsp = bfs(G,1)
elif choice == 3:
	tsp = ids(G,1)
elif choice == 4:
	tsp = dfbb(G,1)
elif choice == 5:
	tsp = a_star(G,1)
elif choice == 6:
	sr_alg(G)

if choice < 5 and choice > 0:
	print("The shortest path for TSP is : ",tsp.path)
	print("The cost incurred is : ",tsp.cost)

'''
tsp = dfs(G,1)
print("The shortest path for TSP is : ",tsp.path)
print("The cost incurred is : ",tsp.cost)
tsp = bfs(G,1)
print("The shortest path for TSP is : ",tsp.path)
print("The cost incurred is : ",tsp.cost)
tsp = ids(G,1)
print("The shortest path for TSP is : ",tsp.path)
print("The cost incurred is : ",tsp.cost)
tsp = dfbb(G,1)
print("The shortest path for TSP is : ",tsp.path)
print("The cost incurred is : ",tsp.cost)
tsp = a_star(G,1)
print("The shortest path for TSP is : ",tsp.path)
print("The cost incurred is : ",tsp.cost)
'''