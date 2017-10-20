# Group 30:
#    Emanuel Fernandes   66088
#    João Louro          78450
#  
#    Test file for the structures to be used in the project
#  

'''função provavelmente inútil......mas deixa ficar como template para quando tiveres de percorrer a lista
#function that removes (del) a component from combinatory list
def filter_component(list_comb,str_comp):
  
  print()
  print("After "+str_comp+" filter:")
  
  for nc in reversed(range(0,list_comb.__len__())):
    if str_comp in list_comb[nc]:
      del(list_comb[nc])
      nc = nc - 1#poupas 1 ciclo por cada eliminação!!!
  
  print(list_comb)
  print(list_comb.__len__())
'''

def filter_weight(list_comb, launch_weight):
  for cwn in reversed(range(0,comb.__len__())):
    if list_comb[cwn][1] >= launch_weight:
      del(list_comb[cwn])






from itertools import combinations
#from copy import deepcopy

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

# Graph creation - ESTA LISTA VAI SER NECESSÁRIA?!?!?!?!?!?!?! se sim, depois para remover cenas, vais ter de recorrer ao deepcopy..
G = {}

for g in V:
  G[g] = (V[g], E_aux[g].__len__(), E_aux[g])
	# G = {'comp_name':(weight_comp, number_edges, list_edges_from_E_aux)}
#print(G)
#print()
#'''
#print the G list in a more comprehensive manner
print('G = {\n NAME |   w    | edges |\tlist_edges')
print('-----------------------------------------------------------')
for key, content in G.items():
  print('  '+key+':\t('+str(content[0])+',\t   '+str(content[1])+'\t[',end = '')
  for nc in range(0, content[1]):
    if nc == content[1]-1:#para não imprimir a virgula no final
      print("'"+str(content[2][nc])+"'])")
    else:
      print("'"+str(content[2][nc])+"',",end = "")
print('}\n')
#'''





#METE ISTO NUMA FUNÇÃO, PORQUE VAI SER UTILIZADA SEMPRE QUE
#QUISERMOS GERAR AS COMBINAÇÕES DOS QUE *NÃO* ESTÃO EM ÓRBITA

# generation of all the possible launch components combinations
comb = []

#print("possible combinations: ")#debug
for k in range(0,V.__len__()+1):#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
  #print(k,end = ': ')#debug
  comb_aux = list(combinations(V.keys(),k))#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
  for j in range(0,comb_aux.__len__()):#para meter todos na mesma lista...
    sum_weights = 0
    for w in comb_aux[j]:
      sum_weights = sum_weights + V[w]#sum the weights of the combination, DEIXA FICAR O V, POIS É O DICT ORIGINAL
    comb.append((comb_aux[j],sum_weights))
  #print(comb_aux)#debug
  #print(comb_aux.__len__())#debug
  #print()#debug
#print()#debug

print(comb)
print(comb.__len__())
print()








# agora vamos remover os que, caso sejam enviados, vão ficar desconectados...
#print("Starting edge filter:")


#FrItArIa
#vá lá que os edges só contêm 2 elementos, assim no if só tens de testar 2 condições (ordem do edge)




#mnheh, so far so good, agora tens de ver como fazes para ver se os que vão ser
#lançados são edges dos que já lá estão em órbita! será que vale a pena, para o 1º, "ser edge do vazio?"
for cln in reversed(range(0,comb.__len__())):
	comp_manifest = comb[cln][0]
	print(comp_manifest)
	if comp_manifest.__len__() <= 1:
	  continue
	not_edge = True#se encontrar, passa a false
	for comp_aux_n in range(0,comp_manifest.__len__()):
		comp_aux = comp_manifest[comp_aux_n]
		print(comp_aux)
		#print()
		for next_comp in comp_manifest[:comp_aux_n]+comp_manifest[comp_aux_n+1:]:
		  print(next_comp)
		  if next_comp in E_aux[comp_aux]:
			  not_edge = False
			  break#quando encontra, activa a flag e salta para fora para poupar ciclos
			#else:
			#  not_edge = True
			#  break
		print()
		#chegou ao fim: se nao encontrou, então a flag não foi alterada (False) e agora é remover este da lista!
		if not_edge:#found one that's not connected to any of the others
		  break#saves cycles
	if not_edge:
	  print("removingggggggggggggggggggggg: ", end = '')
	  print(comb[cln])
	  del(comb[cln])
	else:
	  print("yeah, all checks out")
	print("\nNEXT!\n")

print("After edge filter:")
print(comb)
print(comb.__len__())
print()






filter_weight(comb,30.0)

print("After weight fillter:")
print(comb)
print(comb.__len__())
print()










'''
print()
print()

a = ("lol","pois","e","agora","crl")

print(a)
print()

for b in range(0,a.__len__()):
  print(b)
  c = a[b]
  print(c)
  print()
  for d in a[:b]+a[b+1:]:
    print(d)
  print()
  print()
'''


