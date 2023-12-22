import math, copy, itertools
from operator import itemgetter
from collections import Counter
    
def by_similar_length_avg_recalculate(by_similar_length):
    tmp = {}
    len_sum = 0

    for value in by_similar_length.values():
        for i in value:
            len_sum += i[0]
        avg = round(len_sum/len(value), 2)
        tmp[avg] = value
        len_sum = 0
    
    by_similar_length = tmp
    return by_similar_length

def make_group(required_length, required_number, original_stock_len):
    by_stock_num = {}      # {stock_num : [ [len, remain, id], [...] ], ...}
    by_similar_length = {} # {avg_len: [ [len, remain, id, stock num], [] ], ...}
    tmp = []               # for taking the average length of each group
    ideal_stock_input = 0

    # group data by stock num
    for i in range(len(required_length)):
        #          [         length          number of stock     id       stock number    ]
        tmp.append([required_length[i][1], required_number[i][1], i, required_length[i][0]])
        ideal_stock_input += (required_length[i][1] * required_number[i][1])

        try:
            by_stock_num[required_length[i][0]] = by_stock_num[required_length[i][0]]
        except:
            by_stock_num[required_length[i][0]] = []
            by_stock_num[required_length[i][0]].append(
                [required_length[i][1], required_number[i][1], i])
        else:
            by_stock_num[required_length[i][0]].append(
                [required_length[i][1], required_number[i][1], i])

    # Group data into dict with each item's whole number part as key
    for i in range(0, original_stock_len - 1):
        by_similar_length[i] = []
        for j in tmp:
            length = j[0] 
            if i <= length < i + 1:
                by_similar_length[i].append(j)
        
        if len(by_similar_length[i]) == 0:
            del by_similar_length[i]

    by_similar_length = by_similar_length_avg_recalculate(by_similar_length)

    return by_stock_num, by_similar_length, ideal_stock_input

