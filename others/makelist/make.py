application_number = []

with open('input_list.txt', 'r') as file:
    for line in file:
        line = line.strip()
        application_number.append(line)

application_number = list(set(application_number)) # remove duplicates

with open('output_list.py', 'w') as file:
     file.write(f"APPLICATION_NUMBERS = {str(application_number)}")