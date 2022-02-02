#-------------------------------------------------------------------------------------------------------------------------------------
#
# To use this toolkit -
#
# - Put the "RigRatToolkit" folder in your scripts folder, eg. \Documents\maya\2022\scripts
# - Put the images from the "Icons" folder in your icons folder, eg. \Documents\maya\2022\prefs\icons
# - Create a new button on the Maya shelf with the following code:
#
#-------------------------------------------------------------------------------------------------------------------------------------

# IMPORT FOLDER
import maya.utils
maya.utils.executeDeferred('import RigRatToolkit')

# IMPORT IMPORT LIBRARY
import importlib

# IMPORT THIS MODULE
import RigRatToolkit.Menu
importlib.reload(RigRatToolkit.Menu)

# IMPORT OTHER MODULES
import RigRatToolkit.Controls
importlib.reload(RigRatToolkit.Controls)

import RigRatToolkit.Joints
importlib.reload(RigRatToolkit.Joints)

import RigRatToolkit.IkFk
importlib.reload(RigRatToolkit.IkFk)

import RigRatToolkit.Addons
importlib.reload(RigRatToolkit.Addons)

import RigRatToolkit.Ribbon
importlib.reload(RigRatToolkit.Ribbon)

# RUN FUNCTION
RigRatToolkit.Menu.Window()