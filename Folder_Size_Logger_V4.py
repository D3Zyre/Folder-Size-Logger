import os
import time
import datetime as d

start = time.time()


def get_num_files(path, print_stats_every_x_seconds = 1):
    """
    Counts the number of files in a directory using os.walk
    set print_stats_every_x_seconds to -1 to never print
    """
    num_files = 0
    t = time.time()
    if print_stats_every_x_seconds != -1:
        print("\nChecking number of files for path "+str(path)+"...\n")
    for path, dir, file in os.walk(os.path.expanduser(path)):
        num_files += len(file)
        if time.time() - t >= print_stats_every_x_seconds and print_stats_every_x_seconds != -1:
            print("\r" + str(num_files) + " files...", end="")
            t = time.time()

    return num_files

def get_size_folder(path, print_stats_every_x_seconds = 1):
    """
    gets the size of the folder
    set print_stats_every_x_seconds to -1 to never print
    """
    size = 0
    t = time.time()
    if print_stats_every_x_seconds != -1:
        print("\nChecking size of path "+str(path)+"...\n")
    for path, dir, files in os.walk(os.path.expanduser(path)):
        size += sum([os.stat(str(path)+"/"+str(file))[6] for file in files])
        if time.time() - t >= print_stats_every_x_seconds and print_stats_every_x_seconds != -1:
            print("\r" + str(size) + " Bytes...", end="")
            t = time.time()
    
    return size


def get_file_folder_sizes_V4(path_to_use):
    """
    this is an example of what folder_sizes_dict looks like (in the format: {index: value, ...}):
    {"drive_letter:/full_path_to_a_directory_inside_path_to_use": {"size": size_of_that_folder, "children": [list_of_all_immediate_children_folders]}, ...}

    This function gets the sizes of all the folders in the input directory and outputs the dictionary above, but the sizes of the folders are only the sum of the files in that folder, and does not include any subfolders.
    """
    folder_sizes_dict = dict()
    num_files = get_num_files(path_to_use) # we want to know the number of files in a directory so that we know our progress through this function, for printing it to the command prompt
    cdsize = 0 # this is the size of the current directory
    count = 0 # this is the number of files inside path_to_use
    print("\nGetting folder sizes for drive "+str(path_to_use)+"...\n")
    for path, dirs, files in os.walk(path_to_use, topdown=True): ############################################################ CHECK TOPDOWN AND RECODE THIS WHOLE THING (cuz you can code it recursively in one go) TwT
        path = str(path).replace("/", "\\") # we want the slashes to be consistent, this is useful for other functions in this program
        count += len(files)
        try: # if a file is deleted or something while the code is running it could error out so we have to account for that and skip it if it got deleted
            cdsize = sum([int(os.stat(str(path)+"/"+str(file))[6]) for file in files]) # sum the sizes of the files
        except FileNotFoundError:
            pass
        except OSError:
            pass
        folder_sizes_dict[path] = dict() # we need tell our code that what is in here will be a dictionary before we can start referring to it like one
        folder_sizes_dict[path]["size"] = cdsize
        folder_sizes_dict[path]["children"] = dirs
        try: # the try is just here to ignore if I divide by 0, I guess I was too lazy to just use an if, I wonder if this is slower...
            print("\r" + str(int((count/num_files)*10000)/100) + "%", end="")
        except ZeroDivisionError:
            pass

    print("\nComputing parent directories for drive "+str(path_to_use)+"...\n")
    folder_sizes_dict = check_parents_recursive(folder_sizes_dict) # now we have to go through our whole dictionary and properly sum up the sizes of the folders, since their sizes are incomplete as described above

    return [folder_sizes_dict, num_files]

# the multiline comment below is old code from previous versions of this script
"""
def check_parents(folder_sizes_dict): # This is the slowest method of calculating actual folder sizes I made so don't use it (brute force)
    n = 1
    num = len(folder_sizes_dict)
    for parent in folder_sizes_dict: # VERY SLOW!!!                             for each directory (potential parent)
        print("\r" + str(float(int(n/num*10000)/100)) + "%", end="")
        n += 1
        for child in folder_sizes_dict: #                                       and for each directory again (potential child)
            if str(child).startswith(str(parent)) and parent != child: #        if potential child a subdirectory or parent
                folder_sizes_dict[parent] += folder_sizes_dict[child] #         add its size to all (for loop) parent directory(es)

    return folder_sizes_dict

def check_parents_depth(folder_sizes_dict): # this is my second, slightly faster attempt at check_parents(), not the fastest I've made, so again, don't use it
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

def check_parents_depth_V2(folder_sizes_dict): # this was my third attempt and I gave up, so don't even try using it because it doesn't even work
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

def check_parents_depth_V3(folder_sizes_dict): # my fourth attempt at check_parents(), superseded my check_parents_recursive(), go use that one
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
"""

