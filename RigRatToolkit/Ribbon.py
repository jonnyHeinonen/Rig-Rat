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
import math
from RigRatToolkit.Menu import RigRatAttributes

# ====================================================================================================================
#
# SIGNATURE:
#	RibbonUiData(*args)
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

def RibbonUiData(*args):

	transformNodes = cmds.ls(transforms=True)

	ribbonName = cmds.textFieldGrp('ribbonName', query=True, text=True)
	if ribbonName in transformNodes:
		cmds.inViewMessage(assistMessage=f'<hl>{ribbonName} already exists</hl>.', position='midCenter', fade=True, clickKill=True)
		cmds.error(f'{ribbonName} already exists.')
	# Set a default name and add a number to avoid name clashing.
	if not ribbonName:
		ribbonName = 'ribbon1'
		while ribbonName in transformNodes:
			ribbonNumber = int(ribbonName[6:])
			ribbonName = 'ribbon' + str(ribbonNumber+1)

	ribbonLength = cmds.floatSliderGrp('ribbonLength', query=True, value=True)

	# 1=X, 2=Y and 3=Z
	ribbonOrientation = cmds.radioButtonGrp('ribbonOrientation', query=True, select=True)
	if ribbonOrientation == 1:
		ribbonOrientation = (1,0,0)
		controlNormal = (0,0,1)
	elif ribbonOrientation == 2:
		ribbonOrientation = (0,1,0)
		controlNormal = (1,0,0)
	elif ribbonOrientation == 3:
		ribbonOrientation = (0,0,1)
		controlNormal = (1,0,0)

	# A value of 1=horizontal and 2=vertical
	ribbonDirection = cmds.radioButtonGrp('ribbonDirection', query=True, select=True)
	if ribbonDirection == 2:
		if ribbonOrientation == (1,0,0):
			ribbonDirection = (90,0,0)
			controlNormal = (0,1,0)
		elif ribbonOrientation == (0,1,0):
			ribbonDirection = (0,90,0)
			controlNormal = (0,0,1)
		elif ribbonOrientation == (0,0,1):
			ribbonDirection = (0,0,90)
			controlNormal = (0,1,0)
	else:
		ribbonDirection = (0,0,0)

	jointNumber = cmds.intSliderGrp('ribbonJointNumber', query=True, value=True)

	# 1=X, 2=Y and 3=Z
	jointOrientation = cmds.radioButtonGrp('ribbonJointOrient', query=True, select=True)
	invertOrientation = cmds.checkBox('invertRibbonJointOrient', query=True, value=True)
	if jointOrientation == 1:
		jointOrientation = (0,0,0)
		if invertOrientation:
			jointOrientation = (0,180,0)
	elif jointOrientation == 2:
		jointOrientation = (0,0,-90)
		if invertOrientation:
			jointOrientation = (0,0,90)
	elif jointOrientation == 3:
		jointOrientation = (0,90,1)
		if invertOrientation:
			jointOrientation = (0,-90,0)

	addControls = cmds.checkBoxGrp('ribbonAddControls', query=True, value1=True)
	controlColor = cmds.colorIndexSliderGrp('ribbonControlColor', query=True, value=True)-1

	del transformNodes
	ribbonNumber = None
	del ribbonNumber
	#del invertOrientation

	CreateRibbon(ribbonName, ribbonLength, ribbonOrientation, ribbonDirection, controlNormal, jointOrientation, jointNumber, addControls, controlColor)

# ====================================================================================================================
#
# SIGNATURE:
#	CreateRibbon(ribbonName, ribbonLength, ribbonOrientation, ribbonDirection, controlNormal, jointOrientation, jointNumber, addControls, controlColor)
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

