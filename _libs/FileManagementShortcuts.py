import os
import pickle

def outputfolder(*parts):
    print(parts)
    name = os.sep.join(parts) + os.sep
    try:
        os.makedirs(name, exist_ok=True)
    except:
        pass
    return name

def pickleThis(object,filename):
    with open(filename, 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)

def unpickleThis(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)