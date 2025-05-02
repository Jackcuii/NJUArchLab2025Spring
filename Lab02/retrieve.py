import json
import os
import re
import sys


def parse_gem5_output(gem5_output_file, target_entry):
    if not os.path.exists(gem5_output_file):
        print(f"Error: Unable to find '{gem5_output_file}'!")
        return
    try:
        with open(gem5_output_file, "r") as f:
            gem5_output_lines = f.readlines()
    except Exception as e:
        print(f"Error: Unable to open '{gem5_output_file}': {e}")
        return
    
    target_value = None

    for line in gem5_output_lines:
        if line.strip().startswith(target_entry):
            parts = line.split()
            if len(parts) >= 2:
                target_value = parts[1]
            break
    if target_value is None:
        print(f"Error: fail to find '{target_entry}'!")
        return

    return target_value

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python script.py <result_name>")
        sys.exit(1)

    gem5_output_file_path = f"./res/{sys.argv[1]}/stats.txt"
    target_entry_name1 = "system.cpu.commit.branches"
    target_entry_name2 = "system.cpu.iew.branchMispredicts"
    target_entry_name3 = "system.cpu.iew.predictedTakenIncorrect"
    target_entry_name4 = "system.cpu.iew.predictedNotTakenIncorrect"
    target_entry_name5 = "simTicks"
    target_entry_name6 = "simInsts"
    target_entry_name7 = "simOps"
    target_entry_name8 = "system.cpu.numCycles"
    
    result1 = parse_gem5_output(gem5_output_file_path, target_entry_name1)
    result2 = parse_gem5_output(gem5_output_file_path, target_entry_name2)
    result3 = parse_gem5_output(gem5_output_file_path, target_entry_name3)
    result4 = parse_gem5_output(gem5_output_file_path, target_entry_name4)
    result5 = parse_gem5_output(gem5_output_file_path, target_entry_name5)
    result6 = parse_gem5_output(gem5_output_file_path, target_entry_name6)
    result7 = parse_gem5_output(gem5_output_file_path, target_entry_name7)
    result8 = parse_gem5_output(gem5_output_file_path, target_entry_name8)
    
    print(f"{sys.argv[1]}:")
    print(f"Total {result5} ticks, {result6} instructions, {result7} operations, {result8} cycles.")
    print(f"Among {result1} branches, {result2} are mispredicted, {result3} are predicted taken incorrectly, {result4} are predicted not taken incorrectly.")
    
