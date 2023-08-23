# cutting-stock-solver
It solves real-world cutting stock problems with designated spare length functions. <br>
At the same time, it also allows the setting of slot rooms for easier use.<br>
<br>

The solve() function in the heavy_stock_solver.py file is the main solver. <br>
But, before calling it, some parameters have to be set through other functions in the same file <br>
<br>

1. <br>
&#9; &#9; Call set_required_length() while passing through a list that looks like this: <br>
&#9; &#9; &#9; [ [stock_num 1, length 1], [stock_num 2, length 2], [stock_num 3, length 3] ... ] <br>
&#9; &#9; This function sets the length of each stock that's requested from the order and its corresponding stock number. <br>
<br>

&#9; &#9; Call set_required_number() while passing through a list that looks like this: <br>
&#9; &#9; &#9; [ [stock_num 1, quantity 1], [stock_num 2, quantity 2], [stock_num 3, quantity 3] ...] <br>
&#9; &#9; This function sets the length of each stock that's requested from the order and its corresponding stock number. <br>
&#9; &#9; (The lists passed through the 2 functions have to be parallel lists based on their stock number)
<br>

2. <br>
&#9; &#9;  Call set_slot_range() while passing through a dictionary that looks like this: <br>
&#9; &#9; &#9; {"Slot name 1" : [min length, max length], "Slot name2 " : [min length, max length] ... } <br>
&#9; &#9; This function sets the max and min allowed length of each however many slots you wish to have to store the stock. <br>
<br>

3. <br>
&#9; Call set_combined_slot_range while passing through a dictionary that looks like this: <br>
&#9; &#9; {"slot name 1" : "slot that combines with it", "slot name 2" : "slot that combines with it" ...} <br>
&#9; This function sets combinations of slot rooms that you wish can be merged temporarily to store longer stock. <br>
<br>

4. <br>
&#9; &#9; Call set_required_length() while passing through a list that looks like this: <br>
&#9; &#9; &#9; [ [stock_num 1, length 1], [stock_num 2, length 2], [stock_num 3, length 3] ...] <br>
&#9; &#9; This function sets the length of each stock that's requested from the order and its corresponding stock number. <br>
<br>

5. <br>
&#9; &#9; Call set_original_stock_len() while passing through an integer: <br>
&#9; &#9; This function sets the length of the uncut stocks that will be passed to the cutting machine. <br>
<br>

6. <br>
&#9; &#9; Call set_machine_max_throughput() while passing through an integer: <br>
&#9; &#9; &#9; [ [stock_num 1, length 1], [stock_num 2, length 2], [stock_num 3, length 3] ...] <br>
&#9; &#9; This function sets the max allowed number of uncut stock that can be passed through the cutting machine. <br>
<br>

7. <br>
&#9; &#9; Call set_wanted_spare_len() while passing through a dictionary that's exactly 4-keys long: <br>
&#9; &#9; &#9; {-1 : "spare len 1", -2 : "spare len 2", -3: : "spare len 3", -4 : "spare len 4"} <br>
&#9; &#9; This function sets the length of each designated spare that you wish to be used later. <br>
<br>

8. <br>
&#9; &#9; Call set_wanted_spare_range() while passing through a list that looks like this: <br>
&#9; &#9; &#9; ["min length allowed as spare", "max length allowed as spare"] <br>
&#9; &#9; This function sets the max and min length that can be considered as designated spare. <br>
<br>

9. <br>
&#9; &#9; Call init_slot_occupied() while passing through a dictionary that looks like this: <br>
&#9; &#9; &#9; {"Slot 1" : 0, "Slot 2 " : 0, "Slot 3" : 0, "Slot 4" : 0 ... } <br>
&#9; &#9; This function initializes the occupation of all the slots you created in set_slot_range() as 0, meaning its empty. <br>
<br>

Finally, by calling solve(), the program calculates the best way to cut the order from a fixed-length original stock. <br>
If you wish to display the result in the terminal, use display_result(). <br>
<br>

The solve() function returns a list with the format:<br>
&#9; [ [len, len, len ... ], number of uncut stock passed through, wasted length of current combination ] <br>
&#9; (If '' is seen around a length, it's a designated spare instead of a stock for the order) <br>
<br>

If the above explanation is unclear, go see driving_code.py, a file that has a complete example. 
