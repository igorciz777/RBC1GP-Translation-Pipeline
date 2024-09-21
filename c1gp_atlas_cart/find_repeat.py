import sys

#a little script to help my find repeats in those /out files

def find_lines_above(file_path, target_line):
    output = open(output_file, 'w')
        
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        previous_line = None 
        for line in file:
            if line.strip() == target_line:
                if previous_line:
                    print(previous_line.strip())
                    output.write(previous_line.strip() + '\n')
            previous_line = line

    output.close()

try:
    file_path = sys.argv[1]
    target_line = sys.argv[2]
    output_file = sys.argv[3]
except IndexError:
    print("Usage: python find_repeat.py <file_path> <target_line> <output_file>")
    sys.exit(1)

find_lines_above(file_path, target_line)
