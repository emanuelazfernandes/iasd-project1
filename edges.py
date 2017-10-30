def filter_edges(vertex_tl,node_mother,problem):

    outer_str=[]
    inner=node_mother.state.present+node_mother.state.manifest

    if not inner:
        outer_str=[]
        for vertex in problem.v_list:
            outer_str.append(vertex.ide)

    while outer:

        for vertex in inner:
            for conn in vertex.c:
                if conn not in outer_str:
                    outer_str.append(conn)

        outer=[]

        for vertex in vertex_tl:
            if vertex.ide in possible_vertex_conn_str:
                outer.append(vertex)

        combinations_list=generate_combinations(outer)

        outer_out=[]
        for vertex in problem.v_list:
            outer_out.append(vertex)

        for vert in outer:
            for verr in outer_out:
                if vert.ide==verr.ide:
                    outer_out.remove(vert)

	for vert in inner:
            for verr in outer_out:
                if vert.ide==verr.ide:
                    outer_out.remove(vert)

	
	#TEMOS OUTER_OUT

        for vertex_oo in outer_out:
            for conn_oo in vertex_oo.c:
                for vertex_o in outer:
                    for conn_o in vertex_o.c:
                        if conn_oo == conn_o:
                            FOUND PAIR (VERTEX_O and VERTEX_OO
			    GERAR COMBINAÇÕES COM VERT_OO E VERT_O (e outros)

	