def check_parents_recursive(folder_sizes_dict, cd = 0): # also this one is my latest functional attempt at check_parents(). it is orders of magnitude faster than all other attempts
    if len(folder_sizes_dict) > 0:
        if cd == 0: # if we're on the top directory of the whole search
            current_top_directory = str(list(folder_sizes_dict)[0]) # then our top directory is just that, our top directory
        else:
            current_top_directory = str(cd) # otherwise we're treating the input current directory as our top directory as we only want to search below this directory (since this function is recursive)
        
        if len(folder_sizes_dict[current_top_directory]["children"]) > 0: # if the current directory has no sub-directories then we obviously don't need to check any, so we skip the code since the directory is already the right size.
            #try: # we try to run our vectorized code, but if windows is dumb then it won't work
                #folder_sizes_dict[current_top_directory]["size"] += sum([check_parents_recursive(folder_sizes_dict, str(current_top_directory.replace("/", "\\").rstrip("\\") + "\\" + child))[str(current_top_directory.replace("/", "\\").rstrip("\\") + "\\" + child)]["size"] for child in folder_sizes_dict[current_top_directory]["children"]]) # this won't even run if the folder has no children
            
            #except KeyError: # this happens when windows has a hidden system folder that doesn't actually exist
            for child in folder_sizes_dict[current_top_directory]["children"]: # this loop is identical to the vectorized code above, but it will only skip the subfolder that doesn't exist as opposed to skipping the whole current folder due to the key error
                try: # this time the try is for each folder so that we don't skip valid folders
                    folder_sizes_dict[current_top_directory]["size"] += check_parents_recursive(folder_sizes_dict, str(current_top_directory.replace("/", "\\").rstrip("\\") + "\\" + child))[str(current_top_directory.replace("/", "\\").rstrip("\\") + "\\" + child)]["size"]
                except KeyError: # we ignore non-existant folders
                    print("{} is not a real folder\n".format(str(current_top_directory.replace("/", "\\").rstrip("\\") + "\\" + child)))

    return folder_sizes_dict


def check_sizes(folder_sizes_dict, minimum_f_size):
    """
    reorganizes the folder_sizes_dict into a list of tuples, cuts out any folder smaller than minimum_f_size, and counts the number of folders that pass and fail that filter
    """
    folders = list() # list of tuples, (folder from dict, size of folder)
    passes = [0, 0] # fails, passes
    length = len(folder_sizes_dict)
    i = 0 # track where we are so we can print progress
    try:
        print("\nChecking folder sizes for drive "+str(list(folder_sizes_dict)[0])+"...\n")
    except IndexError: # if the dict was empty then this error occurs
        print("\nNon-existant drive...\n")
    for p in folder_sizes_dict: # seperate function           <--- I don't remember why I wrote that there lol
        if folder_sizes_dict[p]["size"] >= minimum_f_size*1000000: # check if the folder we're on passes the minimum size filter
            folders.append(tuple([str(p), int(folder_sizes_dict[p]["size"])])) # if so add it to the folder list along with its size
            passes[1] += 1 # and increment the number of passes
        elif i == 0: # include topmost folder regardless of whether it passes the minimum size or not
            folders.append(tuple([str(p), int(folder_sizes_dict[p]["size"])])) # add it to the list
        else:
            passes[0] += 1 # otherwise the folder failed, increment fails
        i += 1
        print("\r" + str(int((i/length)*10000)/100) + "%", end="") # print progress percentage
    

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

    for letter in alphabet:
        folders = get_file_folder_sizes_V4(letter+":/")
        sizes = check_sizes(folders[0], minimum_folder_size)
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

    with open("Folder_Size_Log.csv", "a") as file:
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
                pass
                


if __name__ == "__main__":
    main()
    end = time.time()
    print("time to run: {} minutes".format(int((end-start)/60)))

