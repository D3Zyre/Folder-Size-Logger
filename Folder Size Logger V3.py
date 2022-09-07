import os
import datetime
from pickle import TRUE
import time

start = time.time()


def get_num_files(path):
    num_files = 0
    i = 0
    print("\nChecking number of files for drive "+str(path)+"...\n")
    for path, dir, file in os.walk(os.path.expanduser(path)):
        num_files += len(file)
        i += 1
        if i % 1000 == 0:
            print("\r" + str(num_files) + " files...", end="")

    return num_files


def get_file_folder_sizes_V3(path_to_use):
    """
    this is an example of what folder_sizes_dict looks like (in the format: {index: value, ...}):
    {"drive_letter:/full_path_to_a_directory_inside_path_to_use": {"size": size_of_that_folder, "children": [list_of_all_immediate_children_folders]}, ...}
    """
    folder_sizes_dict = dict()
    num_files = get_num_files(path_to_use)
    cdsize = 0
    count = 0
    print("\nGetting folder sizes for drive "+str(path_to_use)+"...\n")
    for path, dirs, files in os.walk(path_to_use, topdown=True):
        count += len(files)
        try:
            cdsize = sum([int(os.stat(str(path)+"/"+str(file))[6]) for file in files])
        except FileNotFoundError:
            pass
        folder_sizes_dict[path] = dict()
        folder_sizes_dict[path]["size"] = cdsize
        folder_sizes_dict[path]["children"] = dirs
        try:
            print("\r" + str(int((count/num_files)*10000)/100) + "%", end="")
        except ZeroDivisionError:
            pass

    print("\nComputing parent directories for drive "+str(path_to_use)+"...\n")
    folder_sizes_dict = check_parents_depth_V3(folder_sizes_dict)

    return [folder_sizes_dict, num_files]

def check_parents(folder_sizes_dict): #SLOWER THAN DEPTH
    n = 1
    num = len(folder_sizes_dict)
    for parent in folder_sizes_dict: # VERY SLOW!!!                             for each directory (potential parent)
        print("\r" + str(float(int(n/num*10000)/100)) + "%", end="")
        n += 1
        for child in folder_sizes_dict: #                                       and for each directory again (potential child)
            if str(child).startswith(str(parent)) and parent != child: #        if potential child a subdirectory or parent
                folder_sizes_dict[parent] += folder_sizes_dict[child] #         add its size to all (for loop) parent directory(es)

    return folder_sizes_dict

def check_parents_depth(folder_sizes_dict): # this is the best one so far
    sorting_dict = dict()
    for i in folder_sizes_dict:
        l = i.count("/") + i.count("\\")
        sorting_dict[i] = l

    folder_sizes_list = sorted(sorting_dict, key=sorting_dict.__getitem__) # list of the folders (indices of the dict) in order of depth
    sorting = sorted(list(sorting_dict.values())) # depth of each item in the list of folders

    n = -1 # n is the item number we are on
    last_depth = 0
    for depth in sorting: # depth is the current depth we are at (each depth can and usually does repeat several times, maybe even hundreds or more) the length of sorting is the length of the dict
        n += 1
        if depth != last_depth:
            last_depth = depth
            print("\rCurrent depth: " + str(depth-min(sorting)) + "/" + str(max(sorting)-min(sorting)), end="") # print stats
        parent = folder_sizes_list[n] # set the parent we are comparing to
        for i in range(n+1, len(folder_sizes_list)): # for each subdirectory in the list (anything after the item set as parent, so everything in the lower depths, and some things in the same depth)
            child = folder_sizes_list[i] # set the child we are comparing with
            if str(child).startswith(str(parent)) and parent != child: # compare parent to child
                folder_sizes_dict[parent] += folder_sizes_dict[child] # if child is a subdirectory then add the child's sum to the parent's
        
    return folder_sizes_dict

