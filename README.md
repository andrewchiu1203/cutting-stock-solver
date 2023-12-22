Cutting Stock Solver
-------------------------

This is a personal coding project that I thought would be interesting to do when one of my friend's parent, who's running a stell processing factory, was talking about this problem to me. The code isn't thoroughly tested and still has many bugs, but it's still fun to write.

### Features

- Minimizes wasted stock when different lengths of rebars of different quantities are cut from fixed-length rebars.
- Rebars are grouped by order number, or "stock_number" as what's called in the source code.
- Slots (rooms) to place the cut rebars immediately after they are processed can be set up by specifying a slot name, its minimum allowed length, and maximum allowed length.
- 2 Slots can be combined into 1 slot to accommodate longer cuts if you choose to set it up.

### How to Setup
- In sample_data.py, set up the 2 PARALLEL LIST (important).

    For list `required_length`, follow<br>
    `[ [ order number, length ], [ order number, length ], ... ]`

    For list `required_number`, follow<br>
    `[ [ order number, quantity ], [ order number, quantity ], ... ]`

- In sample_data.py, set up 1 list and 2 dictionary related to slot room.

    For list `slot_range`, follow<br>
    `["slot name" : [ min allowed length, max allowed length ],<br>"slot name" : [ min allowed length, max allowed length ], ... ]`

    For dict `slot_occupied`, follow<br>
   `{ "slot name" : 0, "slot name" : 0, "slot name" : 0, ... }`<br>
    *Note: All slot names in `slot_range` need to be in this dict with value init as 0.*

    For dict `combined_slot_range`, follow
	`{ "slot_name1 slot_name2" : [ min allowed length, max allowed length ],<br>"slot_name1 slot_name2" : [ min allowed length, max allowed length ], ... }`<br>
    *Note: The 2 slot names with 1 space in between are the slots that can be combined.*<br>
    *Note: If you do not wish to have any slots combined, leave this dict empty.*

- In sample_data.py, set `original_stock_len` to a int that defines the length of the original uncut rebars that were to pass through the cutting machine.
- In sample_data.py, set `machine_max_throughput` to a int that defines the maximum quantity of uncut rebars that can pass through the cutting machine at one time.

### How to Use
- Run driver.py to execute the program.
- The result will be output to a txt file named result.txt in the same directory.
- Adjust some of the parameters if possible:

    The `max_main_loop_count` is a safety guard that stops the main loop if there's a bug causing it not to end.

    The `accurate_level` determines how long the program searches for the best length combination for each cut. It works between 1 and 4.

	The `accurate_mode_threshold`. If there are more than this number of orders still left uncut, the accurate mode is not activated and `accurate_level` does nothing. This machenism is to reduce time of calculation.

Example Output
-------------------------
output.txt

    Ideal stock input: 248.4 m
    Final stock input: 256 m
    Waste percentage: 2.97 %

    Step: 1
	    Cuts# : x7		Waste: 0.3m		Clear: #3 
	    Groups: 3.7     4.0     8.0     
	    Stock#: 1       3       3       
	    Slot status: A-1 | A2-3 | B-0 | B2-0 | C1-0 | C2-0 | D1-0 | D2-0 | E-0 | F-0 | 
    Step: 2
	    Cuts# : x6		Waste: 0.0m		Clear: 
	    Groups: 3.1     2.6     2.6     2.0     2.6     3.1     
	    Stock#: 1       2       2       2       2       1       
	    Slot status: A-1 | A2-0 | B-0 | B2-0 | C1-2 | C2-0 | D1-0 | D2-0 | E-0 | F-0 | 
    Step: 3
	    Cuts# : x2		Waste: 0.3m		Clear: #2 
	    Groups: 2.0     2.0     3.7     2.0     2.0     2.0     2.0     
	    Stock#: 2       2       1       2       2       2       2       
	    Slot status: A-1 | A2-0 | B-0 | B2-0 | C1-2 | C2-0 | D1-0 | D2-0 | E-0 | F-0 | 
    Step: 4
	    Cuts# : x1		Waste: 1.2m		Clear: (3.7m of #1 x1 extra) #1 
	    Groups: 3.7     3.7     3.7     3.7     
	    Stock#: 1       1       1       1       
	    Slot status: A-1 | A2-0 | B-0 | B2-0 | C1-0 | C2-0 | D1-0 | D2-0 | E-0 | F-0 | 

    Current Stock Info [order number, remain number, id]:
    1 : [[3.7, -1, 0], [3.1, 0, 1]]
    2 : [[2.6, 0, 2], [2.0, 0, 3]]
    3 : [[8.0, 0, 4], [4.0, 0, 5]]