def CreateRibbon(ribbonName, ribbonLength, ribbonOrientation, ribbonDirection, controlNormal, jointOrientation, jointNumber, addControls, controlColor):

	# Create the nurbs plane
	cmds.nurbsPlane(name=ribbonName, axis=ribbonOrientation, degree=3, lengthRatio=0.2, patchesU=jointNumber-1, width=ribbonLength, constructionHistory=False)
	cmds.xform(ribbonName, rotation=ribbonDirection, objectSpace=True)
	cmds.makeIdentity(ribbonName, apply=True)

	# Create the follicle group
	follicleGroup = f'{ribbonName}_follicleGroup'
	cmds.group(name=follicleGroup, empty=True)

	# Create the follicles and name them
	for i in range(jointNumber):
		if i < 9:
			follicleShape = f'{ribbonName}_follicle0{i+1}Shape'
			follicleTransform = f'{ribbonName}_follicle0{i+1}'
			jointName = f'{ribbonName}_jnt0{i+1}'
		else:
			follicleShape = f'{ribbonName}_follicle{i+1}Shape'
			follicleTransform = f'{ribbonName}_follicle{i+1}'
			jointName = f'{ribbonName}_jnt{i+1}'
		cmds.createNode('follicle', name=follicleShape)
		cmds.setAttr(f'{follicleShape}.simulationMethod', 0)
		shapeParent = cmds.listRelatives(follicleShape, parent=True)
		cmds.rename(shapeParent, follicleTransform)
		cmds.parent(follicleTransform, follicleGroup)

		# Attach the follicles to the nurbs plane
		cmds.connectAttr(f'{follicleShape}.outRotate', f'{follicleTransform}.rotate', force=True)
		cmds.connectAttr(f'{follicleShape}.outTranslate', f'{follicleTransform}.translate', force=True)
		cmds.connectAttr(f'{ribbonName}.worldMatrix', f'{follicleShape}.inputWorldMatrix')
		cmds.connectAttr(f'{ribbonName}.local', f'{follicleShape}.inputSurface')

		# Place the follicles along the nurbs plane
		cmds.setAttr(f'{follicleTransform}.parameterU', float(i)/(jointNumber-1))
		cmds.setAttr(f'{follicleTransform}.parameterV', 0.5)

		# Create the joints
		cmds.joint(name=jointName, orientation=jointOrientation)
		cmds.matchTransform(jointName, follicleTransform, position=True)

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'ribbon', i+1, 'undefined', 'undefined')

	# Create the setup container
	cmds.group(ribbonName, follicleGroup, name=f'{ribbonName}_grp')

	# -------------------------------------------------------------------------------------------------------------------
	# Add Controls
	# -------------------------------------------------------------------------------------------------------------------
	
	# Add groups for the driver joints and controls
	if addControls:
		cmds.select(clear=True)
		driverGroup = cmds.group(name=f'{ribbonName}_driverGroup', empty=True)
		controlGroup = cmds.group(name=f'{ribbonName}_controlGroup', empty=True)

		# Get the 2 (if even) or 3 (if uneven) joints
		if jointNumber < 10:
			lastJoint = f'{ribbonName}_jnt0{jointNumber}'
		else:
			lastJoint = f'{ribbonName}_jnt{jointNumber}'

		if jointNumber % 2 == 0:
			jointList = [f'{ribbonName}_jnt01', lastJoint]

		else:
			if jointNumber < 19:
				midJoint = f'{ribbonName}_jnt0{math.ceil(jointNumber * 0.5)}'
			else:
				midJoint = f'{ribbonName}_jnt{math.ceil(jointNumber * 0.5)}'
			jointList = [f'{ribbonName}_jnt01', midJoint, lastJoint]

		# Create the driver joints and control names
		driverJoints = []
		for joint in jointList:
			jointName = f'{joint[:-5]}driverJnt{joint[-2:]}'
			controlName = f'{joint[:-5]}ctrl{joint[-2:]}'
			fixGroupName = f'{joint[:-5]}fixGroup{joint[-2:]}'

			# Create the driver joints
			cmds.duplicate(joint, name=jointName, parentOnly=True)
			cmds.parent(jointName, world=True)

			# Edit Rig Rat Attributes
			RigRatAttributes(jointName, 'joint', 'ribbonDriver', jointList.index(joint)+1, 'undefined', 'undefined')

			# Create the fixGroups and controls
			cmds.group(name=fixGroupName, empty=True)
			cmds.matchTransform(fixGroupName, jointName)
			cmds.circle(name=controlName, normal=controlNormal, radius=ribbonLength*0.15, constructionHistory=False)
			cmds.matchTransform(controlName, fixGroupName, position=True)
			cmds.parent(controlName, fixGroupName)
			cmds.makeIdentity(controlName, apply=True)
			cmds.setAttr(f'{controlName}.overrideEnabled', 1)
			cmds.setAttr(controlName+'.overrideColor', controlColor)

			# Edit Rig Rat Attributes
			RigRatAttributes(controlName, 'control', 'ribbonDriver', jointList.index(joint)+1, 'undefined', 'undefined')

			# Parent and constraint
			cmds.parent(jointName, driverGroup)
			cmds.parent(fixGroupName, controlGroup)

			cmds.parentConstraint(controlName, jointName)

			driverJoints.append(jointName)

		# Parent to the setup container
		cmds.parent(driverGroup, controlGroup, f'{ribbonName}_grp')

		# Skin the driver joints to the nurbs plane
		cmds.select(clear=True)
		cmds.select(driverJoints)
		cmds.select(ribbonName, add=True)
		cmds.skinCluster(name=f'{ribbonName}_skinCluster', bindMethod=0, maximumInfluences=4, normalizeWeights=1, obeyMaxInfluences=True, removeUnusedInfluence=True, toSelectedBones=True)

	cmds.select(clear=True)