#
# this tool is used to rename file names according to '_file_list_.txt'
#
# @since 2018.04.11
# @version 1.0
# @version 1.1.20190627
# @author tsungjung411@gmail.com
#

import os
import re

# ####################################################################
def throwException():
    error = 'press ENTER to end the app process'
    try:
        raw_input(error) # for python 2.X
    except Exception as w:
        input(error) # for python 3.X
    raise Exception()
# end-of-def

# ####################################################################
# gets the file list under the current working directory
# 
# Input:
#    None
# Output
#    <type 'list'>: the current working file list
#
def get_current_working_file_list():
    current_working_directory = os.getcwd()
    return sorted(os.listdir(current_working_directory))
# end-of-def


# ####################################################################
# splits the given input line into two file names:
# - old_file_name
# - new_file_name
#
# Input:
#    <type 'str'>: a line which consists of two arguments
#        line format: old_file_name new_file_name
# Output:
#    <type 'str'>, <type 'str'>: 
#        for example, 
#        ```
#        old_file_name, new_file_name = split_input_filenames('1.jpg 001.jpg')
#        ```
#        old_file_name will be '1.jpg', new_file_name will be '001.jpg'
#
# More examples:
#    split_input_filenames('old_filename.txt   new_filename.txt')
#    split_input_filenames('000.jpg 001.jpg')
#
def split_input_filenames(line):
    # parses the line
    # do not include the '\s' (whitespace), so that we can allow '\s' in the file name
    # such as 'track 01.mp3' (a whitespace between 'k' and '0')
    tokens = re.split('[\t\r\n]+', line)
    
    # collects non-empty tokens
    tokens = [token for token in tokens if len(token) > 0]
    
    # checks if there are two arguments: old_file_name and  new_file_name
    if len(tokens) != 2:
        print('[ERROR] line: {}'.format(line))
        print('[ERROR] tokens: {}'.format(str(tokens)))
        print('[ERROR] the format should be: src_file dest_file (two file names in one line)')
        throwException()
    # end-of-if
    return tokens[0], tokens[1]
# end-of-def


# ####################################################################
# checks whether or not the given file path exists
#
# Input:
#    file_path: the file path to be checked
# Output:
#    None
# Exception:
#    will be thrown if the file path does not exist
#
def check_file_existence(file_path):
    if os.path.exists(file_path) == False:
        raw_input('"{}" not exists'.format(os.path.abspath(file_path)))
        throwException()
    # end-of-if
# end-of-def


# ####################################################################
# 
def main():
    
    # reads the file list
    file_path = '_file_list_.txt'
    
    # checks whether or not the given file path exists
    if os.path.exists(file_path) == False:
        print('"{}" not exists'.format(os.path.abspath(file_path)))
        print("please invoke 'python_listdir.py' first")
        throwException()
    else:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        # end-of-with
    # end-of-def
    
    
    # prints detailed info
    src_to_dest_list = list() # an empty list, used to collect the target file names
    
    print('------------------------------------------------------------')
    print('File list:')
    print('------------------------------------------------------------')
    for line in lines:
        if len(line.strip()) == 0:
            continue;
        # end-of-if
        src_file, dest_file = split_input_filenames(line)
        print(src_file + ' -> ' + dest_file)
        tmp_file = '___tmp___.' + dest_file
        triple = (src_file, tmp_file, dest_file)
        src_to_dest_list.append(triple)
    # end-of-for
    
    
    print('------------------------------------------------------------\n')
    print('Simulation:')
    print('------------------------------------------------------------')
    # replaces old file names with new ones
    target_file_list = get_current_working_file_list()
    for src_file, tmp_file, dest_file in src_to_dest_list:
        
        # checks if the src file in the current file list
        # if yes, rename the src file to the dest file
        if src_file in target_file_list:
            index = target_file_list.index(src_file)
            target_file_list[index] = dest_file
        else:
            print('[WARNING] "{}" does not exist'.format(src_file))
        # end-of-if
    # end-of-for
    
    # finds conflicted file names
    file_set = set()
    for file in target_file_list:
        #print(' - ' + file)
        
        # conflicted?
        if file in file_set:
            print('[ERROR] conflicted files: "{}", please check the sources below:'.format(file))
            
            # lists conflicted files
            for src_file, tmp_file, dest_file in src_to_dest_list:
                if dest_file == file:
                    print('[ERROR] ' + src_file + ' -> ' + dest_file)
                # end-of-if
            # end-of-for
            throwException()
        else:
            file_set.add(file)
        # end-of-if
    # end-of-for
    
    
    print('------------------------------------------------------------\n')
    print('Rename:')
    print('------------------------------------------------------------')
    # renames src files to tmp files
    for src_file, tmp_file, dest_file in src_to_dest_list:
        print('rename: ' + src_file + ' -> ' + tmp_file)
        if os.path.exists(src_file) == False:
            print('[WARNING] "{}" does not exist, skipped\n'.format(src_file))
            continue
        elif os.path.exists(tmp_file) == True:
            print('[ERROR] "{}" exists'.format(tmp_file))
            print('[ERROR] when renaming from {} to {}'.format(src_file, tmp_file))
            throwException()
        # end-of-if
        os.rename(src_file, tmp_file)
    # end-of-for
    
    # renames tmp files to dest files
    for src_file, tmp_file, dest_file in src_to_dest_list:
        print('rename: ' + tmp_file + ' -> ' + dest_file)
        if os.path.exists(tmp_file) == False:
            print('[WARNING] "{}" does not exist, skipped\n'.format(tmp_file))
            continue
        elif os.path.exists(dest_file) == True:
            print('[ERROR] "{}" exists'.format(dest_file))
            throwException()
        # end-of-if
        os.rename(tmp_file, dest_file)
    # end-of-for
    
    raw_input('Finished!!!  Press ENTER to continue.')
# end-of-def

main()
