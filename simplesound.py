import platform
import os
import threading

def _play_sound_logic(filename):
    system = platform.system()

    if system == "Windows":
        import winsound
        # SND_FILENAME means it's a file, SND_ASYNC means don't freeze the program
        winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
    
    elif system == "Darwin":  # MacOS
        # afplay is built into macOS
        os.system(f'afplay "{filename}" &')
        
    elif system == "Linux":
        # aplay is standard on most Linux distros
        os.system(f'aplay "{filename}" &')
    
    else:
        print("Sorry, your operating system is not supported for simple sound.")

def play(filename):
    """
    Plays a .wav file. 
    Usage: simplesound.play("mysound.wav")
    """
    # We run this in a thread so it doesn't freeze your game/program
    t = threading.Thread(target=_play_sound_logic, args=(filename,))
    t.start()