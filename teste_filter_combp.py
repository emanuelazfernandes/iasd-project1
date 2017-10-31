def filter_combinations(con_list, vertex_tl, node_mother, problem):

    for c_tup in con_list:
        #c_tup = (['VK','VP','VS'],6.9)
        comb = c_tup[0]
        #comb tem agora a lista de strings desta combinação => ['VK','VP','VS']
        if len(comb) < 2:
            continue#só estamos interessados em eliminar aqueles que têm pelo menos 2 componentes, pois o objectivo aqui é verificar se vão ficar conectados no espaço...
        for n_vide in range(0, len(comb)):
            vide = comb[n_vide]
            #vide contem agora o v.ide da comb => 'VK'
            for v_orig in problem.v_list:#procurar os edges do VK
                if v_orig.ide == vide:
                    edges = v_orig.c
            #edges contem agora ['VCM','VDM'], uma lista de strings!!!
            comb_others = comb[:n_vide] + comb[n_vide+1:]
            #comb_others contem agora todos os outros da comb que não o vide => ['VP','VS']

            present = node_mother.state.present
            manifest = node_mother.state.manifest
            outer_ring = []

            for vp in present:#present = ['VK1','VCM'], vp.ide = 'VK1'
                for vpe in vp.c:#vp.c = ['VPM','VCM']
                    if vpe in present:
                        continue#ignorar os companheiros de "inner ring"
                    if vpe == vp:#estava aqui
                        outer_ring.append(vpe)
            #outer_ring agora contem todas as ligações de 1º nivel

            for vtl in vertex_tl:
                


            for co in comb_others:
                if co not in edges:
                    

    #percorrer as combinações 1 por 1, e ver se há pelo menos 1 desconexão!
    #se houver, essa combinação salta fora!


'''
    print(con_list)

    possible_vertex_conn_str = []

    vertex_in_space = node_mother.state.present + node_mother.state.manifest
    for v in vertex_in_space:
        print("     ", v.ide, end = "")
    print("caralho")

    for vertex in vertex_in_space:
        for conn in vertex.c:
            if conn not in possible_vertex_conn_str:
                possible_vertex_conn_str.append(conn)
    print(possible_vertex_conn_str)

    if not vertex_in_space:
        possible_vertex_conn_str=[]
        for vertex in problem.v_list:
            possible_vertex_conn_str.append(vertex.ide)
    print(possible_vertex_conn_str)

    for combi in con_list:
        if len(combi[0])==1:
            if combi[0] not in possible_vertex_conn_str:
                con_list.remove(combi)
    print(con_list)
    input()
    #até aqui, já filtrou .....

    #for 

    return con_list
'''