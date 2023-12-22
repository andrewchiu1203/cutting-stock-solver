from sample_data import \
    required_length, required_number, combined_slot_range,\
    machine_max_throughput, slot_range, slot_occupied, original_stock_len
    
from stock_solver import solve

def main():
    outputs, ideal_stock_input, real_stock_input, by_stock_num = solve(
        required_length, required_number, slot_range, slot_occupied, combined_slot_range, 
        original_stock_len, machine_max_throughput, max_main_loop_count = 35, force_break_point = 0,
        accurate_mode_threshold = 5, accurate_level = 4)
    
    print("Ideal stock input:", round(ideal_stock_input, 2), "m")
    print("Final stock input:", round(real_stock_input, 2), "m")
    print("Waste percentage:",
          round((real_stock_input - ideal_stock_input)*100 / real_stock_input, 2), "%")
    print("Total steps:", len(outputs))
    print("Analyze done...")

if __name__ == "__main__":
    main()