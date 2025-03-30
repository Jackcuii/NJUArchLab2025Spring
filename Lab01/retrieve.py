import json
import os
import re
import sys


def parse_gem5_output_and_update_json(json_file, gem5_output_file, independent_var, target_entry):
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

    print(f"\033[34mCaught:{target_value}\033[0m")

    json_data = {}
    if os.path.exists(json_file):
        try:
            with open(json_file, "r") as f:
                json_data = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Bad json '{json_file}' , overwrite.")
        except Exception as e:
            print(f"Error: cannot read from '{json_file}': {e}")
            return

    json_data[independent_var] = target_value

    try:
        with open(json_file, "w") as f:
            json.dump(json_data, f, indent=4)
    except Exception as e:
        print(f"Error: cannot write to json '{json_file}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("python script.py <json_file> <gem5_output_file> <independent_var> <target_entry>")
        sys.exit(1)

    json_file_path = sys.argv[1]        
    gem5_output_file_path = sys.argv[2]
    independent_variable = sys.argv[3]  
    target_entry_name = sys.argv[4]     

    parse_gem5_output_and_update_json(json_file_path, gem5_output_file_path, independent_variable, target_entry_name)
