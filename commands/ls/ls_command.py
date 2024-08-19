from .args import ls_standard as arg_standard
from .args import ls_arg_L as arg_l

def get_priority_list():
    return [
        "/?", "-?",  # Help flag
        "/V", "-V",  # Version flag
        "Directory Path",  # Placeholder for the directory path
        "/B", "-B",  # Bare format
        "/W", "-W",  # Wide format
        "/D", "-D",  # Sorted by column
        "/A", "-A",  # File attributes
        "/S", "-S",  # Include subdirectories
        "/T", "-T",  # Time field
        "/O", "-O",  # Sorting order
        "/N", "-N",  # Long format sorted by name
        "/Q", "-Q",  # Show file ownership
        "/X", "-X",  # Show short file names
        "/R", "-R",  # Show alternate data streams
        "/P", "-P",  # Pause after each screen
        "/L", "-L",  # Use lowercase
        "/C", "-C"   # Display the thousand separator
    ]
    
def load_arg_order(args):
    priority_list = get_priority_list()
    
    parsed_args = {}
    
    for arg in args:
        current_val = arg[0]
        if not current_val.startswith('-') and not current_val.startswith('/'):
            parsed_args['Directory Path'] = current_val
            break
        
    for priority in reversed(priority_list):
        if priority == "Directory Path":
            continue
        for arg in args:
            current_val = arg[0]
            if current_val.startswith(priority):
                parsed_args[priority] = current_val
                
    return parsed_args

def ls_command(args, current_dir):
    parsed_args = load_arg_order(args)
    
    command_output = arg_standard.standard_format(current_dir)
    for current_arg in parsed_args.keys():
        if(current_arg == "/L"):
            #All lowercase
            command_output = arg_l.parse(command_output)
                
    return command_output