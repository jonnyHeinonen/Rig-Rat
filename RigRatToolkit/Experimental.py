# ====================================================================================================================
#
# Rig Rat Toolkit - IKFK
#
# ====================================================================================================================
#
# DESCRIPTION:
#	Constains the functions for the "IKFK" tab.
#
# REQUIRES:
#	Nothing
#
# ====================================================================================================================

import maya.cmds as cmds
from RigRatToolkit.Menu import RigRatAttributes

# ====================================================================================================================
#
# SIGNATURE:
#	IkFkUiData(*args)
#
# DESCRIPTION:
#	
#
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================
"""
def EyelidJoints(*args):

	eyeJoint = cmds.textFieldGrp('eyeJointName', query=True, text=True)

	# A value of 1=Upper and 2=Lower
	upperLower = cmds.radioButtonGrp('upperLowerEyelid', query=True, select=True)
	if upperLower == 1:
		upperLower = 'Upper'
	elif upperLower == 2:
		upperLower = 'Lower'

	vertecies = cmds.ls(selection=True, flatten=True)

	eyelidGroup = cmds.group(name=f'{eyeJoint[:2]}eyelid{upperLower}Joints_grp', empty=True)

	for vertex in vertecies:

		# Number added to the joint name
		if vertecies.index(vertex) < 9:
			jointNumber = '0' + str(vertecies.index(vertex)+1)
		else:
			jointNumber = str(vertecies.index(vertex)+1)

		# Create the center joint
		cmds.select(clear=True)
		centerJoint = cmds.joint(name=f'{eyeJoint[:2]}eyelid{upperLower}Center{jointNumber}_jnt')
		pos = cmds.xform(eyeJoint, query=True, worldSpace=True, translation=True)
		cmds.xform(centerJoint, worldSpace=True, translation=pos)

		# Create the eyelid joint
		tipJoint = cmds.joint(name=f'{eyeJoint[:2]}eyelid{upperLower}Tip{jointNumber}_jnt')
		pos = cmds.xform(vertex, query=True, worldSpace=True, translation=True)
		cmds.xform(tipJoint, worldSpace=True, translation=pos)

		# Orient center joint
		cmds.joint(centerJoint, edit=True, orientJoint='xyz', secondaryAxisOrient='yup', children=True, zeroScaleOrient=True)

		cmds.parent(centerJoint, eyelidGroup)

def EyelidReorderNumbers(*args):

	selection = cmds.ls(selection=True, long=True)

	number = int(len(selection)/2 + 1)
	print(number)

	for joint in selection:

		newName = joint.split('|')[-1]
		print(newName)

		if selection.index(joint) % 2 == 0:
			number -= 1

			print(joint)
		if number < 10:
			cmds.rename(joint, f'{newName[:-6]}0{str(number)}_jnt')

		else:
			cmds.rename(joint, f'{newName[:-6]}{str(number)}_jnt')

	selection = cmds.ls(selection=True, shortNames=True)

	for joint in selection:

		if joint[-1] == '1':
			cmds.rename(joint, joint[:-1])

def EyelidLocators(*args):

	upObject = cmds.textFieldGrp('eyelidUpObject', query=True, text=True)

	selection = cmds.ls(selection=True)

	locatorGroup = cmds.group(name=f'{selection[0][:13]}Locator_grp', empty=True)

	for joint in selection:

		locator = cmds.spaceLocator(name=f'{joint[:13]}{joint[16:19]}loc')[0]
		pos = cmds.xform(joint, query=True, worldSpace=True, translation=True)
		cmds.xform(locator, worldSpace=True, translation=pos)

		jointParent = cmds.listRelatives(joint, parent=True)[0]

		cmds.aimConstraint(locator, jointParent, maintainOffset=True, weight=1, aimVector=(1,0,0), upVector=(0,1,0), worldUpType='object', worldUpObject=upObject)

		cmds.parent(locator, locatorGroup)

	cmds.select(clear=True)
"""