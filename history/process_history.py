import sys
import csv

current_path = sys.path[0] + "/"
current_history_file = current_path + input() + '.csv'

def transfer_data(current_history_file):
    """
    INPUT: None
    transfer_data converts data of txt file and writes it into csv file
    (txt and csv file must have same names)
    OUTPUT: None
    """
    # Write header in csv file:
    with open(current_history_file, 'w') as sheet:
        writer = csv.writer(sheet)
        header = [
            'file',
            'time_in_seconds',
            'solution_size',
            'recursive_steps',
            'first_lower_bound_difference',
            'high_degree_rules',
            'degree_zero_rules',
            'extreme_reduction_rules',
            'degree one rules',
            'degree two rules',
            'domination rules',
            'lower_bounds',
            'finished',
            'solution_size_verified'
        ]
        writer.writerow(header)
    # Iterate through every line of txt file:
    for line in sys.stdin:
        for starter in ["random/", "dimacs/", "snap/"]:
            # If row contains statistics:
            if line.startswith(starter):
                # Write data in csv file:
                with open(current_history_file, 'a') as sheet:
                    writer = csv.writer(sheet)
                    line_values = line.split()
                    if len(line_values) < len(header):
                        line_values.insert(3,'')
                    writer.writerow(line_values)
                break

transfer_data(current_history_file)