# ====================================================================================================================
#
# Rig Rat Toolkit - Controls
#
# ====================================================================================================================
#
# DESCRIPTION:
#	Constains the functions for the "Controls" tab.
#
# REQUIRES:
#	Nothing
#
# ====================================================================================================================

import maya.cmds as cmds
import sys
from RigRatToolkit.Menu import RigRatAttributes

# ====================================================================================================================
#
# SIGNATURE:
#	CreateControl(*args)
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

def CreateControl(controlChoice):

	# Gather UI and selection data
	controlName = cmds.textFieldGrp('controlName', query=True, text=True)

	controlAimAxis = cmds.radioButtonGrp('controlAim', query=True, select=True)
	if controlAimAxis == 1:
		controlNormal = (1,0,0)
	elif controlAimAxis == 2:
		controlNormal = (0,1,0)
	elif controlAimAxis == 3:
		controlNormal = (0,0,1)

	controlColor = cmds.colorIndexSliderGrp('controlColor', query=True, value=True)-1

	controlSize = cmds.floatSliderGrp('controlSize', query=True, value=True)

	transformNodes = cmds.ls(transforms=True)
	# Set a default name and add a number to avoid name clashing.
	if not controlName:
		controlName = 'curve1'
		while controlName in transformNodes:
			controlNumber = int(controlName[5:])
			controlName = 'curve' + str(controlNumber+1)
	fixGroupName = f'{controlName}_fixGroup'

	selection = cmds.ls(selection=True)

	# -------------------------------------------------------------------------------------------------------------------
	# Create control and fixGroup on selected object/s
	if selection:
		for item in selection:
			controlName = f'{item}_ctrl'
			if controlName in transformNodes:
				cmds.inViewMessage(assistMessage=f'<hl>{controlName} already exists</hl>.', position='midCenter', fade=True, clickKill=True)
				cmds.error(f'{controlName} already exists.')
			fixGroupName = f'{item}_fixGroup'

			BuildControl(controlChoice, controlName, controlNormal, controlSize)

			cmds.group(controlName, name=fixGroupName)
			if controlChoice == 'lollipop':
				cmds.xform(fixGroupName, rotatePivot=(0,0,0), scalePivot=(0,0,0), worldSpace=True)
			cmds.matchTransform(fixGroupName, item)
			cmds.setAttr(f'{controlName}.overrideEnabled', 1)
			cmds.setAttr(f'{controlName}.overrideColor', controlColor)

			# Edit Rig Rat Attributes
			RigRatAttributes(controlName, 'control', 'undefined', 'undefined', 'undefined', 'undefined')
			
	# Create control and fixGroup on origo
	elif not selection:
		if controlName in transformNodes:
			cmds.inViewMessage(assistMessage=f'<hl>{controlName} already exists</hl>.', position='midCenter', fade=True, clickKill=True)
			cmds.error(f'{controlName} already exists.')

		BuildControl(controlChoice, controlName, controlNormal, controlSize)

		cmds.group(controlName, name=fixGroupName)
		if controlChoice == 'lollipop':
				cmds.xform(fixGroupName, rotatePivot=(0,0,0), scalePivot=(0,0,0), worldSpace=True)
		cmds.setAttr(f'{controlName}.overrideEnabled', 1)
		cmds.setAttr(f'{controlName}.overrideColor', controlColor)

		# Edit Rig Rat Attributes
		RigRatAttributes(controlName, 'control', 'undefined', 'undefined', 'undefined', 'undefined')

	cmds.select(clear=True)

# ====================================================================================================================
#
# SIGNATURE:
#	BuildControl(controlChoice, controlName, controlNormal, controlSize)
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

