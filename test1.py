# Group 30:
#    Emanuel Fernandes   66088
#    João Louro          78450
#  
#    Test file for the structures to be used in the project
#  

### LIBRARIES
from itertools import combinations
from copy import deepcopy



### PRINTING
#print the G list in a more comprehensive manner
def print_G(list_G):
    print('G = {\n NAME |   w    | edges |\tlist_edges')
    print('-----------------------------------------------------------')
    for key, content in list_G.items():
        print('  '+key+':\t('+str(content[0])+',\t   '+str(content[1])+'\t[',end = '')
        for nc in range(0, content[1]):
            if nc == content[1]-1:#para não imprimir a virgula no final
                print("'"+str(content[2][nc])+"'])")
            else:
                print("'"+str(content[2][nc])+"',",end = "")
    print('}\n')

#print the combinations list
def print_comb(list_comb):
    print("List of combinations = {")
    print("  n\tsum_w\tlist_components")
    print("-----------------------------------------")
    for pcn in range(0,list_comb.__len__()):
        print(" ",pcn,end = "")
        print(":\t",end="")
        print("{0:.2f}".format(list_comb[pcn][1]),end = "\t")
        print(list_comb[pcn][0])
    print("} size =",list_comb.__len__(),"\n")



### STRUCTURES GENERATION
#function that generates E_aux
def generate_E_aux(list_V,list_E):
    # Auxiliary edge list for the graph construction
    list_E_aux = {}
    for v in list_V:
        list_E_aux[v] = []
    # populate it
    for (e1,e2) in list_E:
        #print(e1,e2)
        if e2 not in list_E_aux[e1]:
            list_E_aux[e1].append(e2)
        if e1 not in list_E_aux[e2]:
            list_E_aux[e2].append(e1)
        #print(list_E_aux[e1],list_E_aux[e2])
    #print(list_E_aux)
    return list_E_aux

# generation of all the possible launch components combinations
def generate_combinations(list_V):
    list_comb = []
  
    #print("possible combinations: ")#debug
    for k in range(0,list_V.__len__()+1):#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
        #print(k,end = ': ')#debug
        comb_aux = list(combinations(list_V.keys(),k))#DEPOIS MODIFICA AQUI O V, PARA SER UMA LISTA SÓ COM OS QUE NÃO ESTÃO EM ÓRBITA
        for j in range(0,comb_aux.__len__()):#para meter todos na mesma lista...
            sum_weights = 0
            for w in comb_aux[j]:
                sum_weights = sum_weights + list_V[w]#sum the weights of the combination, DEIXA FICAR O V, POIS É O DICT ORIGINAL
            list_comb.append((comb_aux[j],sum_weights))#create tuple and append (list,sum_weight)
        #print(comb_aux)#debug
        #print(comb_aux.__len__())#debug
        #print()#debug
    #print()#debug
  
    #print_comb(list_comb)
    return list_comb



### FILTERS
#função provavelmente inútil......mas deixa ficar como template para quando tiveres de percorrer a lista
#function that removes (del) a component from combinatory list
def filter_component(list_comb,str_comp):
    #print()
    #print("After "+str_comp+" filter:")
    for nc in reversed(range(0,list_comb.__len__())):
        if str_comp in list_comb[nc][0]:
            del(list_comb[nc])
            #nc = nc - 1#poupas 1 ciclo por cada eliminação!!!
    #print(list_comb)
    #print(list_comb.__len__())

#function that filters combinations if at least 1 element will be unconnected in orbit, except the first one
def filter_edges(list_comb,list_E_aux,printmsg = False):
    #mnheh, so far so good, agora tens de ver como fazes para ver se os que vão ser
    #lançados são edges dos que já lá estão em órbita! será que vale a pena, para o 1º, "ser edge do vazio?"
    if printmsg:
        print("*** Applying edges filter: ***\n")
    else:
        print("*** Applying edges filter...", end = "")
    prev_size = list_comb.__len__()
    n_rem = 0
    for cln in reversed(range(0,prev_size)):
        comp_manifest = list_comb[cln][0]
        #print(comp_manifest)
        if comp_manifest.__len__() <= 1:#solução trolha para o lançamento do 1º-pode funcionar se a list_comb que aqui entra, já for "a que vai ficar depois deste lançamento"
            continue
        not_edge = True#se encontrar, passa a false
        for comp_aux_n in range(0,comp_manifest.__len__()):
            comp_aux = comp_manifest[comp_aux_n]
            #print(comp_aux)
            #print()
            for next_comp in comp_manifest[:comp_aux_n]+comp_manifest[comp_aux_n+1:]:
                #print(next_comp)
                if next_comp in list_E_aux[comp_aux]:
                    not_edge = False
                    break#quando encontra, activa a flag e salta para fora para poupar ciclos
                #else:
                #  not_edge = True
                #  break
            #print()
            #chegou ao fim para este comp_aux: se nao encontrou um edge nos restantes, então a flag não foi alterada (False) e agora é remover este manifesto da lista!
            if not_edge:#found one that's not connected to any of the others
                break#saves cycles
            #senão, passa para o comp_aux seguinte, e assim sucessivamente...
        #agora que já verificou todos (comp_aux já foi um de cada OU encontrou um que não tem edge), vem o veredicto
        if not_edge:
            if printmsg:
                print("removing: ", end = '')
                print(list_comb[cln])
            n_rem = n_rem + 1
            del(list_comb[cln])
        #else:
            #print("yeah, all checks out")
        #print("\nNEXT!\n")
    #print("\nremoved a total of",n_rem,"combinations that would put at leaast 1 element unconnected in orbit")
    if printmsg:
        print("\nTotal invalid combinations removed:",n_rem,"out of",prev_size,"\n")
    else:
        print("done. ***\nTotal invalid combinations removed:",n_rem,"out of",prev_size,"\n")

