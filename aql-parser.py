import sys

source_file = 'test2.aql'

commands = []

with open(source_file, 'r') as file:    
    command = ''

    for line in file:
        line = line.strip().rstrip()
        command = command + line
        if (line.endswith(';')):            
            commands.append(command.rstrip(';'))
            command = ''


for command in commands:
     print(command)    
     tokens = command.split()
     print(tokens)