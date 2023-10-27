# cutting-stock-solver
It solves real-world cutting stock problems with designated spare length functions. <br>
At the same time, it also allows the setting of slot rooms for easier use.<br>
<br>

The solve() function in the heavy_stock_solver.py file is the main solver. <br>
But, before calling it, some parameters have to be set through other functions in the same file <br>
For how to set them, explanations are in driving_code.py <br>
<br>

After that, by calling solve(), the program calculates the best way to process the order from a fixed-length original stock. <br>
If you wish to display the result in the terminal, use display_result(). <br>
<br>

The solve() function returns a list with the format:<br>
&#9; [ [ len, len, len ... ], number of uncut stock passed through, wasted length of current combination ] <br>
&#9; (If '' is seen around a length, it's a reserved spare instead of a stock for the order) <br>
<br>