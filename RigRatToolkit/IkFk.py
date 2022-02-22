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

def IkFkUiData(*args):

	# A value of 1=FK and 2=IK/FK
	fkOrIkFk = cmds.radioButtonGrp('fkOrIkFk', query=True, select=True)

	# Gives one of the following: 'Biped - Arm', 'Biped - Leg', 'Quadruped - Front', 'Quadruped - Rear'
	systemChoice = cmds.optionMenuGrp('ikFkSystemChoice', query=True, value=True)

	# Gives one of the following: 'Left', 'Right', 'Center'
	side = cmds.optionMenuGrp('sideChoice', query=True, value=True)

	# Set IK/FK global control and fixGroup names
	customGlobalControlName = cmds.textFieldGrp('customGlobalControlName', query=True, text=True)
	if systemChoice == 'Biped - Arm':
		globalControlName = f'{side[0].lower()}_arm_ctrl'
		globalFixGroupName = f'{side[0].lower()}_arm_fixGroup'
	elif systemChoice == 'Biped - Leg':
		globalControlName = f'{side[0].lower()}_leg_ctrl'
		globalFixGroupName = f'{side[0].lower()}_leg_fixGroup'
	transformNodes = cmds.ls(transforms=True)
	# Set the names to the custom input
	if not customGlobalControlName == '':
		customControlUnderscoreIndexList = []
		for index,letter in enumerate(customGlobalControlName):
			if letter == '_':
				customControlUnderscoreIndexList.append(index)
		if customControlUnderscoreIndexList:
			globalFixGroupName = f'{customGlobalControlName[:customControlUnderscoreIndexList[-1]]}_fixGroup'
		else:
			globalFixGroupName = f'{customGlobalControlName}_fixGroup'
		globalControlName = customGlobalControlName
	# Alert the user if it already exists and stop the script
	if globalControlName in transformNodes:
		cmds.inViewMessage(assistMessage=f'<hl>{globalControlName} already exists</hl>.', position='midCenter', fade=True, clickKill=True)
		cmds.error(f'{globalControlName} already exists.')
	if globalFixGroupName in transformNodes:
		cmds.inViewMessage(assistMessage=f'<hl>{globalFixGroupName} already exists</hl>.', position='midCenter', fade=True, clickKill=True)
		cmds.error(f'{globalFixGroupName} already exists.')

	# 1=joint and 2=world
	ikControlOrientation = cmds.radioButtonGrp('ikControlOrientation', query=True, select=True)

	# 0=Off and 1=On
	twistOption = cmds.checkBoxGrp('twistStretchCheck', query=True, value1=True)
	if not cmds.checkBoxGrp('twistStretchCheck', query=True, enable=True):
		twistOption = 0
	stretchOption = cmds.checkBoxGrp('twistStretchCheck', query=True, value2=True)
	if not cmds.checkBoxGrp('twistStretchCheck', query=True, enable=True):
		stretchOption = 0

	twistJointAmount = cmds.intSliderGrp('twistJointAmount', query=True, value=True)

	# 1=X, 2=Y and 3=Z
	jointPrimaryAxisChoice = cmds.radioButtonGrp('jointPrimaryAxis', query=True, select=True)
	invertPrimaryAxis = cmds.checkBox('invertJointPrimaryAxis', query=True, value=True)
	if jointPrimaryAxisChoice == 1:
		jointPrimaryAxis = (1,0,0)
		if invertPrimaryAxis:
			jointPrimaryAxis = (-1,0,0)
	elif jointPrimaryAxisChoice == 2:
		jointPrimaryAxis = (0,1,0)
		if invertPrimaryAxis:
			jointPrimaryAxis = (0,-1,0)
	elif jointPrimaryAxisChoice == 3:
		jointPrimaryAxis = (0,0,1)
		if invertPrimaryAxis:
			jointPrimaryAxis = (0,0,-1)

	controlColor = cmds.colorIndexSliderGrp('ikFkControlColor', query=True, value=True)-1
	controlSize = cmds.floatSliderGrp('ikFkControlSize', query=True, value=True)

	selection = cmds.ls(selection=True, type='joint')
	if not len(selection) == 2:
		cmds.error('Please select the start then the end joint.')

	jointChildren = cmds.listRelatives(selection[0], allDescendents=True, type='joint')
	if not selection[1] in jointChildren:
		cmds.error('Please select two joints in the same hierarchy.')
	jointChildren.reverse()

	endJointIndex = jointChildren.index(selection[1])
	jointHierarchy = [selection[0]] + jointChildren[:endJointIndex+1]

	# -------------------------------------------------------------------------------------------------------------------
	# Delete unused variables
	del customGlobalControlName
	del transformNodes
	controlNumber = None
	del controlNumber
	fixGroupNumber = None
	del fixGroupNumber
	customControlUnderscoreIndexList = None
	del customControlUnderscoreIndexList
	del jointPrimaryAxisChoice
	del invertPrimaryAxis
	del selection
	del jointChildren
	del endJointIndex

	# -------------------------------------------------------------------------------------------------------------------
	if fkOrIkFk == 1:
		FkSystem(jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
	elif fkOrIkFk == 2 and 'Biped' in systemChoice:
		IkFkBipedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, stretchOption, jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
	elif fkOrIkFk == 2 and 'Quadruped' in systemChoice:
		IkFkQuadrupedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, stretchOption, jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
	if twistOption == 1 and 'Biped' in systemChoice:
		TwistBipedSetup(systemChoice, side, globalControlName, twistJointAmount, jointPrimaryAxis, jointHierarchy)
	if stretchOption == 1 and 'Biped' in systemChoice:
		StretchBipedSetup(systemChoice, side, globalControlName, jointPrimaryAxis, jointHierarchy)

# ====================================================================================================================
#
# SIGNATURE:
#	FkSystem(jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
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

def FkSystem(jointPrimaryAxis, controlColor, controlSize, jointHierarchy):

	cmds.select(clear=True)

	for joint in jointHierarchy:

		# Create the joint
		jointUnderscoreIndexList = []
		for index,letter in enumerate(joint):
			if letter == '_':
				jointUnderscoreIndexList.append(index)
		jointName = f'{joint[:jointUnderscoreIndexList[0]]}_fk{joint[jointUnderscoreIndexList[0]:]}'
		if '_result_' in jointName:
			jointName = jointName.replace('_result', '')
		cmds.duplicate(joint, name=jointName, parentOnly=True)
		if not joint == jointHierarchy[0]:
			cmds.parent(jointName, previousJoint)

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'fk', str(jointHierarchy.index(joint)+1), 'undefined', 'undefined')
		
		# -------------------------------------------------------------------------------------------------------------------
		# Find the suffix (the last '_' in the joint name) and create the control name
		jointNameUnderscoreIndexList = []
		for index,letter in enumerate(jointName):
			if letter == '_':
				jointNameUnderscoreIndexList.append(index)
		controlName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_ctrl'
		fixGroupName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_fixGroup'

		# Create the control
		cmds.circle(normal=jointPrimaryAxis, radius=controlSize, name=controlName, constructionHistory=False)
		cmds.group(controlName, name=fixGroupName)
		cmds.matchTransform(fixGroupName, joint)
		cmds.setAttr(controlName+'.overrideEnabled', 1)
		cmds.setAttr(controlName+'.overrideColor', controlColor)

		# Edit Rig Rat Attributes
		RigRatAttributes(controlName, 'control', 'fk', str(jointHierarchy.index(joint)+1), 'undefined', 'undefined')

		# Create the system holder group
		if joint == jointHierarchy[0]:
			systemsGroupContainer = f'FK_SYSTEM_{jointName}'
			cmds.group(jointName, name=systemsGroupContainer, world=True)
		cmds.parent(fixGroupName, systemsGroupContainer)

		cmds.parentConstraint(controlName, jointName)
		cmds.parentConstraint(jointName, joint)

		# Parent constraint controls to each other based on hierarchy
		if not joint == jointHierarchy[0]:
			cmds.parentConstraint(previousControl, fixGroupName, maintainOffset=True)

		previousJoint = jointName
		previousControl = controlName

	cmds.select(clear=True)

