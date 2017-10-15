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
	('K','DM'),
]
# E.append(frominputfile)

# Auxiliary edge list for the graph construction
E_aux = {}
for v in V:
	E_aux[v] = []

# populate it
for (e1,e2) in E:
	#print(e1,e2)

	if e2 not in E_aux[e1]:
		E_aux[e1].append(e2)
	if e1 not in E_aux[e2]:
		E_aux[e2].append(e1)

	#print(E_aux[e1],E_aux[e2])
#print(E_aux)

# Graph creation
G = {}

for g in V:
	G[g] = (V[g], E_aux[g].__len__(), E_aux[g])
	# G = {'comp_name':(weight_comp, number_edges, list_edges_from_E_aux)}
print(G)
