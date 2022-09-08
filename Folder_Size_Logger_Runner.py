import time as t

with open("Time_In_Seconds.txt", "r") as file:
    time_offset = int(file.readline()) # just reads whatever is on the first line of the file and uses that as the time offset between runs of the logger
time_old = t.time()
time_difference = time_offset

while True:
    t.sleep(1) # wait one second between running the while loop, otherwise it would use more CPU for no reason
    if time_difference >= time_offset: # once time is up
        exec(open("Folder_Size_Logger_V4.py", "r").read()) # run the logger
        time_old = t.time() # reset time
    else:
        print("waiting {} seconds...".format(int(time_offset - time_difference)), end="\r") # print how much time is left until next run
    time_difference = t.time() - time_old # update time remaining
