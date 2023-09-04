def check_valid_parentheses(target_str: str) -> bool:
    start_para_count = 0
    end_para_count = 0
    valid = True

    for word in target_str:
        if word == "(":
            start_para_count += 1
        if word == ")":
            end_para_count += 1
        
        if end_para_count > start_para_count:
            valid = False
            break
    
    return valid

test_str = "wehfui((wef()weu)))"
valid = check_valid_parentheses(test_str)
print(valid)