#function that filters list_comb based on available weight
def filter_weight(list_comb, launch_weight):
    for cwn in reversed(range(0,list_comb.__len__())):
        if list_comb[cwn][1] >= launch_weight:
            del(list_comb[cwn])



# mir.txt
# Vertices of the graph
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

# Edges of the graph; depois faz E.append(frominputfile)
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

'''
# trivial1.txt
V = {
    '1': float(17),
    '2': float(11),
    '3': float(23),
}
E = [
    ('1','2'),
    ('3','2'),
]
'''


# More comprehensive edges list
E_aux = generate_E_aux(V,E)

# Graph creation - ESTA LISTA VAI SER NECESSÁRIA?!?!?!?!?!?!?!
G = {}
for g in V:
    G[g] = (V[g], E_aux[g].__len__(), E_aux[g])
    # G = {'comp_name':(weight_comp, number_edges, list_edges_from_E_aux)}
#print(G)
#print()

print_G(G)
'''
G = {
 NAME |   w    | edges |  list_edges
-----------------------------------------------------------
  CM: (20.4,     6  ['K1','P','S','STM','K','K2'])
  DM: (4.3,    1  ['K'])
  K:  (19.64,    2  ['CM','DM'])
  K1: (20.6,     2  ['PM','CM'])
  K2: (19.64,    1  ['CM'])
  P:  (19.7,     1  ['CM'])
  PM: (7.13,     1  ['K1'])
  S:  (19.64,    1  ['CM'])
  STM:  (7.15,     1  ['CM'])
}
'''



#generate combinations list
comb = generate_combinations(V)
#print - debug
#print_comb(comb)



# agora vamos remover os que, caso sejam enviados, vão ficar desconectados...
#print("Starting edge filter:")
#filter_edges(comb,E_aux,True)
filter_edges(comb,E_aux)
print("\n*** After edge filter: ***\n")
#print_comb(comb)



#max_weight = float(22.8)#L1, L2, L5, L7, L8
#max_weight = float(140)#L3
#max_weight = float(70)#L4
#max_weight = float(250)#L6
#max_weight = float(23)#L9
#max_weight = float(115)#L10

#filter_weight(comb,max_weight)
#print("*** After weight fillter ("+"{0:.2f}".format(max_weight)+"): ***\n")
#print_comb(comb)



#TEACHER SOLUTION - mir.txt
#L8
max_weight = float(22.8)
comb8 = deepcopy(comb);
filter_weight(comb8,max_weight)
print("L8: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb8)
print()
print()

#L9
max_weight = float(23)
comb9 = deepcopy(comb);
filter_component(comb9,'K1')
comb10 = deepcopy(comb9);
filter_weight(comb9,max_weight)
print("L9: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb9)
print()
print()

#L10
max_weight = float(115)
#print_comb(comb10)
filter_component(comb10,'CM')
filter_weight(comb10,max_weight)
print("L10: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb10)
print()
print()

'''
#TEACHER SOLUTION - trivial1.txt
#L1
max_weight = float(24)
comb1 = deepcopy(comb);
filter_weight(comb1,max_weight)
print("L1: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb1)
print()
print()

#L2
max_weight = float(20)
comb2 = deepcopy(comb);
filter_component(comb2,'3')
comb3 = deepcopy(comb2);
filter_weight(comb2,max_weight)
print("L2: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb2)
print()
print()

#L3
max_weight = float(20)
#print_comb(comb3)
filter_component(comb3,'2')
filter_weight(comb3,max_weight)
print("L3: after weight fillter ("+"{0:.2f}".format(max_weight)+"):\n")
print_comb(comb3)
print()
print()
'''



#pronto, até aqui está a aplicar os 2 filtros bem:
# edges - caso leve pelo menos 1 (que não o 1.º) que vá ficar sozinho;
# weight - caso o peso ultrapasse o max_payload

#falta:
# - verificar que o filter_edges está a remover todos os que é suposto (já verifiquei que os que remove, pelo menos esses está bem)
# - optimizar talvez essa função
# - ver como faço para as gerações seguinte: descomento aquela função lá em cima para remover o/os que já estiverem em órbita, tendo de fazer deepcopy para cada node (!) ou gero uma nova lista de combinações para cada node (!) ?????
# - meter o filter_edges a receber uma lista que é "o que vai ficar em órbita"
# - fazer a lista (ou estrutura) do node (launch)



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























