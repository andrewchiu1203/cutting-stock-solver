from heavy_stock_solver import *
len_to_fill = 7.4
self_comb_contradict_id_list = [1, 2]
by_similar_len = {}

if self_comb_contradict_id_list != []:
    by_similar_len_extend, tmp = {}, {}
    len_sum = 0
    for k, j in by_similar_len.items():
        by_similar_len_extend[k] = []
        for l in j:
            if l[0][0] in slot_occupied.values() and l[2] not in self_comb_contradict_id_list:
                by_similar_len_extend[k].append(l)
    for value in by_similar_len_extend.values():
        if len(value) != 0:
            for l in value:
                len_sum += l[0][1]
            avg = round(len_sum/len(value), 2)
            tmp[avg] = value
            len_sum = 0
    by_similar_len_extend = tmp
    tmp = []
    for k, v in by_similar_len_extend.items():
        if v == []:
            tmp.append(k)
    for k in tmp:
        del by_similar_len_extend[k]
    len_to_look_extend, comb_to_look_extend = get_avg_group(len_to_fill, by_similar_len_extend, False)
    comb_result_extend, comb_result_comp_extend, max_comb_len_extend = make_combination(original_stock_len, len_to_look_extend, i[0])
    comb_result = comb_result_extend
    comb_result_comp = comb_result_comp_extend
    comb_to_look = comb_to_look_extend
    comb_result_stock_num, comb_result_num, comb_result_id = [], [], []
    for j in comb_result:
        search_finished = False
        for k in comb_to_look:
            for l in k:
                if j == l[0][1]:
                    comb_result_stock_num.append(l[0][0])
                    comb_result_num.append(l[1][1])
                    comb_result_id.append(l[2])
                    search_finished = True
                    break
            if search_finished:
                break