def get_avg_group(lengths, length_to_fill, accurate_mode, accurate_level=4):
    max_combs = []
    tmp = []

    if accurate_mode:
        for i in lengths:
            dup_count = (int(length_to_fill//i) - 1)
            if dup_count > accurate_level:
                dup_count = accurate_level
            for j in range(dup_count):
                tmp.append(i)

        lengths = list(lengths) + tmp

    for i in range(1, len(lengths) + 1):
        limited_comb_list = []
        comb = itertools.combinations(lengths, i)
        for j in comb:
            if sum(j) <= length_to_fill:
                limited_comb_list.append([j, sum(j)])
        limited_comb_list.sort(key = itemgetter(1), reverse= True)
        try:
            max_combs.append(limited_comb_list[0])
        except:
            pass
    
    try:
        max_combs.sort(key = itemgetter(1), reverse=True)
        return max_combs[0][0]
    except:
        return []

def make_combination(max_comb, length_to_fill, by_similar_length):
    lengths = []
    result = []

    for avg in max_comb:
        for stock in by_similar_length[avg]:
            length = stock[0]
            lengths.append(length)

    comb = itertools.combinations(lengths, len(max_comb))

    for i in comb:
        if sum(i) <= length_to_fill:
            result.append([sum(i), i]) # (sum, combination)
    result.sort(key = itemgetter(0), reverse= True)
    total_length, combination = result[0][0], result[0][1]

    return round(total_length, 2), combination

def allocate_slot_by_stock_num(stock_num, by_stock_num, slot_range, combined_slot_range, slot_occupied):
    availible_slots = []
    current_stock_lengths = []

    for slot_name, use in slot_occupied.items():
        if use == stock_num:
            availible_slots.append(slot_name)
    if availible_slots != []:
        return availible_slots

    for stock in by_stock_num[stock_num]:
        length = stock[0]
        current_stock_lengths.append(length)
    
    max_length = max(current_stock_lengths)
    min_length = min(current_stock_lengths)

    for slot, tolerance in slot_range.items():
        max_tolerance = tolerance[1]
        min_tolerance = tolerance[0]

        if max_tolerance >= max_length and min_tolerance <= min_length:
            if slot_occupied[slot] == 0:
                availible_slots.append([slot])
            if slot_occupied[slot] == stock_num:
                availible_slots = [[slot]]
                break
    
    if len(availible_slots) == 0:
        for slot, tolerance in combined_slot_range.items():
            max_tolerance = tolerance[1]
            min_tolerance = tolerance[0]
            slot1 = slot.split(" ")[0]
            slot2 = slot.split(" ")[1]

            if max_tolerance >= max_length and min_tolerance <= min_length:
                if slot_occupied[slot1] == 0 and slot_occupied[slot2] == 0:
                    availible_slots.append([slot1, slot2])
                if (slot_occupied[slot1] == stock_num and slot_occupied[slot2] == stock_num) or\
                   (slot_occupied[slot1] == stock_num and slot_occupied[slot2] == 0) or\
                   (slot_occupied[slot1] == 0 and slot_occupied[slot2] == stock_num):
                    availible_slots = [[slot1, slot2]]
                    break

    if len(availible_slots) > 0:
        return availible_slots[0]
    else:
        return []

def get_slot_by_stock_num(stock_num, slot_occupied):
    result = []

    for slot, occupation in slot_occupied.items():
        if occupation == stock_num:
            result.append(slot)

    return result

def get_result_paral_list(lengths_to_look, by_similar_length, avg_max_comb, slot_occupied):
    ids_to_look, stock_nums_to_look, remains_to_look = [], [], []

    for length_to_look in lengths_to_look:
        for avg in avg_max_comb:
            if math.floor(avg) == math.floor(length_to_look):
                ids_to_look.append("")
                stock_nums_to_look.append("")
                remains_to_look.append("")

                for stock in by_similar_length[avg]:
                    length = stock[0]
                    remain = stock[1]
                    id = stock[2]
                    stock_num = stock[3]

                    if length == length_to_look:
                        ids_to_look[-1] = id
                        stock_nums_to_look[-1] = stock_num
                        remains_to_look[-1] = remain

                        # if a stock num is already in slot, choose it first
                        if get_slot_by_stock_num(stock_num, slot_occupied) != []:
                            break
                break
    
    return ids_to_look, stock_nums_to_look, remains_to_look

def get_cut_number(remain, remains_to_look, id, ids_to_look, machine_max_throughput):
    dup = {id : remain}
    count = {id : 1}

    for i in range(len(ids_to_look)):
        dup[ids_to_look[i]] = remains_to_look[i]
        try:
            count[ids_to_look[i]] = count[ids_to_look[i]] + 1
        except:
            count[ids_to_look[i]] = 1
    
    for target_id, repeat in count.items():
        dup[target_id] = dup[target_id] // repeat
        if dup[target_id] == 0:
            dup[target_id] = 1

    cut_number = min(dup.values())
    if cut_number > machine_max_throughput:
        cut_number = machine_max_throughput
    return cut_number

def get_by_similar_length_constrain(by_similar_length, slot_occupied):
    by_similar_length_constrain = {}

    for avg, stocks in by_similar_length.items():
        by_similar_length_constrain[avg] = []
        for stock in stocks:
            stock_num = stock[3]
            if stock_num in slot_occupied.values():
                by_similar_length_constrain[avg].append(stock)
        if len(by_similar_length_constrain[avg]) == 0:
            del by_similar_length_constrain[avg]
    
    return by_similar_length_avg_recalculate(by_similar_length_constrain)

def current_stock_num_empty(stock_num, by_stock_num):
    for stock in by_stock_num[stock_num]:
        remain = stock[1]
        if remain > 0:
            return False
    return True

def update_by_stock_num(by_stock_num, cut_number, id, ids_to_look, slot_occupied):
    clear_message = ""
    clear_message_set = set()
    extra = dict()

    for target_id in [id] + ids_to_look:
        for stock_num, stocks in by_stock_num.items():
            for stock in stocks:
                main_id = stock[2]
                if main_id == target_id:
                    # remain = stock[1]
                    stock[1] -= cut_number
                    if current_stock_num_empty(stock_num, by_stock_num):
                        slot = get_slot_by_stock_num(stock_num, slot_occupied)
                        for s in slot:
                            slot_occupied[s] = 0
                            clear_message_set.add("#{} ".format(stock_num))
                    if stock[1] < 0:
                        try:
                            extra[stock_num][stock[0]] += -stock[1]
                        except:
                            extra[stock_num] = [stock[0], -stock[1]]
    
    for stock_num, data in extra.items():
        clear_message_set.add("({}m of #{} x{} extra) ".format(
            data[0], stock_num, data[1])
        )

    for i in clear_message_set:
        clear_message += i

    return by_stock_num, slot_occupied, clear_message

def update_by_similar_length(by_similar_length, cut_number, id, ids_to_look):
    new_by_similar_length = dict()
    occurance = Counter([id] + ids_to_look)

    for avg, stocks in by_similar_length.items():
        new_by_similar_length[avg] = []
        for stock in stocks:
            main_id = stock[2]
            if occurance[main_id] > 0:
                # remain = stock[1]
                stock[1] -= cut_number * occurance[main_id]

            if stock[1] > 0:
                new_by_similar_length[avg].append(stock)
        
        if len(new_by_similar_length[avg]) == 0:
            del new_by_similar_length[avg]

    return by_similar_length_avg_recalculate(new_by_similar_length)

def _solve(by_stock_num, by_similar_length, slot_range, slot_occupied, combined_slot_range, 
           original_stock_len, machine_max_throughput, max_main_loop_count, force_break_point,
           accurate_mode_threshold, accurate_level):
    
    output = []
    stock_used = 0
    main_loop_count = 0
    force_break = False

    while len(by_similar_length) != 0:
        main_loop_count += 1
        if main_loop_count > max_main_loop_count:
            print("Exceed max main loop count")
            print("Current Slot Info at error:")
            for k, v in by_stock_num.items():
                print(k, ":", v)
            exit()

        for base_stock_num, base_stocks in by_stock_num.items():
            if current_stock_num_empty(base_stock_num, by_stock_num):
                continue

            availible_slot = allocate_slot_by_stock_num(
                            base_stock_num, by_stock_num, slot_range, combined_slot_range, slot_occupied)
            
            if len(availible_slot) != 0:
                has_room = True
                for i in availible_slot:
                    slot_occupied[i] = base_stock_num
            else:
                has_room = False

            if not has_room:
                continue

            for stock in base_stocks:
                length = stock[0]
                remain = stock[1]
                id = stock[2]
                length_to_fill = original_stock_len - length

                if remain <= 0:
                    continue

                if len(by_similar_length) < accurate_mode_threshold:
                    avg_max_comb = get_avg_group(
                        by_similar_length.keys(), length_to_fill, True, accurate_level)
                else:
                    avg_max_comb = get_avg_group(
                        by_similar_length.keys(), length_to_fill, False, accurate_level)
                
                pair_length, lengths_to_look = make_combination(
                    avg_max_comb, length_to_fill, by_similar_length)
                
                ids_to_look, stock_nums_to_look, remains_to_look = get_result_paral_list(
                    lengths_to_look, by_similar_length, avg_max_comb, slot_occupied)
                
                has_room = False
                tmp_slot_occupied = copy.deepcopy(slot_occupied)
                for stock_num in stock_nums_to_look:
                    availible_slot = allocate_slot_by_stock_num(
                            stock_num, by_stock_num, slot_range, combined_slot_range, tmp_slot_occupied)
                    if len(availible_slot) != 0:
                        has_room = True
                        for i in availible_slot:
                            tmp_slot_occupied[i] = stock_num
                    else:
                        has_room = False
                        break

                if not has_room:
                    by_similar_length_constrain = get_by_similar_length_constrain(
                                                        by_similar_length, slot_occupied)

                    if len(by_similar_length_constrain) < accurate_mode_threshold:
                        avg_max_comb = get_avg_group(
                            by_similar_length_constrain.keys(), length_to_fill, True, accurate_level)
                    else:
                        avg_max_comb = get_avg_group(
                            by_similar_length_constrain.keys(), length_to_fill, False, accurate_level)
                                        
                    pair_length, lengths_to_look = make_combination(
                        avg_max_comb, length_to_fill, by_similar_length_constrain)

                    ids_to_look, stock_nums_to_look, remains_to_look = get_result_paral_list(
                        lengths_to_look, by_similar_length_constrain, avg_max_comb, slot_occupied)
                        
                else:
                    slot_occupied = tmp_slot_occupied

                cut_number = get_cut_number(
                    remain, remains_to_look, id, ids_to_look, machine_max_throughput)
                
                by_similar_length = update_by_similar_length(
                    by_similar_length, cut_number, id, ids_to_look)
                
                result = [length] + list(lengths_to_look)
                result_stock_num = [base_stock_num] + stock_nums_to_look
                waste = round(original_stock_len - length - pair_length, 2)
                output.append(
                    [result, result_stock_num, cut_number, waste, copy.deepcopy(slot_occupied), ""]
                )
                
                by_stock_num, slot_occupied, clear_mesaage = update_by_stock_num(
                    by_stock_num, cut_number, id, ids_to_look, slot_occupied)
                
                stock_used += cut_number * original_stock_len
                output[-1][-1] = clear_mesaage

                if len(output) == force_break_point:
                    force_break = True
                    break

            if force_break:
                break

        if force_break:
            break
    
    return output, stock_used, by_stock_num

def solve(required_length, required_number, slot_range, slot_occupied, combined_slot_range, 
        original_stock_len, machine_max_throughput, max_main_loop_count = 35, force_break_point = 0,
        accurate_mode_threshold = 4, accurate_level = 4):
    
    by_stock_num, by_similar_length, ideal_stock_input = make_group(
                                        required_length, required_number, original_stock_len)
    
    output, real_stock_input, by_stock_num = _solve(
            by_stock_num, by_similar_length, slot_range, slot_occupied, combined_slot_range, 
            original_stock_len, machine_max_throughput, max_main_loop_count, force_break_point,
            accurate_mode_threshold, accurate_level)
    
    write_output_to_txt(output, ideal_stock_input, real_stock_input, by_stock_num)
    
    return output, ideal_stock_input, real_stock_input, by_stock_num

def write_output_to_txt(outputs, ideal_stock_input, real_stock_input, by_stock_num):
    file = open("result.txt", "w", encoding="utf-8")
    file.write("Ideal stock input: {} m\n".format(round(ideal_stock_input, 2)))
    file.write("Final stock input: {} m\n".format(round(real_stock_input, 2)))
    file.write("Waste percentage: {} %\n".format(
        round((real_stock_input - ideal_stock_input)*100 / real_stock_input, 2)
    ))

    step = 0
    for output in outputs:
        step += 1
        file.write("\nStep: {}".format(step))
        file.write("\n\tCuts# : x{}".format(output[2]))
        file.write("\t\tWaste: {}m".format(output[3]))
        file.write("\t\tClear: {}\n".format(output[5]))

        file.write("\tGroups: ")
        for i in output[0]:
            file.write("{:<6}  ".format(i))
        file.write("\n\tStock#: ")
        for i in output[1]:
            file.write("{:<6}  ".format(i))
        file.write("\n")

        file.write("\tSlot status: ")
        for slot_name, status in output[4].items():
            file.write("{}-{} | ".format(slot_name, status))
    
    file.write("\n\n")
    file.write("Current Stock Info [order number, remain number, id]:\n")
    for stock_num, stocks in by_stock_num.items():
        file.write("{} : {}\n".format(stock_num, stocks))
    file.close()
