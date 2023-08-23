import math, copy, itertools, random
from operator import itemgetter

required_length = []
required_number = []
slot_range = {}
combined_slot_range = {}
original_stock_len = 0
machine_max_throughput = 0
wanted_spare_len = {}
wanted_spare_len = {}
wanted_spare_range = []
slot_occupied = {}
result, spare_result = [], {}
total_input_len, total_waste_len, order_total_len= 0, 0, 0
use_wanted_spare = True

def to_use_wanted_spare(_use_wanted_spare):
    global use_wanted_spare
    use_wanted_spare =_use_wanted_spare

def set_required_length(_required_length):
    global required_length
    required_length = _required_length

def set_required_number(_required_number):
    global required_number
    required_number = _required_number

def set_slot_range(_slot_range):
    global slot_range
    slot_range = _slot_range

def set_combined_slot_range(_combined_slot_range):
    global combined_slot_range
    combined_slot_range = _combined_slot_range

def set_original_stock_len(_original_stock_len):
    global original_stock_len
    original_stock_len = _original_stock_len

def set_machine_max_throughput(_machine_max_throughput):
    global machine_max_throughput
    machine_max_throughput = _machine_max_throughput

def set_wanted_spare_len(_wanted_spare_len):
    global wanted_spare_len
    wanted_spare_len = _wanted_spare_len

def set_wanted_spare_range(_wanted_spare_range):
    global wanted_spare_range
    wanted_spare_range = _wanted_spare_range

def init_slot_occupied(_slot_occupied):
    global slot_occupied
    slot_occupied = _slot_occupied

def make_group(_required_length, _required_number, _original_stock_len):
    required_length = _required_length
    required_number = _required_number
    original_stock_len = _original_stock_len
    tmp, by_similar_len, by_stock_num = [], {}, {}

    # Add length and num into 1 list
    for i in range(len(required_length)):
        tmp.append([required_length[i], required_number[i], i])

        try:
            by_stock_num[required_length[i][0]] = by_stock_num[required_length[i][0]]
        except:
            by_stock_num[required_length[i][0]] = []
            by_stock_num[required_length[i][0]].append(
                [required_length[i][1], required_number[i][1], i])
        else:
            by_stock_num[required_length[i][0]].append(
                [required_length[i][1], required_number[i][1], i])

    # Group them into dict with each item's whole number part as key
    for i in range(1, original_stock_len + 1):
        by_similar_len[i] = []
        for j in tmp:
            if i <= j[0][1] < i + 1:
                by_similar_len[i].append(j)
        
        if len(by_similar_len[i]) == 0:
            del by_similar_len[i]

    # Replace the key with the avg of every len in each item
    tmp = {}
    len_sum = 0

    for value in by_similar_len.values():
        for i in value:
            len_sum += i[0][1]
        avg = round(len_sum/len(value), 2)
        tmp[avg] = value
        len_sum = 0
    
    by_similar_len = tmp

    return by_stock_num, by_similar_len