# ====================================================================================================================
#
# SIGNATURE:
#	IkFkBipedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, stretchOption, jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
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

def IkFkBipedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, stretchOption, jointPrimaryAxis, controlColor, controlSize, jointHierarchy):

	# List the created IK and FK joints
	createdJoints = []

	for ikFk in ['_fk','_ik']:
		cmds.select(clear=True)

		for joint in jointHierarchy:

			# Create the joint
			jointUnderscoreIndexList = []
			for index,letter in enumerate(joint):
				if letter == '_':
					jointUnderscoreIndexList.append(index)
			jointName = joint[:jointUnderscoreIndexList[0]] + ikFk + joint[jointUnderscoreIndexList[0]:]
			if '_result_' in jointName:
				jointName = jointName.replace('_result', '')
			cmds.duplicate(joint, name=jointName, parentOnly=True)
			if not joint == jointHierarchy[0]:
				cmds.parent(jointName, previousJoint)

			# Edit Rig Rat Attributes
			RigRatAttributes(jointName, 'joint', ikFk[1:], str(jointHierarchy.index(joint)+1), side.lower(), systemChoice[8:].lower())

			# -------------------------------------------------------------------------------------------------------------------
			# Find the suffix (the last '_' in the joint name) and create the control name
			jointNameUnderscoreIndexList = []
			for index,letter in enumerate(jointName):
				if letter == '_':
					jointNameUnderscoreIndexList.append(index)
			controlName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_ctrl'
			fixGroupName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_fixGroup'

			# -------------------------------------------------------------------------------------------------------------------
			if ikFk == '_fk':
				# Create the FK control
				cmds.circle(normal=jointPrimaryAxis, radius=controlSize, name=controlName, constructionHistory=False)
				cmds.group(controlName, name=fixGroupName)
				cmds.matchTransform(fixGroupName, joint)
				cmds.setAttr(controlName+'.overrideEnabled', 1)
				cmds.setAttr(controlName+'.overrideColor', controlColor)

				# Edit Rig Rat Attributes
				RigRatAttributes(controlName, 'control', 'fk', str(jointHierarchy.index(joint)+1), side.lower(), systemChoice[8:].lower())

				# Create and parent the first FK joint the "SYSTEMS" holder group
				if joint == jointHierarchy[0]:
					systemsGroupContainer = f'{side.upper()}_{systemChoice[8:].upper()}_SYSTEMS'
					cmds.group(jointName, name=systemsGroupContainer, world=True)
					controlsGroupContainer = f'{side.upper()}_{systemChoice[8:].upper()}_CTRLS'
					cmds.group(name=controlsGroupContainer, empty=True, world=True)
				# Create and parent the FK controls to the "CTRLS" holder group
				cmds.parent(fixGroupName, controlsGroupContainer)

				# Constraint FK controls to joints
				cmds.parentConstraint(controlName, jointName)
				# Parent constraint controls to each other based on hierarchy
				if not joint == jointHierarchy[0]:
					cmds.parentConstraint(previousControl, fixGroupName, maintainOffset=True)

			previousJoint = jointName
			previousControl = controlName

			# -------------------------------------------------------------------------------------------------------------------
			if ikFk == '_ik':
				# Constraint the IK and FK joints to the base joints
				cmds.orientConstraint(jointName, jointName.replace('_ik_', '_fk_'), joint, weight=0.0)
				if stretchOption == 1:
					cmds.pointConstraint(jointName, jointName.replace('_ik_', '_fk_'), joint, weight=0.0)
			
			# If on the last loop in the "['_fk','_ik']" and "jointHierarchy" loop
			if ikFk == '_ik' and joint == jointHierarchy[-1]:

				# Ik control
				cmds.curve(degree=1, name=controlName, point=( (0,0,1.5), (-1.5,0,0), (0,0,-1.5), (1.5,0,0), (0,0,1.5) ), knot=(0,1,2,3,4))
				cmds.rename(cmds.listRelatives(controlName, shapes=True), controlName+'Shape')
				
				# Pole vector control
				poleVectorJointName = createdJoints[4]
				poleVectorJointUnderscoreIndexList = []
				for index,letter in enumerate(poleVectorJointName):
					if letter == '_':
						poleVectorJointUnderscoreIndexList.append(index)
				poleVectorControlName = f'{poleVectorJointName[:poleVectorJointUnderscoreIndexList[-1]]}_ctrl'
				cmds.curve(degree=1, name=poleVectorControlName, knot=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),
							point=( (0,0.75,0), (0,0.5,-0.5), (0,0,-0.75), (0,-0.5,-0.5), (0,-0.75,0), (0,-0.5,0.5), (0,0,0.75), (0,0.5,0.5), (0,0.75,0), (0.5,0.5,0), (0.75,0,0), (0.5,-0.5,0), (0,-0.75,0), (-0.5,-0.5,0), (-0.75,0,0), (-0.5,0.5,0), (0,0.75,0) ))
				cmds.rename(cmds.listRelatives(poleVectorControlName, shapes=True), poleVectorControlName+'Shape')
				
				# Global control (IK/FK switch)
				cmds.curve(degree=3, name='globalCtrlHead', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
					point=( (0.324,0,0.586), (0.324,0,0.586), (0.324,0,0.586), (0.35,0,0.41), (0.54,0,0.41), (0.756,0,0.41), (0.972,0,-0.02), (0.756,0,-0.545), (0.324,0,-0.803), (-0.324,0,-0.803), (-0.756,0,-0.545), (-0.972,0,-0.02), (-0.756,0,0.41), (-0.54,0,0.41), (-0.35,0,0.41), (-0.324,0,0.586), (-0.324,0,0.586), (-0.324,0,0.586) ))
				cmds.curve(degree=3, name='globalCtrlNose', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
					point=( (0,0,0.2), (0,0,0.2), (0,0,0.2), (-0.12,0,0.31), (-0.14,0,0.52), (0,0,0.39), (0.14,0,0.52), (0.12,0,0.31), (0,0,0.2), (0,0,0.2), (0,0,0.2) ))
				cmds.curve(degree=3, name='globalCtrlTeeth', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
					point=( (0.324,0,0.587), (0.324,0,0.587), (0.324,0,0.587), (0.317,0,0.778), (0.141,0,0.643), (0,0,0.803), (-0.141,0,0.643), (-0.317,0,0.778), (-0.324,0,0.587), (-0.324,0,0.587), (-0.324,0,0.587) ))
				for eye in ['globalCtrlLeftEye', 'globalCtrlRightEye']:
					cmds.circle(normal=(0,1,0), radius=1, name=eye, constructionHistory=False)
				cvNum = 0
				for point in [(-0.367,0,-0.344), (-0.551,0,-0.269), (-0.627,0,-0.033), (-0.6,0,0.203), (-0.367,0,0.301), (-0.134,0,0.203), (-0.107,0,-0.033), (-0.183,0,-0.269)]:
					cmds.xform(f'globalCtrlLeftEye.cv[{cvNum}]', translation=point)
					cvNum += 1
				cvNum = 0
				for point in [(0.367,0,-0.344), (0.551,0,-0.269), (0.627,0,-0.033), (0.6,0,0.203), (0.367,0,0.301), (0.134,0,0.203), (0.107,0,-0.033), (0.183,0,-0.269)]:
					cmds.xform(f'globalCtrlRightEye.cv[{cvNum}]', translation=point)
					cvNum += 1
				del cvNum

				for shape in ['globalCtrlHead', 'globalCtrlNose', 'globalCtrlTeeth', 'globalCtrlLeftEye', 'globalCtrlRightEye']:
					cmds.rename(cmds.listRelatives(shape, shapes=True), f'{globalControlName}{shape[10:]}Shape')
				cmds.parent(cmds.listRelatives('globalCtrlNose', 'globalCtrlTeeth', 'globalCtrlLeftEye', 'globalCtrlRightEye', shapes=True), 'globalCtrlHead', shape=True, relative=True)
				cmds.delete('globalCtrlNose', 'globalCtrlTeeth', 'globalCtrlLeftEye', 'globalCtrlRightEye')
				cmds.rename('globalCtrlHead', globalControlName)
				cmds.addAttr(globalControlName, longName='IK_FK', keyable=True, attributeType='float', min=0, max=1, defaultValue=0)
				
				# -------------------------------------------------------------------------------------------------------------------
				# Adjust controls and group them
				for i in ['X','Y','Z']:
					cmds.setAttr(controlName+'.scale'+i, controlSize)
					cmds.setAttr(poleVectorControlName+'.scale'+i, controlSize)
					cmds.setAttr(globalControlName+'.scale'+i, controlSize)
				cmds.group(controlName, name=fixGroupName)
				poleVectorFixGroupName = f'{poleVectorJointName[:poleVectorJointUnderscoreIndexList[-1]]}_fixGroup'
				cmds.group(poleVectorControlName, name=poleVectorFixGroupName)
				cmds.group(name=globalFixGroupName, empty=True)
				cmds.parent(globalControlName, globalFixGroupName)

				if ikControlOrientation == 1:
					cmds.matchTransform(fixGroupName, jointName)
					if jointPrimaryAxis==(1,0,0) or jointPrimaryAxis==(-1,0,0):
						cmds.setAttr(controlName+'.rotateZ', 90)
					elif jointPrimaryAxis==(0,0,1) or jointPrimaryAxis==(0,0,-1):
						cmds.setAttr(controlName+'.rotateX', 90)
				elif ikControlOrientation == 2:
					cmds.matchTransform(fixGroupName, jointName, position=True, rotation=False, scale=False)

				cmds.setAttr(globalControlName+'.rotateX', 90)
				cmds.matchTransform(poleVectorFixGroupName, poleVectorJointName)
				cmds.makeIdentity(controlName, apply=True, translate=False, rotate=True, scale=True)
				cmds.makeIdentity(poleVectorControlName, apply=True, translate=False, rotate=False, scale=True)
				cmds.makeIdentity(globalControlName, apply=True, translate=False, rotate=True, scale=True)

				controlsToEdit = [controlName, poleVectorControlName]
				for control in controlsToEdit:
					cmds.setAttr(f'{control}.overrideEnabled', 1)
					cmds.setAttr(f'{control}.overrideColor', controlColor)
					# Edit Rig Rat Attributes
					RigRatAttributes(control, 'control', 'ik', str(controlsToEdit.index(control)+1), side.lower(), systemChoice[8:].lower())
				cmds.setAttr(f'{globalControlName}.overrideEnabled', 1)
				cmds.setAttr(f'{globalControlName}.overrideColor', controlColor)
				RigRatAttributes(globalControlName, 'control', 'global', 'undefined', side.lower(), systemChoice[8:].lower())

				# -------------------------------------------------------------------------------------------------------------------
				# Constraints and IK handle
				ikHandleName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_hdl'
				cmds.ikHandle(name=ikHandleName, solver='ikRPsolver', startJoint=createdJoints[3], endEffector=jointName)
				cmds.parent(ikHandleName, controlName)
				cmds.orientConstraint(controlName, jointName, maintainOffset=True)
				cmds.poleVectorConstraint(poleVectorControlName, ikHandleName)
				cmds.pointConstraint(joint, globalFixGroupName)

				# Set up IK/FK switch
				switchReverseNode = f'{side.lower()}_{systemChoice[8:].lower()}_ikFk_reverse'
				cmds.createNode('reverse', name=switchReverseNode)
				cmds.connectAttr(f'{globalControlName}.IK_FK', f'{switchReverseNode}.input.inputX', force=True)

				# Parent everything IK related to the "SYSTEMS" and "CTRLS" holder groups
				cmds.parent(createdJoints[3], systemsGroupContainer)
				cmds.parent(fixGroupName, controlsGroupContainer)
				cmds.parent(poleVectorFixGroupName, controlsGroupContainer)
				cmds.parent(globalFixGroupName, controlsGroupContainer)

			createdJoints.append(jointName)

	# -------------------------------------------------------------------------------------------------------------------
	# Complete IK / FK switch connections
	for joint in jointHierarchy:
		for ikFk in ['_fk','_ik']:

			# Find index where "joint" prefix starts
			jointUnderscoreIndexList = []
			for index,letter in enumerate(joint):
				if letter == '_':
					jointUnderscoreIndexList.append(index)
			jointName = joint[:jointUnderscoreIndexList[0]] + ikFk + joint[jointUnderscoreIndexList[0]:]
			if '_result_' in jointName:
				jointName = jointName.replace('_result', '')

			# Find index where "jointName" suffix starts
			jointNameUnderscoreIndexList = []
			for index,letter in enumerate(jointName):
				if letter == '_':
					jointNameUnderscoreIndexList.append(index)
			controlName = f'{jointName[:jointNameUnderscoreIndexList[-1]]}_ctrl'

			# Connect the IK/FK switch and reverse node to the constraints and control visibilities
			if ikFk == '_fk':
				cmds.connectAttr(f'{globalControlName}.IK_FK', f'{joint}_orientConstraint1.{jointName}W1', force=True)
				if stretchOption == 1:
					cmds.connectAttr(f'{globalControlName}.IK_FK', f'{joint}_pointConstraint1.{jointName}W1', force=True)
				cmds.connectAttr(f'{globalControlName}.IK_FK', f'{controlName}.visibility', force=True)
			elif ikFk == '_ik':
				cmds.connectAttr(f'{switchReverseNode}.output.outputX', f'{joint}_orientConstraint1.{jointName}W0', force=True)
				if stretchOption == 1:
					cmds.connectAttr(f'{switchReverseNode}.output.outputX', f'{joint}_pointConstraint1.{jointName}W0', force=True)
				if joint == jointHierarchy[-1]:
					cmds.connectAttr(f'{switchReverseNode}.output.outputX', f'{controlName}.visibility', force=True)
					cmds.connectAttr(f'{switchReverseNode}.output.outputX', f'{poleVectorControlName}.visibility', force=True)
	
	cmds.select(clear=True)

