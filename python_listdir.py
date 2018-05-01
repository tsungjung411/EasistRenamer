import os

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
def main():
    with open('_file_list_.txt', 'w') as f:
        file_list = get_current_working_file_list()
        
        # iterates each file
        # @see [https://goo.gl/ET4QEK Correct way to write line to file?]
        for file in file_list:
            f.write(file.strip() + '\n')
        # end-of-file
    # end-of-with
# end-of-def

main()