def make_combination(_len_to_fill, _comb_list, _base_len, threshold = 5, neg_offset = 0.03, pos_offset = 0.05):
    comb_list = _comb_list
    len_to_fill = _len_to_fill
    base_len = _base_len
    comb = list(itertools.product(*comb_list))
    comb_sum, compensated = [], []

    for i in comb:
        comb_sum.append([sum(i), i])
    comb_sum.sort(key=itemgetter(0), reverse=True)

    for i in comb_sum:
        if round(i[0] + base_len, 4) == len_to_fill:
            return list(i[1]), list(i[1])+[base_len], len_to_fill
        
        elif round(i[0] + base_len, 4) > len_to_fill:
            num_len_gt_than_threshold = 0
            for j in i[1]:
                if j >= threshold:
                    num_len_gt_than_threshold += 1
            if base_len >= threshold:
                num_len_gt_than_threshold += 1

            off_set = neg_offset * num_len_gt_than_threshold

            if i[0] + base_len - off_set <= len_to_fill:
                avg_offset = round((i[0] + base_len - len_to_fill) / num_len_gt_than_threshold, 2)
                for j in i[1]:
                    if j >= threshold:
                        compensated.append(round(j - avg_offset, 2))
                    else:
                        compensated.append(j)

                if base_len >= threshold:
                    compensated += [round(base_len - avg_offset, 2)]
                else:
                    compensated += [round(base_len, 2)]

                return list(i[1]), compensated, sum(compensated)
            
        elif round(i[0] + base_len, 4) < len_to_fill:
            num_len_gt_than_threshold = 0
            for j in i[1]:
                if j >= threshold:
                    num_len_gt_than_threshold += 1
            if base_len >= threshold:
                num_len_gt_than_threshold += 1

            off_set = pos_offset * num_len_gt_than_threshold

            if i[0] + base_len + off_set >= len_to_fill:
                avg_offset = round((len_to_fill - i[0] - base_len) / num_len_gt_than_threshold, 2)
                for j in i[1]:
                    if j >= threshold:
                        compensated.append(round(j + avg_offset, 2))
                    else:
                        compensated.append(j)
                
                if base_len >= threshold:
                    compensated += [round(base_len + avg_offset, 2)]
                else:
                    compensated += [round(base_len, 2)]

                return list(i[1]), compensated, sum(compensated)
        
    compensated = []
    for i in comb_sum:
        if i[0] < round(len_to_fill - base_len, 4):
            num_len_gt_than_threshold = 0
            for j in i[1]:
                if j >= threshold:
                    num_len_gt_than_threshold += 1
            if base_len >= threshold:
                    num_len_gt_than_threshold += 1

            if num_len_gt_than_threshold == 0:
                    return list(i[1]), list(i[1])+[base_len], i[0] + base_len

            avg_offset = round((len_to_fill - i[0] - base_len) / num_len_gt_than_threshold, 2)
            if avg_offset > pos_offset:
                avg_offset = pos_offset

            for j in i[1]:
                if j >= threshold:
                    compensated.append(round(j + avg_offset, 2))
                else:
                    compensated.append(j)
                
            if base_len >= threshold:
                compensated += [round(base_len + avg_offset, 2)]
            else:
                compensated += [round(base_len, 2)]
            
            return list(i[1]), compensated, sum(compensated)
    
    return list(i[1]), list(i[1])+[base_len], i[0] + base_len

