import os, secrets, string, time
from flag import flag


def main():
    # It's a tiny server...
    blob = bytearray(2**16)
    files = {}
    used = 0

    # Use deduplication to save space.
    def store(data):
        nonlocal used
        """
        NONNLOCAL
        def myfunc1():
          x = "John"
          def myfunc2():
            nonlocal x
            x = "hello"
          myfunc2() 
          return x
        print(myfunc1())
        """
        MINIMUM_BLOCK = 16
        MAXIMUM_BLOCK = 1024
        part_list = []
        while data:
            prefix = data[:MINIMUM_BLOCK]
            #perfin 16 spaces
            ind = -1
            bestlen, bestind = 0, -1
            while True:
                ind = blob.find(prefix, ind+1)
                #la funcion find no se encuentra
                if ind == -1: break
                ##no se lena sale
                length = len(os.path.commonprefix([data, bytes(blob[ind:ind+MAXIMUM_BLOCK])]))
                ##longest common path prefix in a list of paths 
                if length > bestlen:
                    #-1>0
                    bestlen, bestind = length, ind
                    #fijamso como el nuevo bestlengh

            if bestind != -1:
                part, data = data[:bestlen], data[bestlen:]
                ##[1,2,3]=> part =[1,2], data=[3]
                part_list.append((bestind, bestlen))
                #part_list #line 27 is empty 
            ##
            ## bestind not neg
            ##                
            else:
                part, data = data[:MINIMUM_BLOCK], data[MINIMUM_BLOCK:]
                # part = [1,1,2]
                # data = [3]
                ###
                ### Blob : bytearray(2**16) before
                ### 
                blob[used:used+len(part)] = part
                ##(0,data[min:])=(0,[16])
                part_list.append((used, len(part)))
                ##
                used += len(part)
                ## se lanzará una excepción
                assert used <= len(blob)

        fid = "".join(secrets.choice(string.ascii_letters+string.digits) for i in range(16))
        """
        >>> import string
        >>> print(string.ascii_letters)
        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
        >>> print(string.digits)
        0123456789
        >>> import secrets
        >>> print(''.join(secrets.choice(string.ascii_letters) for i in range (10)))
        XcpqEbUwNg
        """
       
        files[fid] = part_list
        return fid

    def load(fid):
        data = []
        ###string aleatorio XcpqEbUwNg =fid
        for ind, length in files[fid]:
           ####ind=12, length
           data.append(blob[ind:ind+length])
        return b"".join(data)

    print("Welcome to our file storage solution.")

    # Store the flag as one of the files.
    store(bytes(flag, "utf-8"))

    while True:
        print()
        print("Menu:")
        print("- load")
        print("- store")
        print("- status")
        print("- exi    ")
        choice = input().strip().lower()
        if choice == "load":
            print("Send me the file id...")
            fid = input().strip()
            data = load(fid)
            print(data.decode())
        elif choice == "store":
            print("Send me a line of data...")
            data = input().strip()
            fid = store(bytes(data, "utf-8"))
            print("Stored! Here's your file id:")
            print(fid)
        elif choice == "status":
            print("User: ctfplayer")
            print("Time: %s" % time.asctime())
            kb = used / 1024.0
            kb_all = len(blob) / 1024.0
            print("Quota: %0.3fkB/%0.3fkB" % (kb, kb_all))
            print("Files: %d" % len(files))
        elif choice == "exit":
            break
        else:
            print("Nope.")
            break

try:
    main()
except Exception:
    print("Nope.")
time.sleep(1)