def BuildControl(controlChoice, controlName, controlNormal, controlSize):

	if controlChoice == 'circle':
		cmds.circle(name=controlName, normal=controlNormal, radius=1, constructionHistory=False)
	if controlChoice == 'square':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4),
					point=( (1,0,1), (-1,0,1), (-1,0,-1), (1,0,-1), (1,0,1) ))
	if controlChoice == 'romb':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4),
					point=( (1,0,0), (0,0,1), (-1,0,0), (0,0,-1), (1,0,0) ))
	if controlChoice == 'plus':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
					point=( (0.5,0,-0.5), (1,0,-0.5), (1,0,0.5), (0.5,0,0.5), (0.5,0,1), (-0.5,0,1), (-0.5,0,0.5), (-1,0,0.5), (-1,0,-0.5), (-0.5,0,-0.5),
						(-0.5,0,-1), (0.5,0,-1), (0.5,0,-0.5) ))
	if controlChoice == 'arrow':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6 ,7),
					point=( (0,1,0), (1,0.25,0), (0.6,0.25,0), (0.6,-1,0), (-0.6,-1,0), (-0.6,0.25,0), (-1,0.25,0), (0,1,0) ))
	if controlChoice == 'lollipop':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28),
						point=( (0,1,0), (0,0.66,-0.66), (0,0,-1), (0,-0.66,-0.66), (0,-1,0), (0,-0.66,0.66), (0,0,1), (0,0,5), (0,0,1), (0,0.66,0.66), (0,1,0),
							(0.66,0.66,0), (1,0,0), (0.66,-0.66,0), (0,-1,0), (-0.66,-0.66,0), (-1,0,0), (-0.66,0.66,0), (0,1,0), (-0.66,0.66,0), (-1,0,0),
							(-0.66,0,-0.66), (0,0,-1), (0.66,0,-0.66), (1,0,0), (0.66,0,0.66), (0,0,1), (-0.66,0,0.66), (-1,0,0) ))
		cmds.xform(controlName, rotatePivot=(0,0,5), scalePivot=(0,0,5), worldSpace=True)
		cmds.xform(controlName, translation=(0,0,-5), worldSpace=True)
		cmds.xform(controlName, scale=(0.33,0.33,0.33))
		if not controlNormal == (0,1,0):
			cmds.xform(controlName, rotation=(90,0,0))
	if controlChoice == 'cube':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 14, 15),
						point=( (-1,1,1), (1,1,1), (1,1,-1), (-1,1,-1), (-1,1,1), (-1,-1,1), (-1,-1,-1), (1,-1,-1), (1,-1,1), (-1,-1,1), (1,-1,1), (1,1,1),
							(1,1,-1), (1,-1,-1), (-1,-1,-1), (-1,1,-1) ))
	if controlChoice == 'sphere':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26),
						point=( (0,1,0), (0,0.66,-0.66), (0,0,-1), (0,-0.66,-0.66), (0,-1,0), (0,-0.66,0.66), (0,0,1), (0,0.66,0.66), (0,1,0), (0.66,0.66,0),
							(1,0,0), (0.66,-0.66,0), (0,-1,0), (-0.66,-0.66,0), (-1,0,0), (-0.66,0.66,0), (0,1,0), (-0.66,0.66,0), (-1,0,0), (-0.66,0,-0.66),
							(0,0,-1), (0.66,0,-0.66), (1,0,0), (0.66,0,0.66), (0,0,1), (-0.66,0,0.66), (-1,0,0) ))
	if controlChoice == 'orient':
		cmds.curve(degree=3, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
							29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61),
						point=( (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.337), (0.751,0.328,-0.337), (1.002,0,0), (1.002,0,0),
							(0.751,0.328,0.337), (0.751,0.328,0.337), (0.751,0.328,0.099), (0.751,0.328,0.099), (0.501,0.5,0.099), (0.096,0.604,0.099), (0.096,0.604,0.099),
							(0.096,0.5,0.501), (0.096,0.328,0.751), (0.096,0.328,0.751), (0.337,0.328,0.751), (0.337,0.328,0.751), (0,0,1.002), (0,0,1.002),
							(-0.337,0.328,0.751), (-0.337,0.328,0.751), (-0.096,0.328,0.751), (-0.096,0.328,0.751), (-0.0969835,0.5,0.501), (-0.096,0.604,0.099),
							(-0.096,0.604,0.099), (-0.501,0.5,0.099), (-0.751,0.328,0.099), (-0.751,0.328,0.099), (-0.751,0.328,0.337), (-0.751,0.328,0.337), (-1.002,0,0),
							(-1.002,0,0), (-0.751,0.328,-0.337), (-0.751,0.328,-0.337), (-0.751,0.328,-0.099), (-0.751,0.328,-0.099), (-0.501,0.5,-0.099), (-0.096,0.604,-0.099),
							(-0.096,0.604,-0.099), (-0.096,0.5,-0.501), (-0.096,0.328,-0.751), (-0.096,0.328,-0.751), (-0.337,0.328,-0.751), (-0.337,0.328,-0.751), (0,0,-1.002),
							(0,0,-1.002), (0.337,0.328,-0.751), (0.337,0.328,-0.751), (0.096,0.328,-0.751), (0.096,0.328,-0.751), (0.096,0.5,-0.501), (0.096,0.604,-0.099),
							(0.096,0.604,-0.099), (0.501,0.5,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099) ))
	if controlChoice == 'orientHalf':
		cmds.curve(degree=3, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 ,14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
							29, 30, 31, 32, 33),
						point=( (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.337), (0.751,0.328,-0.337), (1.002,0,0), (1.002,0,0),
							(0.751,0.328,0.337), (0.751,0.328,0.337), (0.751,0.328,0.099), (0.751,0.328,0.099), (0.501,0.5,0.099), (0.096,0.604,0.099), (-0.096,0.604,0.099),
							(-0.501,0.5,0.099), (-0.751,0.328,0.099), (-0.751,0.328,0.099), (-0.751,0.328,0.337), (-0.751,0.328,0.337), (-1.002,0,0), (-1.002,0,0),
							(-0.751,0.328,-0.337), (-0.751,0.328,-0.337), (-0.751,0.328,-0.099), (-0.751,0.328,-0.099), (-0.501,0.5,-0.099), (-0.096,0.604,-0.099),
							(0.096,0.604,-0.099), (0.501,0.5,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099), (0.751,0.328,-0.099) ))
	if controlChoice == 'arrows':
		cmds.curve(degree=1, name=controlName, knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 , 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24),
						point=( (1,0,0), (0.6,0,0.4), (0.6,0,0.2), (0.2,0,0.2), (0.2,0,0.6), (0.4,0,0.6), (0,0,1), (-0.4,0,0.6), (-0.2,0,0.6), (-0.2,0,0.2),
							(-0.6,0,0.2), (-0.6,0,0.4), (-1,0,0), (-0.6,0,-0.4), (-0.6,0,-0.2), (-0.2,0,-0.2), (-0.2,0,-0.6), (-0.4,0,-0.6), (0,0,-1), (0.4,0,-0.6),
							(0.2,0,-0.6), (0.2,0,-0.2), (0.6,0,-0.2), (0.6,0,-0.4), (1,0,0) ))
	if controlChoice == 'cuteHead':
		cmds.curve(degree=3, name='globalCtrlHead', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
			point=( (0.324,0,0.586), (0.324,0,0.586), (0.324,0,0.586), (0.35,0,0.41), (0.54,0,0.41), (0.756,0,0.41), (0.972,0,-0.02), (0.756,0,-0.545), (0.324,0,-0.803),
				(-0.324,0,-0.803), (-0.756,0,-0.545), (-0.972,0,-0.02), (-0.756,0,0.41), (-0.54,0,0.41), (-0.35,0,0.41), (-0.324,0,0.586), (-0.324,0,0.586), (-0.324,0,0.586) ))
		cmds.curve(degree=3, name='globalCtrlNose', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
			point=( (0,0,0.2), (0,0,0.2), (0,0,0.2), (-0.12,0,0.31), (-0.14,0,0.52), (0,0,0.39), (0.14,0,0.52), (0.12,0,0.31), (0,0,0.2), (0,0,0.2), (0,0,0.2) ))
		cmds.curve(degree=3, name='globalCtrlTeeth', knot=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
			point=( (0.324,0,0.587), (0.324,0,0.587), (0.324,0,0.587), (0.317,0,0.778), (0.141,0,0.643), (0,0,0.803), (-0.141,0,0.643), (-0.317,0,0.778), (-0.324,0,0.587),
				(-0.324,0,0.587), (-0.324,0,0.587) ))
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
			cmds.rename(cmds.listRelatives(shape, shapes=True), f'{controlName}{shape[10:]}Shape')
		cmds.parent(cmds.listRelatives('globalCtrlNose', 'globalCtrlTeeth', 'globalCtrlLeftEye', 'globalCtrlRightEye', shapes=True), 'globalCtrlHead', shape=True, relative=True)
		cmds.delete('globalCtrlNose', 'globalCtrlTeeth', 'globalCtrlLeftEye', 'globalCtrlRightEye')
		cmds.rename('globalCtrlHead', controlName)

	for choice in ['square', 'romb', 'plus', 'arrow', 'orient', 'orientHalf', 'arrows', 'cuteHead']:
		if choice == controlChoice:
			if controlNormal == (1,0,0):
				cmds.xform(controlName, rotation=(0,0,90))
			elif controlNormal == (0,0,1):
				cmds.xform(controlName, rotation=(90,0,0))

	cmds.xform(controlName, scale=(controlSize,controlSize,controlSize))
	cmds.makeIdentity(controlName, apply=True)

