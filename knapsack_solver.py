import itertools
from operator import itemgetter

INT_MIN=-2147483648

def nextPermutation(nums: list) -> None:
        if sorted(nums,reverse=True)==nums:
            return None
        n=len(nums)
        brk_point=-1
        for pos in range(n-1,0,-1):
            if nums[pos]>nums[pos-1]:
                brk_point=pos
                break
        else:
            nums.sort()
            return
        replace_with=-1
        for j in range(brk_point,n):
            if nums[j]>nums[brk_point-1]:
                replace_with=j
            else:
                break
        nums[replace_with],nums[brk_point-1]=nums[brk_point-1],nums[replace_with]
        nums[brk_point:]=sorted(nums[brk_point:])
        return nums
 
# Find the all the possible solutions of the 0/1 knapSack problem
def knapSack(W, wt, val, n):
    # Mapping weights with Profits
    umap=dict()
    
    set_sol=set()
    # Making Pairs and inserting to the map
    for i in range(n) :
        umap[wt[i]]=val[i]
    
    result = INT_MIN
    remaining_weight=0
    sum = 0
     
    # Loop to iterate over all the possible permutations of array
    while True:
        sum = 0
        
        # Initially bag will be empty
        remaining_weight = W
        possible=[]
         
        # Loop to fill up the bag until there is no weight such which is 
        # less than the remaining weight of the 0-1 knapSack
        for i in range(n) :
            if (wt[i] <= remaining_weight) :
 
                remaining_weight -= wt[i]
                sum += (umap[wt[i]])
                possible.append((wt[i],
                     umap[wt[i]])
                )
             
        possible.sort()
        if (sum > result) :
            result = sum
         
        if (tuple(possible) not in set_sol):
            # for sol in possible:
                # print(sol[0], ": ", sol[1], ", ",end='')
                # pass
             
            # print()
            set_sol.add(tuple(possible))
         
         
        if not nextPermutation(wt):
            break

    return round(result, 4), possible

def knapsack_solver_brute_force(comb_list: list, r = 4, len_repeated_max = 3, len_to_fill = 14):
    max_comb_under_current_repeat_max = []

    for i in range(1, r + 1):
        limited_comb_list = []
        comb = itertools.combinations(comb_list, i)
        for j in comb:
            if sum(j) <= len_to_fill:
                limited_comb_list.append([j, sum(j)])
        limited_comb_list.sort(key = itemgetter(1), reverse= True)
        max_comb_under_current_repeat_max.append(limited_comb_list[0])

    max_comb_under_current_repeat_max.sort(key = itemgetter(1), reverse= True)
    combination = max_comb_under_current_repeat_max[0]
    print(combination)

# Driving code for testing
# comb_list = [2.3, 3.6, 4.1, 2.7, 4.5, 5.4, 5.7, 6.4, 7.8, 8.6, 8.9]
# knapsack_solver_brute_force(comb_list)

# l = sorted([2.3, 3.6, 4.1, 5.4, 5.7, 6.4, 7.8, 8.6])
# result, comb = knapSack(14, l, l, len(l))
# print(comb)