# ====================================================================================================================
#
# SIGNATURE:
#	IkFkQuadrupedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, jointPrimaryAxis, controlColor, controlSize, jointHierarchy)
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

def IkFkQuadrupedSystem(systemChoice, side, globalControlName, globalFixGroupName, ikControlOrientation, jointPrimaryAxis, controlColor, controlSize, jointHierarchy):
	print('IkFkQuad')

# ====================================================================================================================
#
# SIGNATURE:
#	TwistBipedSetup(systemChoice, side, globalControlName, twistJointAmount, jointPrimaryAxis, jointHierarchy)
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

def TwistBipedSetup(systemChoice, side, globalControlName, twistJointAmount, jointPrimaryAxis, jointHierarchy):

	# -------------------------------------------------------------------------------------------------------------------
	# FIRST SECTION (eg. shoulder to elbow)
	# -------------------------------------------------------------------------------------------------------------------

	# Find index where suffix starts in first joint
	jointUnderscoreIndexList = []
	for index,letter in enumerate(jointHierarchy[0]):
		if letter == '_':
			jointUnderscoreIndexList.append(index)

	# Create twist resultGrp, fixGroup, distance Group and a group container for these groups
	resultGroupName = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twists_results'
	if '_result_' in resultGroupName:
		resultGroupName = resultGroupName.replace('_result_', '_')
	fixGroupName = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twists_fixGrp'
	distanceGroup = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twistsDistance_holder'
	twistGroupsContainer = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twists_group'
	for group in [resultGroupName, fixGroupName, distanceGroup, twistGroupsContainer]:
		cmds.group(name=group, empty=True)
		cmds.matchTransform(group, jointHierarchy[0])
	cmds.parent(resultGroupName, fixGroupName)
	cmds.parent(fixGroupName, distanceGroup, twistGroupsContainer)


	# Parent to "SYSTEMS" holder group
	systemsGroupContainer = f'{side.upper()}_{systemChoice[8:].upper()}_SYSTEMS'
	cmds.parent(twistGroupsContainer, systemsGroupContainer)

	# Measure the distance between the first and second joint (eg. shoulder and elbow)
	startPoint = cmds.xform(jointHierarchy[0], query=True, translation=True, worldSpace=True)
	endPoint = cmds.xform(jointHierarchy[1], query=True, translation=True, worldSpace=True)
	cmds.distanceDimension(startPoint=startPoint, endPoint=endPoint)
	totalDistance = cmds.getAttr('distanceDimension1.distance')
	distancePerJoint = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twistPlacement_divide'
	cmds.createNode('multiplyDivide', skipSelect=True, name=distancePerJoint)
	cmds.setAttr(f'{distancePerJoint}.operation', 2)
	cmds.connectAttr('distanceDimension1.distance', f'{distancePerJoint}.input1.input1X')
	cmds.setAttr(f'{distancePerJoint}.input2.input2X', twistJointAmount)

	# Group and constrain distance measuring nodes
	cmds.parent('distanceDimension1', 'locator1', 'locator2', distanceGroup)
	cmds.pointConstraint(jointHierarchy[0], 'locator1')
	cmds.pointConstraint(jointHierarchy[1], 'locator2')

	# Rename distance measuring nodes
	cmds.rename('distanceDimension1', f'{side.lower()}_{systemChoice[8:].lower()}_twist1_distance')
	cmds.rename('locator1', f'{side.lower()}_{systemChoice[8:].lower()}_twist_distanceStart_loc')
	cmds.rename('locator2', f'{side.lower()}_{systemChoice[8:].lower()}_twist_distanceMiddle_loc')

	# -------------------------------------------------------------------------------------------------------------------
	# Create the rotation extractor joints
	for extractor in ['_rotExtEnd', '_rotExt']:
		jointName = jointHierarchy[0][:jointUnderscoreIndexList[-1]] + extractor + jointHierarchy[0][jointUnderscoreIndexList[-1]:]
		if '_result_' in jointName:
			jointName = jointName.replace('_result_', '_')
		cmds.duplicate(jointHierarchy[0], name=jointName, parentOnly=True)
		cmds.parent(jointName, fixGroupName)

		if extractor == '_rotExtEnd':
			cmds.xform(jointName, translation=(jointPrimaryAxis[0]*totalDistance*0.7, jointPrimaryAxis[1]*totalDistance*0.7, jointPrimaryAxis[2]*totalDistance*0.7))
			cmds.setAttr(f'{jointName}.radius', 0.2 * cmds.getAttr(f'{jointName}.radius'))

		if extractor == '_rotExt':
			cmds.parent(jointName.replace('_rotExt_', '_rotExtEnd_'), jointName)
			cmds.aimConstraint(jointHierarchy[1], jointName, aimVector=jointPrimaryAxis, worldUpType='none')
			cmds.orientConstraint(jointName, resultGroupName)

			# Create output locator
			outputLocatorName = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}{extractor}_out'
			cmds.spaceLocator(name=outputLocatorName)
			cmds.matchTransform(outputLocatorName, jointHierarchy[0])
			cmds.parent(outputLocatorName, jointName)
			cmds.orientConstraint(jointHierarchy[0], outputLocatorName)

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'twistRotExtractor', 'undefined', side.lower(), systemChoice[8:].lower())

	# Set up variables for multiply node(s)
	if jointPrimaryAxis == (1,0,0) or jointPrimaryAxis == (-1,0,0):
		jointPrimaryAxisLetter = 'X'
	elif jointPrimaryAxis == (0,1,0) or jointPrimaryAxis == (0,-1,0):
		jointPrimaryAxisLetter = 'Y'
	elif jointPrimaryAxis == (0,0,1) or jointPrimaryAxis == (0,0,-1):
		jointPrimaryAxisLetter = 'Z'

	# -------------------------------------------------------------------------------------------------------------------
	# Create the twist joints
	for i in range(twistJointAmount):
		jointName = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twist{str(i)}{jointHierarchy[0][jointUnderscoreIndexList[-1]:]}'
		cmds.duplicate(jointHierarchy[0], name=jointName, parentOnly=True)
		cmds.parent(jointName, resultGroupName)

		#Place the joints
		placementNode = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twistPlacement{i+1}_multi'
		cmds.createNode('multiplyDivide', skipSelect=True, name=placementNode)
		cmds.setAttr(f'{placementNode}.input1.input1X', i)
		cmds.connectAttr(f'{distancePerJoint}.output.outputX', f'{placementNode}.input2.input2X')
		cmds.connectAttr(f'{placementNode}.output.outputX', f'{jointName}.translate{jointPrimaryAxisLetter}')

		# Set joint labelling
		cmds.setAttr(f'{jointName}.type', 18)
		cmds.setAttr(f'{jointName}.otherType', 'twist', type='string')

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'twist', str(i+1), side.lower(), systemChoice[8:].lower())

	# -------------------------------------------------------------------------------------------------------------------
	# Create the global control twist attributes
	cmds.addAttr(globalControlName, longName='twistSeparator', niceName='_______', attributeType='enum', enumName='TWIST', keyable=True)
	cmds.setAttr(f'{globalControlName}.twistSeparator', lock=True)
	for i in range(twistJointAmount):
		twistMultiValue = (1 / twistJointAmount) * i
		cmds.addAttr(globalControlName, longName=f'twist_1_{str(i)}_multi', niceName=f'Twist 1 {str(i)} Multi', attributeType='float', defaultValue=twistMultiValue, keyable=True)

	numberOfMultipliers = math.ceil(twistJointAmount / 3)

	# Create the twist multiply node(s)
	numberOfConnections = 0
	for i in range(numberOfMultipliers):
		multiplyNodeName = f'{side.lower()}_{systemChoice[8:].lower()}_twist_1_multi{i}'
		cmds.createNode('multiplyDivide', skipSelect=True, name=multiplyNodeName)

		# Connect the output locator and global control to the multiply node(s)
		for letter in ['X','Y','Z']:
			if not numberOfConnections >= twistJointAmount:
				cmds.connectAttr(f'{outputLocatorName}.rotate{jointPrimaryAxisLetter}', f'{multiplyNodeName}.input1.input1{letter}')
				cmds.connectAttr(f'{globalControlName}.twist_1_{numberOfConnections}_multi', f'{multiplyNodeName}.input2.input2{letter}')

				# Connect the multiply node(s) to the twist joints
				jointName = f'{jointHierarchy[0][:jointUnderscoreIndexList[-1]]}_twist{str(numberOfConnections)}{jointHierarchy[0][jointUnderscoreIndexList[-1]:]}'
				cmds.connectAttr(f'{multiplyNodeName}.output.output{letter}', f'{jointName}.rotate{jointPrimaryAxisLetter}')
				numberOfConnections += 1

	# -------------------------------------------------------------------------------------------------------------------
	# SECOND SECTION (eg. elbow to wrist)
	# -------------------------------------------------------------------------------------------------------------------

	# Find index where suffix starts in second joint
	jointUnderscoreIndexList = []
	for index,letter in enumerate(jointHierarchy[1]):
		if letter == '_':
			jointUnderscoreIndexList.append(index)

	jointExtractorUnderscoreIndexList = []
	for index,letter in enumerate(jointHierarchy[2]):
		if letter == '_':
			jointExtractorUnderscoreIndexList.append(index)

	# Create twist resultGrp, fixGroup and distance fixGroup
	resultGroupName = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twists_results'
	if '_result_' in resultGroupName:
		resultGroupName = resultGroupName.replace('_result_', '_')
	fixGroupName = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twists_fixGrp'
	for group in [resultGroupName, fixGroupName]:
		cmds.group(name=group, empty=True)
	cmds.matchTransform(resultGroupName, jointHierarchy[1])
	cmds.matchTransform(fixGroupName, jointHierarchy[2])
	cmds.parent(resultGroupName, fixGroupName)
	cmds.parentConstraint(jointHierarchy[1], resultGroupName)
	cmds.pointConstraint(jointHierarchy[2], fixGroupName)

	# parent to system holder group
	cmds.parent(fixGroupName, twistGroupsContainer)

	# Measure the distance between the second and third joint (eg. elbow to wrist)
	startPoint = cmds.xform(jointHierarchy[1], query=True, translation=True, worldSpace=True)
	endPoint = cmds.xform(jointHierarchy[2], query=True, translation=True, worldSpace=True)
	cmds.distanceDimension(startPoint=startPoint, endPoint=endPoint)
	totalDistance = cmds.getAttr('distanceDimension1.distance')
	distancePerJoint = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twistPlacement_divide'
	cmds.createNode('multiplyDivide', skipSelect=True, name=distancePerJoint)
	cmds.setAttr(f'{distancePerJoint}.operation', 2)
	cmds.connectAttr('distanceDimension1.distance', f'{distancePerJoint}.input1.input1X')
	cmds.setAttr(f'{distancePerJoint}.input2.input2X', twistJointAmount)

	# Group and constrain distance measuring nodes
	cmds.parent('distanceDimension1', 'locator1', distanceGroup)
	cmds.pointConstraint(jointHierarchy[2], 'locator1')

	# Rename distance measuring nodes
	cmds.rename('distanceDimension1', f'{side.lower()}_{systemChoice[8:].lower()}_twist2_distance')
	cmds.rename('locator1', f'{side.lower()}_{systemChoice[8:].lower()}_twist_distanceEnd_loc')

	# -------------------------------------------------------------------------------------------------------------------
	# Create the rotation extractor joints
	extractor = ['_rotExtLookAt', '_rotExtEnd', '_rotExt']
	for nameAddon in extractor:
		jointName = jointHierarchy[2][:jointExtractorUnderscoreIndexList[-1]] + nameAddon + jointHierarchy[2][jointExtractorUnderscoreIndexList[-1]:]
		if '_result_' in jointName:
				jointName = jointName.replace('_result_', '_')
		cmds.duplicate(jointHierarchy[2], name=jointName, parentOnly=True)
		cmds.parent(jointName, fixGroupName)
		if nameAddon == '_rotExtLookAt':
			cmds.xform(jointName, translation=(jointPrimaryAxis[0]*totalDistance*0.3, jointPrimaryAxis[1]*totalDistance*0.3, jointPrimaryAxis[2]*totalDistance*0.3))
			cmds.parentConstraint(jointHierarchy[2], jointName, maintainOffset=True)
		if nameAddon == '_rotExtEnd':
			cmds.xform(jointName, translation=(jointPrimaryAxis[0]*totalDistance*0.2, jointPrimaryAxis[1]*totalDistance*0.2, jointPrimaryAxis[2]*totalDistance*0.2))
		if nameAddon == '_rotExt':
			cmds.parent(jointName.replace('_rotExt_', '_rotExtEnd_'), jointName)
			cmds.aimConstraint(jointName.replace('_rotExt_', '_rotExtLookAt_'), jointName, aimVector=jointPrimaryAxis, worldUpType='none')

			# Create output locator
			outputLocatorName = f'{jointHierarchy[2][:jointExtractorUnderscoreIndexList[-1]]}{nameAddon}_out'
			cmds.spaceLocator(name=outputLocatorName)
			cmds.matchTransform(outputLocatorName, jointHierarchy[2])
			cmds.parent(outputLocatorName, jointName)
			cmds.orientConstraint(jointHierarchy[2], outputLocatorName)

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'twistRotExtractor', 'undefined', side.lower(), systemChoice[8:].lower())

	# -------------------------------------------------------------------------------------------------------------------
	# Create the twist joints
	for i in range(twistJointAmount):
		jointName = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twist{str(i)}{jointHierarchy[1][jointUnderscoreIndexList[-1]:]}'
		cmds.duplicate(jointHierarchy[1], name=jointName, parentOnly=True)
		cmds.parent(jointName, resultGroupName)

		#Place the joints
		placementNode = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twistPlacement{i+1}_multi'
		cmds.createNode('multiplyDivide', skipSelect=True, name=placementNode)
		cmds.setAttr(f'{placementNode}.input1.input1X', i)
		cmds.connectAttr(f'{distancePerJoint}.output.outputX', f'{placementNode}.input2.input2X')
		cmds.connectAttr(f'{placementNode}.output.outputX', f'{jointName}.translate{jointPrimaryAxisLetter}')

		# Set joint labelling
		cmds.setAttr(f'{jointName}.type', 18)
		cmds.setAttr(f'{jointName}.otherType', 'twist', type='string')

		# Edit Rig Rat Attributes
		RigRatAttributes(jointName, 'joint', 'twist', str(i+1), side.lower(), systemChoice[8:].lower())

	# -------------------------------------------------------------------------------------------------------------------
	# Create the global control twist attributes
	for i in range(twistJointAmount):
		twistMultiValue = 1 / twistJointAmount * (i+1)
		cmds.addAttr(globalControlName, longName=f'twist_2_{str(i)}_multi', niceName=f'Twist 2 {str(i)} Multi', attributeType='float', defaultValue=twistMultiValue, keyable=True)

	# Create the twist multiply node(s)
	numberOfConnections = 0
	for i in range(numberOfMultipliers):
		multiplyNodeName = f'{side.lower()}_{systemChoice[8:].lower()}_twist_2_multi{i}'
		cmds.createNode('multiplyDivide', skipSelect=True, name=multiplyNodeName)

		# Connect the output locator and global control to the multiply node(s)
		for letter in ['X','Y','Z']:
			if not numberOfConnections >= twistJointAmount:
				cmds.connectAttr(f'{outputLocatorName}.rotate{jointPrimaryAxisLetter}', f'{multiplyNodeName}.input1.input1{letter}')
				cmds.connectAttr(f'{globalControlName}.twist_2_{numberOfConnections}_multi', f'{multiplyNodeName}.input2.input2{letter}')

				# Connect the multiply node(s) to the twist joints
				jointName = f'{jointHierarchy[1][:jointUnderscoreIndexList[-1]]}_twist{str(numberOfConnections)}{jointHierarchy[1][jointUnderscoreIndexList[-1]:]}'
				cmds.connectAttr(f'{multiplyNodeName}.output.output{letter}', f'{jointName}.rotate{jointPrimaryAxisLetter}')
				numberOfConnections += 1

	cmds.select(clear=True)

	'''
	CREATE A DICTIONARY OF EG. IK JOINTS IN THE LEFT ARM
	ikJointsDict = {}

	for joint in cmds.ls(exactType='joint'):
		try:
			if cmds.attributeQuery('jhRigSystem', node=joint, listEnum=True)[0] == 'ik' and cmds.attributeQuery('jhRigSide', node=joint, listEnum=True)[0] == side.lower() and cmds.attributeQuery('jhRigLimbType', node=joint, listEnum=True)[0] == systemChoice[8:].lower():
				if cmds.attributeQuery('jhRigObjectNumberInSystem', node=joint, listEnum=True)[0] == '1':
					ikJointsDict['joint1'] = joint
				elif cmds.attributeQuery('jhRigObjectNumberInSystem', node=joint, listEnum=True)[0] == '2':
					ikJointsDict['joint2'] = joint
				elif cmds.attributeQuery('jhRigObjectNumberInSystem', node=joint, listEnum=True)[0] == '3':
					ikJointsDict['joint3'] = joint
		except:
			continue
	'''