def get_avg_group(_len_to_fill, _by_similar_len, r = 3, len_repeated_max = 2, repeat_comb = True): 
    len_to_fill = _len_to_fill
    by_similar_len = _by_similar_len
    tmp, len_to_look, comb_to_look = [], [], []
    val = copy.deepcopy(list(by_similar_len.keys()))

    # Repeat avg in the basket several times when possible
    if repeat_comb:
        for j in val:
            if len_to_fill // j > 1:
                n = int(len_to_fill // j)
                if n > len_repeated_max:
                    n = 2
                for k in range(n):
                    tmp.append(j)
        val += tmp
    val.sort()

    max_comb_under_current_repeat_max = []

    if len(val) < 4:
        r = len(val)

    for i in range(1, r + 1):
        limited_comb_list = []
        comb = itertools.combinations(val, i)
        for j in comb:
            if sum(j) <= len_to_fill:
                limited_comb_list.append([j, sum(j)])
        limited_comb_list.sort(key = itemgetter(1), reverse= True)
        try:
            max_comb_under_current_repeat_max.append(limited_comb_list[0])
        except:
            pass

    max_comb_under_current_repeat_max.sort(key = itemgetter(1), reverse= True)
    try:
        combination = list(max_comb_under_current_repeat_max[0][0])
    except:
        combination = []

    for j in combination:
        comb_to_look.append(by_similar_len[j])
    
    for j in comb_to_look:
        tmp1 = []
        for k in j:
            tmp1.append(k[0][1])

        len_to_look.append(tmp1)
    
    return len_to_look, comb_to_look

def get_slot_of_stock_num(_stock_num, _by_stock_num, _id = None):
    stock_num = copy.deepcopy(_stock_num)
    by_stock_num = _by_stock_num
    current_stock_len_list = []
    slot = []
    id = _id

    try:
        for i in by_stock_num[stock_num]:
            current_stock_len_list.append(i[0])
            max_len_of_current_stock = max(current_stock_len_list)
            min_len_of_current_stock = min(current_stock_len_list)
    except:
        max_len_of_current_stock = wanted_spare_len[id]
        min_len_of_current_stock = wanted_spare_len[id]

    already_occupied = False
    for k, v in slot_occupied.items():
        if id == None:
            if v == stock_num:
                slot.append(k)
                already_occupied = True
        else:
            if v == id:
                slot.append(k)
                already_occupied = True

    if not already_occupied:
        for k, v in slot_range.items():
            if slot_occupied[k] == 0:
                if min_len_of_current_stock >= v[0] and max_len_of_current_stock <= v[1]:
                    slot.append(k)
                    break
    
    if len(slot) == 0:
        for k, v in slot_range.items():
            if min_len_of_current_stock >= v[0] and max_len_of_current_stock <= v[1]:
                slot.append(k)
                break

    if len(slot) == 0:
        for k, v in combined_slot_range.items():
            min_list = []
            min_list.append(slot_range[k][0])
            min_list.append(slot_range[v][0])
            min_limit = min(min_list)
            max_limit = slot_range[k][1] +  slot_range[v][1]

            if min_len_of_current_stock >= min_limit and max_len_of_current_stock <= max_limit:
                slot.append(k)
                slot.append(v)
                break

    if slot == []:
        print("No applicable slot room for stock #{}".format(stock_num))
        quit()

    return slot

def get_Xn(_comb_result, _comb_result_stock_num, _comb_result_num, _comb_result_id):
    comb_result = _comb_result
    comb_result_stock_num = _comb_result_stock_num
    comb_result_num = _comb_result_num
    comb_result_id = _comb_result_id

    x, x_id_and_index, Xn = [], {}, []
    for j in range(len(comb_result)):
        try:
            x_id_and_index[comb_result_id[j]]
        except:
            x.append(1)
            x_id_and_index[comb_result_id[j]] = j
        else:
            x.append(0)
            x[x_id_and_index[comb_result_id[j]]] += 1
    
    tmp = []
    for j in range(len(comb_result)):
        try:
            tmp.append(comb_result_num[j] // x[j])
        except:
            pass
    xn = sorted(tmp)[0]
    if xn > machine_max_throughput:
                xn = machine_max_throughput
    if xn == 0:
        xn = 1

    for j in range(len(x)):
        if x[j] != 0:
            remain = comb_result_num[j] - x[j] * xn
            Xn.append([comb_result_stock_num[j], comb_result_id[j], remain, abs(xn)])
    
    return Xn

def update_by_stock_num_and_by_similar_length(_by_stock_num, _by_similar_len, _Xn):
    by_stock_num = _by_stock_num
    by_similar_len = _by_similar_len
    Xn = _Xn

    for j in range(len(Xn)):
        if Xn[j][0] != -1:
            for k in by_stock_num[Xn[j][0]]:
                if k[2] == Xn[j][1]:
                    current_len = k[0]
                    k[1] = Xn[j][2]
                    break
            
            tmp = {}
            for avg, group in by_similar_len.items():
                if math.floor(avg) == math.floor(current_len):
                    tmp[avg] = []
                    for k in range(len(group)):
                        if group[k][2] == Xn[j][1]:
                            if Xn[j][2] > 0:
                                group[k][1][1] = Xn[j][2]
                                tmp[avg].append(group[k])
                        else:
                            tmp[avg].append(group[k])
                else:
                    tmp[avg] = group
                
                if len(tmp[avg]) == 0:
                    del tmp[avg]
            
            by_similar_len = tmp

            tmp = {}
            len_sum = 0

            for value in by_similar_len.values():
                for i in value:
                    len_sum += i[0][1]
                avg = round(len_sum/len(value), 2)
                tmp[avg] = value
                len_sum = 0
            
            by_similar_len = tmp
    
    return by_stock_num, by_similar_len

def update_spare_result(_comb_result, _comb_result_id, _Xn, _spare_result):
    comb_result = _comb_result
    comb_result_id = _comb_result_id
    spare_result = _spare_result
    Xn = _Xn
    len_sum = 0

    for i in range(len(comb_result)):
        if comb_result_id[i] < 0:
            try:
                spare_result[comb_result[i]]
            except:
                spare_result[comb_result[i]] = Xn[0][3]
            else:
                spare_result[comb_result[i]] += Xn[0][3]
        len_sum += comb_result[i]
    
    return spare_result

def process_slot_and_spare_info():
    global slot_range

    for k, v in slot_range.items():
        slot_range[k].append(round(abs(slot_range[k][1] - slot_range[k][0]), 2))
    slot_range = dict(sorted(slot_range.items(), key=lambda item: item[1][2]))
    if wanted_spare_len == {}:
        wanted_spare_len[-1] = wanted_spare_range[0]
        wanted_spare_len[-2] = round(wanted_spare_len[-1] + ((wanted_spare_range[1] - wanted_spare_range[0])/3), 2)
        wanted_spare_len[-3] = round(wanted_spare_len[-2] + ((wanted_spare_range[1] - wanted_spare_range[0])/3), 2)
        wanted_spare_len[-4] = wanted_spare_range[1]

def display_result():
    total_wanted_spare_len = 0
    for k, v in spare_result.items():
        total_wanted_spare_len += round(k * v, 2)
        total_wanted_spare_len = round(total_wanted_spare_len, 2)

    print("Designated spare:")
    print(spare_result)
    print()
    print("Total input stock: ", total_input_len)
    print("Order total length:", order_total_len)
    print("Total waste tock:  ", round(total_waste_len, 2))
    print("Total spare len:   ", total_wanted_spare_len)
    print("Waste perc:        ", round(total_waste_len/total_input_len * 100, 2), "%")
    print("Spare perc:        ", round(total_wanted_spare_len/total_input_len * 100, 2), "%")

    all_slot_cleared = True
    for c in slot_occupied.values():
        if c != 0:
            all_slot_cleared = False
            break
    print("All slots cleared: ", all_slot_cleared)

def _solve():
    process_slot_and_spare_info()

    global combined_slot_range, wanted_spare_len, wanted_spare_range, slot_occupied, \
           result, spare_result, total_input_len, total_waste_len, order_total_len, use_wanted_spare
    
    by_stock_num, by_similar_len = make_group(required_length, required_number, original_stock_len)
    
    for stock_num, combs in by_stock_num.items():
        for c in combs:
            order_total_len += c[0] * c[1]
    order_total_len = round(order_total_len, 2)

    max_loop_count = 1000
    for main_loop_count in range(max_loop_count):
        # prev_by_similar_len = copy.deepcopy(by_similar_len)
        for key, value in by_stock_num.items(): # key is stock num, value is comb

            slot = get_slot_of_stock_num(key, by_stock_num)

            has_room = True
            tmp = copy.deepcopy(slot_occupied)
            for s in slot:
                if slot_occupied[s] == key or slot_occupied[s] == 0:
                    tmp[s] = key
                else:
                    has_room = False
            if has_room:
                slot_occupied = tmp
            else:
                continue

            for i in value:
                # If remain num is 0, it's finished
                if i[1] == 0:
                    continue
                
                # Fill by_similar_len with spare
                len_to_fill = original_stock_len - i[0]
                by_similar_len_extend = copy.deepcopy(by_similar_len)

                if use_wanted_spare == 1:
                    for k, j in wanted_spare_len.items():
                        try:
                            by_similar_len_extend[j] = by_similar_len_extend[j]
                        except:
                            # Stock num & id negative means its wanted spare
                            by_similar_len_extend[j] = [[[-1, j], [-1, 1000000000], k]]

                len_to_look, comb_to_look = get_avg_group(
                    len_to_fill, by_similar_len_extend)
                comb_result, comb_result_comp, max_comb_len = make_combination(
                    original_stock_len, len_to_look, i[0])

                # Fill comb_result paral list
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
                
                # See if there's room in slots
                has_room= True
                tmp = copy.deepcopy(slot_occupied) 
                for j in range(len(comb_result_stock_num)):
                    dealing_spare = False
                    if comb_result_id[j] >= 0:
                        pair_slot = get_slot_of_stock_num(comb_result_stock_num[j], by_stock_num)
                    else:
                        pair_slot = get_slot_of_stock_num(comb_result_stock_num[j], by_stock_num, comb_result_id[j])
                        dealing_spare = True

                    for p in pair_slot:
                        if slot_occupied[p] == 0 or slot_occupied[p] == comb_result_stock_num[j] or slot_occupied[p] == comb_result_id[j]:
                            if dealing_spare:
                                tmp[p] = comb_result_id[j]
                            else:
                                tmp[p] = comb_result_stock_num[j]
                        else:
                            has_room = False
                            break
                    if not has_room:
                        break
                
                if has_room:
                    slot_occupied = tmp

                if not has_room:
                    # Force use stock in slots to make comb
                    by_similar_len_extend, tmp = {}, {}
                    len_sum = 0

                    for k, j in by_similar_len.items():
                        by_similar_len_extend[k] = []
                        for l in j:
                            if l[0][0] in slot_occupied.values():
                                by_similar_len_extend[k].append(l)

                    for value in by_similar_len_extend.values():
                        if len(value) != 0:
                            for l in value:
                                len_sum += l[0][1]
                            avg = round(len_sum/len(value), 2)
                            tmp[avg] = value
                            len_sum = 0
                    by_similar_len_extend = tmp

                    len_to_look_extend, comb_to_look = get_avg_group(len_to_fill, by_similar_len_extend)
                    comb_result, comb_result_comp, max_comb_len = make_combination(original_stock_len, len_to_look_extend, i[0])

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

                # Complete the comb with current length and finded length
                comb_result += [i[0]]
                comb_result_stock_num += [key]
                comb_result_num += [i[1]]
                comb_result_id += [i[2]]

                # Solve logistic
                Xn = get_Xn(comb_result_comp, comb_result_stock_num, comb_result_num, comb_result_id)
                by_stock_num, by_similar_len = update_by_stock_num_and_by_similar_length(by_stock_num, by_similar_len, Xn)
                spare_result = update_spare_result(comb_result_comp, comb_result_id, Xn, spare_result)

                # Write result and format it nicely
                total_input_len += Xn[0][3] * original_stock_len
                total_waste_len += round(original_stock_len - sum(comb_result_comp), 2) * Xn[0][3]

                len_to_fill = round(original_stock_len - sum(comb_result_comp), 2)
                if len_to_fill >= 0:
                    len_to_fill = abs(len_to_fill)
                format_result_waste = str(len_to_fill) + " x " + str(Xn[0][3])
                original_stock_needed = Xn[0][3]
                current_slot_situation = copy.deepcopy(slot_occupied)

                for j in range(len(comb_result_id)):
                    if comb_result_id[j] < 0:
                        comb_result_comp[j] = str(comb_result_comp[j])
                if Xn[0][3] != 0:
                    result.append((comb_result_comp, original_stock_needed, format_result_waste, current_slot_situation))
                
                # Display result
                last = result[-1]
                print("\n{:<30}".format(str(last[0])) + "x{:<5}".format(last[1]) + "waste: {:<15}".format(last[2]))
                # print(slot_occupied, "\n")

            # Clear up slots if a stock is finished
            stock_finished = False
            for slot_alpha, stock_num in slot_occupied.items():
                if stock_num > 0:
                    stock_finished = True
                    for i in by_stock_num[stock_num]:
                        if i[1] > 0:
                            stock_finished = False
                            break
                    if stock_finished:
                        slot_occupied[slot_alpha] = 0

                        for k, v in slot_occupied.items():
                            if v < 0:
                                slot_occupied[k] = 0

        if len(by_similar_len.keys()) == 0:
            break
    
    # Print extra
    for stock_num, remain in by_stock_num.items():
        for r in remain:
            if r[1] < 0:
                print("\nLength", r[0], "from #", stock_num, "has", abs(r[1]), "extra")
    print()

    return result

def solve():
    if required_length == [] or required_number == [] or slot_range == {} or combined_slot_range == {}\
        or original_stock_len == 0 or machine_max_throughput == 0 or wanted_spare_range == [] or slot_occupied == {}:
        
        print("Error: Parameters not set properly")
        quit()

    _solve()
