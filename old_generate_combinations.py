# aux function to generate all of the possible launch components combinations
def generate_combinations(v_list, present, problem):
    
    #aqui somos obrigados a fazer isto assim por causa do combinations e sum_w
    list_V = {} # aux dict
    for v in v_list:
        list_V[v.ide] = v.w
        #{'VCM' = 20.4, 'VDM' = ...}
    list_comb = []

    #print("possible combinations: ")#debug
    for k in range(0, list_V.__len__()+1):# +1 para gerar o lançamento vazio
        #print(k, end = ': ')#debug
        comb_aux = list(combinations(list_V.keys(), k))
        for j in range(0, len(comb_aux)): # format it for single list
            sum_weights = float(0)
            for c in comb_aux[j]:
                sum_weights += list_V[c]#sum the weights of the combination, DEIXA FICAR O V, POIS É O DICT ORIGINAL

            list_comb.append((comb_aux[j], sum_weights))
        #print(comb_aux)#debug
        #print(comb_aux.__len__())#debug
        #print()#debug

    #print()#debug
    #print(list_comb)#debug
