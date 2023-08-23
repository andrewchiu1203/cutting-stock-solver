def extend_wanted_spare_in_comb_result(_comb_result, _comb_result_id):
    comb_result = _comb_result
    comb_result_id = _comb_result_id
    len_sum = sum(comb_result)
    len_to_fill = original_stock_len - len_sum
    spare_quantity = 0
    
    if len_to_fill == 0:
        return comb_result

    # Pick wanted spare length out
    for i in range(len(comb_result_id)):
        if comb_result_id[i] < 0:
            spare_quantity += 1

    if spare_quantity != 0:
        # Add len to fill to the shortest spare length so there's no scrape in comb_result
        avg_spare_extend = round(len_to_fill / spare_quantity, 2)
        for i in range(len(comb_result_id)):
            if comb_result_id[i] < 0:
                if wanted_spare_range[0] <= comb_result[i] + avg_spare_extend <= wanted_spare_range[1]:
                    comb_result[i] = round(comb_result[i] + avg_spare_extend, 2)
                else:
                    if comb_result[i] + avg_spare_extend >= wanted_spare_range[1]:
                        comb_result[i] = wanted_spare_range[1]
    
    return comb_result