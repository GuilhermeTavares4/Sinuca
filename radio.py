import platform
import os
import threading

# We need a global variable to help us stop sounds manually if needed
_STOP_FLAG = False

def _play_one_file_blocking(filename):
    global _STOP_FLAG
    system = platform.system()
    
    if system == "Windows":
        import winsound
        # Windows allows us to stop sound by playing 'None'
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME)
        except:
            pass # Handle errors gracefully if sound is killed
        
    elif system == "Darwin":  # MacOS
        os.system(f'afplay "{filename}"')
        
    elif system == "Linux":
        os.system(f'aplay "{filename}"')

def _sequence_logic(file_list):
    global _STOP_FLAG
    _STOP_FLAG = False # Reset flag
    for filename in file_list:
        # Check if someone asked to stop the music
        if _STOP_FLAG:
            break
        _play_one_file_blocking(filename)

def play(filename):
    t = threading.Thread(target=_play_one_file_blocking, args=(filename,))
    t.daemon = True  # <--- THIS LINE ensures sound dies when program exits
    t.start()

def play_sequence(file_list):
    t = threading.Thread(target=_sequence_logic, args=(file_list,))
    t.daemon = True  # <--- THIS LINE ensures sound dies when program exits
    t.start()
    return t

def stop_all():
    """
    Forces sound to stop immediately (Best effort).
    """
    global _STOP_FLAG
    _STOP_FLAG = True
    
    system = platform.system()
    if system == "Windows":
        import winsound
        # This special command tells Windows to purge all sounds instantly
        winsound.PlaySound(None, winsound.SND_PURGE)
    elif system == "Darwin":
        os.system("killall afplay") # Force kill audio player
    elif system == "Linux":
        os.system("killall aplay")  # Force kill audio player