def check_parents_depth_V2(folder_sizes_dict): # still broken lol
    # needs to start at the deepest depth and sum only the folders one depth above, then go up one and sum only one depth above, using only the current depth, repeat until surface
    sorting_dict = dict()
    for i in folder_sizes_dict:
        l = i.count("/") + i.count("\\")
        sorting_dict[i] = l

    folder_sizes_list = sorted(sorting_dict, key=sorting_dict.__getitem__) # list of the folders (indices of the dict) in order of depth
    folder_sizes_list.reverse() # deepest first
    sorting = sorted(list(sorting_dict.values())) # depth of each item in the list of folders
    sorting.reverse() # deepest first
    sorting_unique = list(set(sorting)) # gets 1 of each unique value of sorting
    sorting_unique.reverse()

    n = sorting.count(max(sorting_unique))-1 # n is the parent folder we are on
    last_depth = 0
    for current_depth in sorting_unique: # once for each depth
        print("\rCurrent depth: " + str(max(sorting)-current_depth+min(sorting)) + "/" + str(max(sorting)-min(sorting)), end="") # print stats
        if current_depth != max(sorting_unique): # if we're not at the deepest depth (cuz there would be no subfolders to check there anyway)
            for i in range(sorting.count(current_depth)): # for each folder at that depth
                n += 1
                parent = folder_sizes_list[n]
                for sub in range(sorting.count(current_depth+1)): # for each subfolder from that depth (so the next depth)
                    #print("\nmax = " + str(len(folder_sizes_list)))
                    #print("current depth = " +str(current_depth))
                    #print("parent = " + str(n))
                    #print("i = " + str(i))
                    #print("child = " + str(n-i-sorting.count(current_depth+1)+sub)) # child should be from previous parents
                    #print("sub = "+str(sub))
                    #print("count = "+str(sorting.count(current_depth+1)))
                    child = folder_sizes_list[n-i-sorting.count(current_depth+1)+sub] # number of folders in all parent directories + number of subdirectory we're on
                    if str(child).startswith(str(parent)) and parent != child: # compare parent to child
                        folder_sizes_dict[parent] += folder_sizes_dict[child] # if child is a subdirectory then add the child's sum to the parent's


    return folder_sizes_dict

def check_parents_depth_V3(folder_sizes_dict): # IS THIS THE FASTEST ONE? yes, check again?
    sorting_dict = dict() # make a dict which will have each directory as key/index, and the depth of that directory as the associated value
    for i in folder_sizes_dict:
        if str(i).endswith(":/"): # if it's a drive the depth is not 1, but 0
            sorting_dict[i] = 0
        else:
            l = i.count("/") + i.count("\\") # count folder depth
            sorting_dict[i] = l

    folder_sizes_list = sorted(sorting_dict, key=sorting_dict.__getitem__, reverse=True) # list of the folders (indices of the dict) in order of depth, sorted from deepest to shallowest
    sorting = sorted(list(sorting_dict.values()), reverse=True) # depth of each item in the list of folders, sorted from deepest to shallowest

    n = -1 # n is the item number we are on in the sorted list
    for depth in sorting: # depth is the current depth we are at (each depth can and usually does repeat several times, maybe even hundreds or more) the length of sorting is the length of the dict
        n += 1
        skip = False
        if n % 100 == 0: # we only need to update the printed percentage once in a while to avoid slowdowns due to printing constantly
            print("\r" + str(float(int(n/len(sorting)*10000)/100)) + "%", end="")
        if sorting.count(depth-2) >= 1: # because we want to check possible parents only for one depth above the current depth, we need to check if that depth exists
            end_of_search = sorting.index(depth-2)
        elif sorting.count(depth-1) >= 1: # if there's only one depth above the current depth, then we want to go to the end of the list
            end_of_search = -1
        else: # if we are at the highest depth, then there are no parents to check
            skip = True
        if not skip:
            for parent in folder_sizes_list[sorting.index(depth-1):end_of_search]: # we only want to look at folders that are one depth above the current depth to see if they contain the current folder
                if str(folder_sizes_list[n]).replace("/", "\\") == str(parent).replace("/", "\\").rstrip("\\") + "\\" + str(folder_sizes_list[n]).replace("/", "\\").split("\\")[-1]: # checks if the folder we're looking at is the same as the potential parent but with only one more directory in it.
                    folder_sizes_dict[parent]["size"] += folder_sizes_dict[folder_sizes_list[n]]["size"] # adding the size of the directory to its parent

            if sorting.index(depth-1) == len(sorting)-1: # if the only parent left is the topmost folder, then the for loop doesn't run it, but we need to count it, so that's why this is here
                folder_sizes_dict[folder_sizes_list[-1]]["size"] += folder_sizes_dict[folder_sizes_list[n]]["size"] # adding the size of every directory to the top one

    return folder_sizes_dict

