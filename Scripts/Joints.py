# ====================================================================================================================
#
# Rig Rat Toolkit - Joints
#
# ====================================================================================================================
#
# DESCRIPTION:
#	Constains the functions for the "Joints" tab.
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
#	CreateJoints(*args)
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

def CreateJoints(*args):

	# Gather UI data
	jointPrefix = cmds.textFieldGrp('jointPrefix', query=True, text=True)
	if not jointPrefix == '':
		jointPrefix = f'{jointPrefix}_'
	jointDescription = cmds.textFieldGrp('jointDescription', query=True, text=True)
	if jointDescription == '':
		jointDescription = 'joint'
	jointSuffix = cmds.textFieldGrp('jointSuffix', query=True, text=True)
	if not jointSuffix == '':
		jointSuffix = f'_{jointSuffix}'

	jointAmount = cmds.intSliderGrp('jointAmount', query=True, value=True)
	jointSpacing = cmds.floatSliderGrp('jointSpacing', query=True, value=True)
	jointSpacingDirection = cmds.optionMenuGrp('jointSpacingDirection', query=True, value=True)
	invertJointSpacingDirection = cmds.checkBox('invertJointSpacingDirection', query=True, value=True)

	jointRotationOrder = cmds.optionMenuGrp('jointRotationOrder', query=True, value=True)

	# Set joint spacing values
	if invertJointSpacingDirection:
		jointSpacing *= -1
	if jointSpacingDirection == 'X+':
		jointDirection = (jointSpacing,0,0)
	elif jointSpacingDirection == 'Y+':
		jointDirection = (0,jointSpacing,0)
	elif jointSpacingDirection == 'Z+':
		jointDirection = (0,0,jointSpacing)

	# -------------------------------------------------------------------------------------------------------------------
	# Create the joints
	for jointNumber in range(jointAmount):
		if jointAmount > 1:
			
			# Remove numbers at the end of "jointDescription"
			if jointDescription[-2:] == '01':
				jointDescription = jointDescription[:-2]
			if jointNumber < 9:
				jointName = f'{jointPrefix}{jointDescription}0{jointNumber+1}{jointSuffix}'
			else:
				jointName = f'{jointPrefix}{jointDescription}{jointNumber+1}{jointSuffix}'

			# Create the first joint at origo/what the user has selected
			if jointNumber == 0:
				cmds.joint(name=jointName, rotationOrder=jointRotationOrder)
			else:
				cmds.joint(name=jointName, position=jointDirection, relative=True, rotationOrder=jointRotationOrder)
		else:
			jointName = jointPrefix + jointDescription + jointSuffix
			cmds.joint(name=jointName, rotationOrder=jointRotationOrder)

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'undefined', 'undefined', 'undefined', 'undefined')

	cmds.select(clear=True)

# ====================================================================================================================
#
# SIGNATURE:
#	CreateLocatorJointOnCenter(*args)
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

def CreateLocatorJointOnCenter(*args):

	# Gather UI data
	jointRotationOrder = cmds.optionMenuGrp('jointOnCenterRotationOrder', query=True, value=True)
	# A value of 1=locator and 2=joint
	locatorOrJoint = cmds.radioButtonGrp('locatorOrJoint', query=True, select=True)
	locatorJointName = cmds.textFieldGrp('locatorJointName', query=True, text=True)

	selection = cmds.ls(selection=True)
	if not selection:
		cmds.error('Nothing is selected.')

	transformNodes = cmds.ls(transforms=True)
	if locatorJointName in transformNodes:
		cmds.error(f'{locatorJointName} already exists.')

	# Set a default name and add a number to avoid name clashing.
	if not locatorJointName:
		if locatorOrJoint == 1:
			locatorJointName = 'locator1'
			while locatorJointName in transformNodes:
				number = int(locatorJointName[7:])
				locatorJointName = 'locator' + str(number+1)
		if locatorOrJoint == 2:
			locatorJointName = 'joint1'
			while locatorJointName in transformNodes:
				number = int(locatorJointName[5:])
				locatorJointName = 'joint' + str(number+1)

	# -------------------------------------------------------------------------------------------------------------------
	# Create the locator or joint
	cmds.cluster(name='centerPoint_cluster')
	cmds.select(clear=True)
	if locatorOrJoint == 1:
		cmds.spaceLocator(name=locatorJointName)
		cmds.pointConstraint('centerPoint_clusterHandle', locatorJointName, name='tempOnCenterPointConstraint')
	if locatorOrJoint == 2:
		cmds.joint(name=locatorJointName, rotationOrder=jointRotationOrder)
		cmds.pointConstraint('centerPoint_clusterHandle', locatorJointName, name='tempOnCenterPointConstraint')

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'undefined', 'undefined', 'undefined', 'undefined')

	cmds.delete('centerPoint_clusterHandle', 'tempOnCenterPointConstraint')
	cmds.select(clear=True)