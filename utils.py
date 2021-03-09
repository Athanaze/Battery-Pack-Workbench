import uuid # Included in the standard library
from preferences import *
'''
Source : <https://wiki.freecadweb.org/Object_name>

In summary, the Name essentially acts like a unique identifier (UID) for an object.
Since a unique Name is very restrictive, all objects also have a Label property
which allows "renaming" the object to something more descriptive.

The internal Name actually remains fixed, but the user editable
Label can be used in most situations where the Name would be used.

In common usage in the program and the documentation,
"renaming" means changing the Label and not the actual Name of the object.

/!\ The Name cannot start with a number;
    it must start with a letter or the underscore, [_a-zA-Z]

'''
def generate_freecad_name():
    s = str(uuid.uuid4())
    if s[0] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return generate_freecad_name()
    
    else:
        return s

def get_mod_path(fdir):
    return fdir + "Mod/"+MOD_FOLDER_NAME+"/"