# ====================================================================================================================
#
# SIGNATURE:
#	UpdateControlColor(*args)
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

def UpdateControlColor(*args):

	controlColor = cmds.colorIndexSliderGrp('controlColor', query=True, value=True)-1
	selection = cmds.ls(selection=True, transforms=True)

	for item in selection:
		cmds.setAttr(f'{item}.overrideEnabled', 1)
		cmds.setAttr(f'{item}.overrideColor', controlColor)

# ====================================================================================================================
#
# SIGNATURE:
#	UpdateControlSize(*args)
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

def UpdateControlSize(*args):

	selection = cmds.ls(selection=True, transforms=True)

	if selection:
		controlSize = cmds.floatSliderGrp('controlSize', query=True, value=True)

		for item in selection:
			try:
				numberOfCvs = cmds.getAttr(f'{item}.degree') + cmds.getAttr(f'{item}.spans')
			except:
				cmds.inViewMessage(assistMessage=f'<hl>{item} is not a nurbs curve</hl>.', position='midCenter', fade=True, clickKill=True)
				cmds.error(f'{controlName} is not a nurbs curve.')
			controlCvs = cmds.select(f'{item}.cv[0:{numberOfCvs-1}]', replace=True)
			cmds.scale(controlSize,controlSize,controlSize)
			cmds.select(selection)