# do a V4 that does it recursively?

def check_sizes(folder_sizes_dict, minimum_f_size):
    folders = list() # list of tuples, (folder from dict, size of folder)
    passes = [0, 0]
    length = len(folder_sizes_dict)
    i = 0
    try:
        print("\nChecking folder sizes for drive "+str(list(folder_sizes_dict)[0])+"...\n")
    except IndexError:
        print("\nNon-existant drive...\n")
    for p in folder_sizes_dict: # seperate function
        if folder_sizes_dict[p]["size"] >= minimum_f_size*1000000:
            folders.append(tuple([str(p), int(folder_sizes_dict[p]["size"])]))
            passes[1] += 1
        elif i == 0: # include topmost folder regardless of whether it passes the minimum size or not
            folders.append(tuple([str(p), int(folder_sizes_dict[p]["size"])]))
            passes[0] += 1
        else:
            passes[0] += 1
        i += 1
        print("\r" + str(int((i/length)*10000)/100) + "%", end="")
    

    return [folders, passes]

def main():
    folder_list = list()
    minimum_folder_size = 1000 # MB
    total = 0
    number_files = 0
    f_sizes = [0, 0] # not large enough count, large enough count
    columns = ["Date", "Folder Path", "Size (B)", "Total Computer Size (B)", "Total Computer Files", "Total Computer Folders"]
    items = list()
    file_sizes = list()
    first_row = True
    first_time = False
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    #for letter in alphabet:
        #folders = get_file_folder_sizes_V2(letter+":/")
    folders = get_file_folder_sizes_V3("C:/")
    sizes = check_sizes(folders[0], minimum_folder_size)
    print(sizes[0])
    file_sizes.append(sizes[0])
    f_sizes = [f_sizes[0]+sizes[1][0], f_sizes[1]+sizes[1][1]]
    number_files += folders[1]
    try:
        total += sizes[0][0][1] # add size of topmost folder
    except IndexError:
        pass

    print("\nFinalizing list of folders...\n")
    [[folder_list.append(ii) for ii in i] for i in file_sizes]

    #print("\nSorting...\n")
    #sorted_by_second = sorted(folder_list, key=lambda tup: tup[1], reverse= True) # sort by size
    print(str(f_sizes[0]), "folders excluded...\n" + str(f_sizes[1]), "folders included...\n" + str(number_files), "files total...\n" + str(int(total)/1000000000), "GB used total...\n")
"""
    with open("Files/Folder Size Log.csv", "a") as file:
        for row in range(len(folder_list)):
            if first_row and first_time:
                items.append(columns)
                first_row = False
            items.append([str(d.datetime.today()), str(folder_list[row][0]), str(folder_list[row][1]), str(total), str(number_files), str(f_sizes[0]+f_sizes[1])])
        for i in items:
            row = str()
            for ii in i:
                row += '"'+ii+'"'+","
            try:
                file.write(row.rstrip(",")+"\n")
            except UnicodeEncodeError:
                print("ERROR!!!!\n")
                
"""


if __name__ == "__main__":
    main()
    end = time.time()
    print(end-start)


# add immediate children directories to each parent in the dict

# do it recursively one down at a time the recursive down again etc.