# ====================================================================================================================
#
# SIGNATURE:
#	TwistBipedSetup(systemChoice, side, globalControlName, jointPrimaryAxis, jointHierarchy)
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

def StretchBipedSetup(systemChoice, side, globalControlName, jointPrimaryAxis, jointHierarchy):

	# Check axis to measure distance along
	if jointPrimaryAxis == (1,0,0) or jointPrimaryAxis == (-1,0,0):
		jointPrimaryAxisLetter = 'X'
	elif jointPrimaryAxis == (0,1,0) or jointPrimaryAxis == (0,-1,0):
		jointPrimaryAxisLetter = 'Y'
	elif jointPrimaryAxis == (0,0,1) or jointPrimaryAxis == (0,0,-1):
		jointPrimaryAxisLetter = 'Z'

	# Measure the distance between the second and third joint (eg. elbow to wrist)
	cmds.distanceDimension(startPoint=(0,0,0), endPoint=(1,0,0))
	cmds.matchTransform('locator1', jointHierarchy[0], position=True, rotation=False, scale=False)
	cmds.matchTransform('locator2', jointHierarchy[2], position=True, rotation=False, scale=False)

	# Limb length at resting position
	limbLength = 0
	for joint in jointHierarchy[1:]:
		limbLength += cmds.getAttr(f'{joint}.translate{jointPrimaryAxisLetter}')

	# Get IK control name
	jointUnderscoreIndexList = []
	for index,letter in enumerate(jointHierarchy[2]):
		if letter == '_':
			jointUnderscoreIndexList.append(index)
	controlName = f'{joint[:jointUnderscoreIndexList[0]]}_ik{joint[jointUnderscoreIndexList[0]:jointUnderscoreIndexList[-1]]}_ctrl'
	if '_result_' in controlName:
		controlName = controlName.replace('_result_', '_')

	# Add stretch attributes to the IK control
	cmds.addAttr(controlName, longName='stretchSeparator', niceName='_______', attributeType='enum', enumName='STRETCH', keyable=True)
	cmds.setAttr(f'{controlName}.stretchSeparator', lock=True)
	cmds.addAttr(controlName, longName='stretch_multi', niceName='Stretch', attributeType='float', min=0.0, max=1.0, defaultValue=0, keyable=True)

	# -------------------------------------------------------------------------------------------------------------------
	# Create the stretch divide and multiply nodes
	for nodeName in [f'{side.lower()}_{systemChoice[8:].lower()}_stretch_divide', f'{side.lower()}_{systemChoice[8:].lower()}_stretch_multi']:
		cmds.createNode('multiplyDivide', skipSelect=True, name=nodeName)
		
		# Connect and calculate distance difference
		if nodeName[-14:] == 'stretch_divide':
			cmds.setAttr(f'{nodeName}.operation', 2)
			cmds.connectAttr('distanceDimension1.distance', f'{nodeName}.input1.input1X')
			cmds.setAttr(f'{nodeName}.input2.input2X', limbLength)

		# Connect the distance difference output and ik controls stretch attribute
		if nodeName[-13:] == 'stretch_multi':
			cmds.connectAttr(nodeName.replace('stretch_multi', 'stretch_divide') + '.output.outputX', f'{nodeName}.input1.input1X')
			cmds.connectAttr(f'{controlName}.stretch_multi', f'{nodeName}.input2.input2X')

			# Set IK joint scale minimum to 1
			for joint in jointHierarchy[:2]:
				jointName = f'{joint[:jointUnderscoreIndexList[0]]}_ik{joint[jointUnderscoreIndexList[0]:]}'
				if '_result_' in jointName:
					jointName = jointName.replace('_result_', '_')
				if jointPrimaryAxisLetter == 'X':
					cmds.transformLimits(jointName, enableScaleX=(True, False), scaleX=(1.0, 1.0))
				elif jointPrimaryAxisLetter == 'Y':
					cmds.transformLimits(jointName, enableScaleY=(True, False), scaleY=(1.0, 1.0))
				elif jointPrimaryAxisLetter == 'Z':
					cmds.transformLimits(jointName, enableScaleZ=(True, False), scaleZ=(1.0, 1.0))

				# Connect the stretch result to the IK joints
				cmds.connectAttr(f'{nodeName}.output.outputX', f'{jointName}.scale{jointPrimaryAxisLetter}')

	# -------------------------------------------------------------------------------------------------------------------
	# Group distance measuring nodes
	fixGroupName = f'{side.lower()}_{systemChoice[8:].lower()}_stretch_fixGroup'
	cmds.group(name=fixGroupName, empty=True)
	cmds.matchTransform(fixGroupName, jointHierarchy[0])
	cmds.parent('distanceDimension1', 'locator1', 'locator2', fixGroupName)

	# Rename distance measuring nodes
	cmds.rename('distanceDimension1', f'{side.lower()}_{systemChoice[8:].lower()}_stretch_distance')
	cmds.rename('locator1', f'{side.lower()}_{systemChoice[8:].lower()}_stretch_distanceStart_loc')
	cmds.rename('locator2', f'{side.lower()}_{systemChoice[8:].lower()}_stretch_distanceEnd_loc')

	# Constraint distance end point to the IK control
	cmds.pointConstraint(controlName, f'{side.lower()}_{systemChoice[8:].lower()}_stretch_distanceEnd_loc')

	# Parent to "SYSTEMS" holder group
	systemsGroupContainer = f'{side.upper()}_{systemChoice[8:].upper()}_SYSTEMS'
	cmds.parent(fixGroupName, systemsGroupContainer)

	cmds.select(clear=True)