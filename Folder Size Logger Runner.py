import time as t

time_offset = 60*60 # seconds
time_old = t.time()
time_difference = time_offset

while True:
    t.sleep(1)
    if time_difference >= time_offset:
        exec(open("Folder_Size_Logger_V4.py", "r").read())
        time_old = t.time()
    else:
        print("waiting {} seconds...".format(int(time_offset - time_difference)), end="\r")
    time_difference = t.time() - time_old