# ====================================================================================================================
#
# SIGNATURE:
#	replaceControlShape(*args)
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

def replaceControlShape(*args):

	tooltipCheck = cmds.framelessDialog( title='Confirm', button=['OK', 'CANCEL'], primary=['OK'],
		message='Make sure both controls are in the same position in world space and are zeroed out (frozen).\n\nThe resulting control could become invisible when executing the script, but moving it and undoing the movement should make it visible.')

	if tooltipCheck == 'CANCEL':
		sys.exit()
	elif tooltipCheck == 'OK':
		# selection[0] is the new control and selection[1] is the one to be replaced
		selection = cmds.ls(selection=True, transforms=True)
		cmds.matchTransform(selection[0], selection[1])

		for item in selection:
			cmds.makeIdentity(item, apply=True)

		newShapes = cmds.listRelatives(selection[0])
		oldShapes = cmds.listRelatives(selection[1])

		cmds.parent(newShapes, selection[1], relative=True, shape=True)
		cmds.delete(selection[0], oldShapes)

# ====================================================================================================================
#
# SIGNATURE:
#	SelectControlCvs(*args)
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

def SelectControlCvs(*args):

	selection = cmds.ls(selection=True, transforms=True)
	controlCvs = []
	cmds.select(clear=True)
	
	if selection:
		for item in selection:
			try:
				numberOfCvs = cmds.getAttr(f'{item}.degree') + cmds.getAttr(f'{item}.spans')
			except:
				cmds.inViewMessage(assistMessage=f'<hl>{item} is not a nurbs curve</hl>.', position='midCenter', fade=True, clickKill=True)
				cmds.error(f'{controlName} is not a nurbs curve.')
			controlCvs.append(f'{item}.cv[0:{numberOfCvs-1}]')
		cmds.selectMode(component=True)
		cmds.select(controlCvs)

# ====================================================================================================================
#
# SIGNATURE:
#	SnappingParent(*args)
#	SnappingPoint(*args)
#	SnappingOrient(*args)
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

def SnappingParent(*args):

	selection = cmds.ls(selection=True, transforms=True)
	selectionLength = len(selection)
	cmds.parentConstraint(selection[0:selectionLength-1], selection[-1], name='tempSnappingConstraint_parent')
	cmds.select(clear=True)
	cmds.delete('tempSnappingConstraint_parent')

def SnappingPoint(*args):
	
	selection = cmds.ls(selection=True, transforms=True)
	selectionLength = len(selection)
	cmds.pointConstraint(selection[0:selectionLength-1], selection[-1], name='tempSnappingConstraint_point')
	cmds.select(clear=True)
	cmds.delete('tempSnappingConstraint_point')

def SnappingOrient(*args):
	
	selection = cmds.ls(selection=True, transforms=True)
	selectionLength = len(selection)
	cmds.orientConstraint(selection[0:selectionLength-1], selection[-1], name='tempSnappingConstraint_orient')
	cmds.select(clear=True)
	cmds.delete('tempSnappingConstraint_orient')