def lower_last_word_of_string(line):
    
    last_space_index = line.rfind(' ')
    
    before_last_word = line[:last_space_index + 1]
    last_word = line[last_space_index + 1:]
    
    last_word = last_word.lower()
    
    modified_first_string = before_last_word + last_word
    
    return modified_first_string

def parse(command_output):
    splitted_output = command_output.split("\n")
    for x, line in enumerate(splitted_output):
        if(len(line) > 0):
            lowered_line = lower_last_word_of_string(line)
            splitted_output[x] = lowered_line
    command_output = '\n'.join(splitted_output)
    
    return command_output