import subprocess

def main():
    nostalePID = getNostalePID()
    for pid in nostalePID:
        hexAddr = isMutexAlive(pid)
        if hexAddr:
            print killMutex(pid, hexAddr)
             

    

def getNostalePID():
    nostalePID = []
    process = subprocess.Popen(["TASKLIST","/FO", "CSV"], stdout = subprocess.PIPE, shell=True)

    for line in iter(process.stdout.readline,''):
       if "NostaleClientX.exe" in line.rstrip():
           nostalePID.append(line.rstrip().split('","')[1])
    return nostalePID

def isMutexAlive(PID):
    process = subprocess.Popen([".\\handle64.exe", "-a" ,"-p", PID], stdout = subprocess.PIPE, shell=True)

    for line in iter(process.stdout.readline,''): 
       if "EntwellNostaleClient" in line.rstrip():
           return line.rstrip().split(b":")[0]

    return False

def killMutex(PID, hexAddr):
    process = subprocess.Popen([".\\handle64.exe", "-c" , hexAddr, "-p", PID, "-y"], stdout = subprocess.PIPE, shell=True)

    status = 1

    for line in iter(process.stdout.readline,''):
        if "Handle closed." in line.rstrip():
            status = 0

    return status
    
    
if __name__ == "__main__":
    main()
