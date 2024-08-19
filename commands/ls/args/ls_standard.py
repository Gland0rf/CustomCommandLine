import subprocess
import os
import humanize
import datetime
from tzlocal import get_localzone

def get_file_modification_time(full_path, is_timestamp_utc=True):
    """Get the formatted modification time of a file."""
    ti_m = os.path.getmtime(full_path)
    local_timezone = get_localzone()
    if is_timestamp_utc:
        dt_object = datetime.datetime.fromtimestamp(ti_m, tz=datetime.timezone.utc)
        local_dt_object = dt_object.astimezone(local_timezone)
    else:
        local_dt_object = datetime.datetime.fromtimestamp(ti_m, tz=local_timezone)
    return local_dt_object.strftime('%d/%m/%Y %H:%M')

def calculate_max_prefix_length(files, current_dir):
    """Calculate the maximum length of the prefix before the file name."""
    max_prefix_length = 0
    for file in files:
        full_path = os.path.join(current_dir, file)
        m_ti = get_file_modification_time(full_path)
        if os.path.isdir(full_path):
            prefix_str = m_ti + " <DIR>  "
        else:
            prefix_str = m_ti + "        "  + str(humanize.intcomma(os.path.getsize(full_path))) + "  "
        if len(prefix_str) > max_prefix_length:
            max_prefix_length = len(prefix_str)
    return max_prefix_length

def generate_aligned_output(files, current_dir, max_prefix_length):
    """Generate the output string with aligned file names."""
    output_str = ""
    total_files = 0
    file_size = 0
    total_folders = 0
    folder_size = 0

    for file in files:
        full_path = os.path.join(current_dir, file)
        m_ti = get_file_modification_time(full_path)
        
        if os.path.isdir(full_path):
            prefix_str = m_ti + " <DIR>  "
        else:
            prefix_str = m_ti + "        " + str(humanize.intcomma(os.path.getsize(full_path))) + "  "
        
        spaces_needed = max_prefix_length - len(prefix_str)
        output_str += prefix_str + ' ' * spaces_needed + file + "\n"
        
        if os.path.isfile(full_path):
            total_files += 1
            file_size += os.path.getsize(full_path)
        elif os.path.isdir(full_path):
            total_folders += 1
            folder_size += os.path.getsize(full_path)

    return output_str, total_files, file_size, total_folders, folder_size

def standard_format(current_dir):
    output_str = ""
    try:
        result = subprocess.run(['vol', 'C:'], shell=True, stdout=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.split("\n")

        if lines:
            for line in lines:
                output_str += line.strip() + "\n"

    except subprocess.CalledProcessError:
        output_str += "Could not find a volume."
        
    output_str += "Directory of " + current_dir + "\n\n"

    files = [entry.name for entry in os.scandir(current_dir + "\\") if entry.is_file() or entry.is_dir()]
    
    total_files = 0
    total_folders = 0
    
    file_size = 0
    folder_size = 0
    
    files = os.listdir(current_dir)  # Get the list of files in the directory

    max_prefix_length = calculate_max_prefix_length(files, current_dir)
    output_str, total_files, file_size, total_folders, folder_size = generate_aligned_output(files, current_dir, max_prefix_length)
            
    file_size = humanize.filesize.naturalsize(file_size)
    folder_size = humanize.filesize.naturalsize(folder_size)
            
    output_str += f"\n{total_files} Files, {file_size}"
    output_str += f"\n{total_folders} Folders, {folder_size} (non-recursive)"
    
    return output_str

