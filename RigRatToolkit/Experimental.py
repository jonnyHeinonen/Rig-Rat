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
#	LabelJoints(*args)
#
# DESCRIPTION:
#	Labels all joints in the scene.
#
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================

def LabelJoints(*args):

	leftPrefix = cmds.textFieldGrp('labelLeftPrefix', query=True, text=True)
	rightPrefix = cmds.textFieldGrp('labelRightPrefix', query=True, text=True)

	selection = cmds.ls(type='joint')

	for joint in selection:

		cmds.setAttr(f'{joint}.type', 18)

	for joint in selection:

		if len(leftPrefix) > 0 and joint[:len(leftPrefix)] == leftPrefix:
			cmds.setAttr(f'{joint}.side', 1)
			cmds.setAttr(f'{joint}.otherType', joint[len(leftPrefix):], type='string')

		elif len(rightPrefix) > 0 and joint[:len(rightPrefix)] == rightPrefix:
			cmds.setAttr(f'{joint}.side', 2)
			cmds.setAttr(f'{joint}.otherType', joint[len(rightPrefix):], type='string')

		else:
			cmds.setAttr(f'{joint}.side', 0)
			cmds.setAttr(f'{joint}.otherType', joint, type='string')

# ====================================================================================================================
#
# SIGNATURE:
#	ConstraintGroups(*args)
#
# DESCRIPTION:
#	Constraint first selection to second selection, eg. select the following in written order: control1 -> control2 -> joint1 -> joint2.
#	Control 1 is constrained to joint 1 and control 2 to joint 2.
#
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================

def ConstraintGroups(*args):

	selection = cmds.ls(sl=True)
	halfList = int(len(selection)/2)

	constraintType = cmds.optionMenuGrp('constraintGroupType', query=True, value=True)
	maintainOffset = cmds.checkBox('constraintGroupsOffset', query=True, value=True)

	for index,item in enumerate(selection[:halfList]):
		if maintainOffset == False:
			if constraintType == 'Parent':
				cmds.parentConstraint(item, selection[index+halfList], maintainOffset=False)
			elif constraintType == 'Point':
				cmds.pointConstraint(item, selection[index+halfList], maintainOffset=False)
			elif constraintType == 'Orient':
				cmds.orientConstraint(item, selection[index+halfList], maintainOffset=False)
		else:
			if constraintType == 'Parent':
				cmds.parentConstraint(item, selection[index+halfList], maintainOffset=True)
			elif constraintType == 'Point':
				cmds.pointConstraint(item, selection[index+halfList], maintainOffset=True)
			elif constraintType == 'Orient':
				cmds.orientConstraint(item, selection[index+halfList], maintainOffset=True)

# ====================================================================================================================
#
# SIGNATURE:
#	ParentGroups(*args)
#
# DESCRIPTION:
#	Parents first selection to second selection, eg. select the following in written order: control1 -> control2 -> joint1 -> joint2.
#	Control 1 is parented to joint 1 and control 2 to joint 2.
#
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================

def ParentGroups(*args):

	selection = cmds.ls(sl=True)
	halfList = int(len(selection)/2)

	for index,item in enumerate(selection[:halfList]):
		cmds.parent(item, selection[index+halfList])