import platform
import os
import threading

_STOP_FLAG = False

def _play_one_file_blocking(filename):
    global _STOP_FLAG
    system = platform.system()
    
    if system == "Windows":
        import winsound
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        except:
            pass
        
    elif system == "Darwin": 
        os.system(f'afplay "{filename}"')
        
    elif system == "Linux":
        os.system(f'aplay "{filename}"')

def _sequence_logic(file_list):
    global _STOP_FLAG
    _STOP_FLAG = False
    for filename in file_list:
        if _STOP_FLAG:
            break
        _play_one_file_blocking(filename)

def play(filename):
    t = threading.Thread(target=_play_one_file_blocking, args=(filename,))
    t.daemon = True  
    t.start()

def play_sequence(file_list):
    t = threading.Thread(target=_sequence_logic, args=(file_list,))
    t.daemon = True 
    t.start()
    return t

def stop_all():

    global _STOP_FLAG
    _STOP_FLAG = True
    
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.PlaySound(None, winsound.SND_PURGE)
    elif system == "Darwin":
        os.system("killall afplay")
    elif system == "Linux":
        os.system("killall aplay")