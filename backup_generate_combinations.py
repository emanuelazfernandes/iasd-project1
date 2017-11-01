# aux function to generate all of the possible launch components combinations
def generate_combinations(v_list, present, problem):
#######################################################       início do novo generate_combinations()

    list_V = {} # aux dict: #{'VCM' = 20.4, 'VDM' = ...}
    for v in v_list:
        list_V[v.ide] = v.w

    list_comb = []
    list_comb.append(([],0))# adicionamos manualmente o lançamento vazio

    if present:
        #fazer agora o mesmo, mas usando os que já estao no present, e no fim retirar isso de cada comb gerada com eles (E O PESO!!!)
        #for vp in present:
        #    vp_ide = vp.ide
        print("not yet (for present)!")

    else:
        #sem nada lá em cima
        for v in v_list:
            #gerar todas as combinações para este vertex (v.ide = 'VDM'), enquanto houver edges não explorados!
            aux = [v.ide]
            edges = return_edges(problem, v.ide)
            #percorrer agora o edges para gerar todas as combinações 2 a 2 com esse(s), 1 a 1, 3 a 3, etc...
            for k in range(1, len(problem.v_list)+1):#como não está la nada, usamos aqui o problem.v_list; depois para o outro caso, usar só o v_list, pois já só contem a quantidade de vertex que podem ser lançados, (acho que) não precisamos de andar a gerar cenas a mais

        ##sem nada lá em cima
        ##percorrer agora o edges para gerar todas as combinações 2 a 2 com esse(s), 1 a 1, 3 a 3, etc...
        #for k in range(1, len(problem.v_list)+1):#como não está la nada, usamos aqui o problem.v_list; depois para o outro caso, usar só o v_list, pois já só contem a quantidade de vertex que podem ser lançados, (acho que) não precisamos de andar a gerar cenas a mais
        #    for v in v_list:
        #        #gerar todas as combinações para este vertex (v.ide = 'VDM'), enquanto houver edges não explorados!
        #        aux = [v.ide]
        #        edges = return_edges(problem, v.ide)

                if k == 1:#fazer para 1 a 1
                    comb = [v.ide]#comb = ['VDM']
                    sum_w = list_V[v.ide]#sum_w = 4.3
                    comb_tup = (comb, sum_w)#comb_tup = (['VDM'],4.3)
                    list_comb.append(comb_tup)
                    #print_comb(list_comb)
                    #print("k =",k)
                    #input()

                if k == 2:#fazer para 2 a 2
                    for edge in edges:#edge = 'VK'
                        comb = [v.ide, edge]#comb = ['VDM','VK']
                        if comb_present(comb, list_comb):
                            #print("ups, esta já existe:", end = '')
                            #print(comb)
                            #input()
                            continue
                        sum_w = float(0)
                        for cw in comb:
                            sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                        comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                        list_comb.append(comb_tup)
                        #print_comb(list_comb)
                        #print("k =",k)
                        #input()

                if k == 3:
                    for edge in edges:#edge = 'VK'
                        aux = [v.ide, edge]
                        for current_v in aux:#procurar os edges, para cada membro do aux!
                            new_edges = return_edges(problem, current_v)#new_edges = ['VCM','VDM']
                            for new_edge in new_edges:
                                if new_edge in aux:
                                    #print("ups, este está repetido:")
                                    #print("new_edge =", new_edge)
                                    #print("aux =", aux)
                                    #input()
                                    continue
                                comb = copy.copy(aux)#shallow copy
                                comb.append(new_edge)
                                #print("comb =", comb)
                                #print("new_edge =", new_edge)
                                #print("aux =", aux)
                                ##input()
                                if comb_present(comb, list_comb):
                                    #print("ups, esta já existe:", end = '')
                                    #print(comb)
                                    #input()
                                    continue
                                sum_w = float(0)
                                for cw in comb:
                                    sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                                comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                                list_comb.append(comb_tup)
                                #print_comb(list_comb)
                                #print("k =",k)
                                #input()
                    print_comb(list_comb)
                    print("fim do 3, k =",k)
                    input()


                #independentemente do k:





    '''
                if k == 4:
                    for edge in edges:#edge = 'VK'
                        if edge in aux:
                            print("aux =", aux, "|", "edge =", edge)
                            print("oi?!")
                            input()
                            continue

                        aux2 = copy.copy(aux)#shallow copy
                        aux2.append(edge)

                        print("aux2 =", aux2)
                        input()

                        for current_v in aux2:#procurar os edges, para cada membro do aux!
                            new_edges = return_edges(problem, current_v)#new_edges = ['VCM','VDM']
                            for new_edge in new_edges:
                                #recursivo a partir daqui...


                                if new_edge in aux2:
                                    print("ups, este está repetido:")
                                    print("new_edge =", new_edge)
                                    print("aux2 =", aux2)
                                    input()
                                    continue
                                comb = copy.copy(aux2)#shallow copy
                                comb.append(new_edge)
                                print("comb =", comb)
                                print("new_edge =", new_edge)
                                print("aux2 =", aux2)
                                #input()
                                if comb_present(comb, list_comb):
                                    print("ups, esta já existe:", end = '')
                                    print(comb)
                                    input()
                                    continue
                                sum_w = float(0)
                                for cw in comb:
                                    sum_w += list_V[cw]#sum_w = 4.3 + 19.64 = 23.94
                                comb_tup = (comb, sum_w)#comb_tup = (['VDM','VK'],23.94)
                                list_comb.append(comb_tup)
                                print_comb(list_comb)
                                print("k =",k)
                                input()
    '''
    #agora que geramos, vamos eliminar repetidas!
    print_comb(list_comb)
    print("chegamos ao fim!")
    input()
    input()
    input()
    input()
    input()

    return list_comb



def return_edges(problem, vertex_str):#vertex: vertex.ide = 'VDM'
    for ve in problem.v_list:#vamos ver agora todos os vizinhos do 'VDM'
        if ve.ide == vertex_str:
            edges = ve.c#edges tem agora uma lista de string com os vizinhos de VDM: ['VK']
            break#já encontramos; poupar ciclos
    return edges

def comb_present(comb, list_comb):
    is_present = False
    for comb_aux_tup in list_comb:
        comb_aux = comb_aux_tup[0]
        if sorted(comb) == sorted(comb_aux):
            is_present = True
            break
    #se não encontrou retorna False; se encontrou retorna True
    return is_present