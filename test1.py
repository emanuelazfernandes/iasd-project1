# Group 30:
#    Emanuel Fernandes   66088
#    João Louro          78450
#  
#    Test file for the structures to be used in the project
#  

# Vertices of the graph - aux/redundant, maybe delete
V = {
	'CM': 20.4,
	'DM': 4.3,
	'K': 19.64,
	'K1': 20.6,
	'K2': 19.64,
	'P': 19.7,
	'PM': 7.13,
	'S': 19.64,
	'STM': 7.15,
}


# Edges of the graph - redundant, maybe delete
E = [# maybe change this to ')'? é só para podermos ir adicionando à medida que se lê do ficheiro
	('PM','K1'),
	('K1','CM'),
	('CM','P'),
	('CM','S'),
	('CM','STM'),
	('CM','K'),
	('CM','K2'),
	('',''),
]




'''



G = {
	'EXIT': ['C'],
	'A': ['B', 'D', 'S1', 'S11'],
	'B': ['A', 'C', 'D', 'S2'],
	'C': ['B', 'D', 'S3', 'EXIT'],
	'D': ['A', 'B', 'C', 'S12'],
	'S1': ['A'],
	'S2': ['B'],
	'S3': ['C'],
	'S11': ['A'],
	'S12': ['D'],
}





edges = {
	'CEXIT': 1,
	'EXITC': 1,
	'AB': 1,
	'BA': 1,
	'AD': 1,
	'DA': 1,
	'BC': 1,
	'CB': 1,
	'BD': 1,
	'DB': 1,
	'CD': 1,
	'DC': 1,
	'AS1': 1,
	'S1A': 1,
	'BS2': 1,
	'S2B': 1,
	'CS3': 1,
	'S3C': 1,
	'AS11': 1,
	'S11A': 1,
	'DS12': 1,
	'S12D': 1,
}

casks_list = {
	'Ca': [4, 0],
	'Cb': [4, 0],
	'Cc': [4, 0],
	'Cd': [3, 0],
	'Ce': [4, 0],
	'Cf': [2, 0]
}

# initial stacks composition
stacks_list = {
	'S1': [0, ['Ca', 'Cb']],
	'S2': [1, ['Cc', 'Cd']],
	'S3': [2, ['Ce', 'Cf']],
	'S11': [3, []],
	'S12': [3, []]
}



'''

















'''

def import_dat(dat_file):
	# Function that imports useful information from the .dat file

	graph = {}
	edges = {}
	casks_list = {}
	stacks_list = {}
	
	with open(dat_file, 'r') as f:
		# talvez verificar se o ficheiro tem alguma coisa? se tem os 3 componentes...
		line = f.readline()  

		while(line != ""):
			#print(line)
			#input()
			# verificar que cada linhas está bem definida (dentro da sintaxe)
			if(line[0] == "C"):
				cask_line = line.split()
				#print(cask_line)
				if len(cask_line) == 3:
					x, y, z = cask_line
					casks_list[x] = [int(y), float(z)] # falta levar aqui os espaços e os pontos em conta!!!!!!
			
			elif(line[0] == "S"):
				y = line.split()
				if len(y) >= 2:
					stacks_list[y[0]] = [int(y[1]), []]

					for i in range(2, len(y)):
						stacks_list[y[0]][1].append(y[i])
			elif(line[0] == "E"):
				edge_line = line.split()
				if len(edge_line) == 4:
					x, y, z, w = edge_line
					edges[y + z] = float(w)
					edges[z + y] = float(w)
					if(y in graph):
						graph[y] += [z]
					else:
						graph[y] = [] + [z]
					if(z in graph):
						graph[z] += [y]
					else:
						graph[z] = [] + [y]
			line = f.readline() 

	# adjust stacks free space
	for s in stacks_list:
		if stacks_list[s][1]:
			for sc in range(stacks_list[s][1].__len__()):
				stacks_list[s][0] -= casks_list[stacks_list[s][1][sc]][0]

	#remove casks not stored in a stack from list
	list_casks_stored = []
	for key, value in stacks_list.items():
		for i in range(value[1].__len__()):
			list_casks_stored.append(value[1][i])
	dif_len = abs(list_casks_stored.__len__() - list(casks_list.keys()).__len__())
	for i in range(0, dif_len):
		for k in range(list(casks_list.keys()).__len__()):
			target = list(casks_list.keys())[k]
			if target not in list_casks_stored:
				break
		del casks_list[target]

	#print(graph)
	#print(edges)
	#print(casks_list)
	#print(stacks_list)




	"""
	print("graph = {")
	for n in graph:
		print("\t'" + n + "':", graph[n])
	print("}")

	print("edges = {")
	for e in edges:
		print("\t'" + e + "':", edges[e])
	print("}")

	print("casks_list = {")
	for c in casks_list:
		print("\t'" + c + "':", casks_list[c])
	print("}")

	print("stacks_list = {")
	for s in stacks_list:
		print("\t'" + s + "':", stacks_list[s])
	print("}")
	"""
	

	"""
	

	"""

	return graph, edges, casks_list, stacks_list
	 
'''
"""
def calc_space(s_list, c_list):
	stacks = list(s_list.keys())
	casks = list(s_list.keys())
	for stacks[0:-1] in s_list:
		b = s_list[stacks] #s -> stack na lista de stacks
		if (len(b) > 2):
			space = b[0]
			for b[1:-1] in c_list:
				c = c_list[b]
				space = space - c[1]
	
	return s_list

"""
