# ====================================================================================================================
#
# Rig Rat Toolkit
#
# ====================================================================================================================
#
# DESCRIPTION:
#	
#
# REQUIRES:
#	Nothing
#
# VERSION:
#	1.0
#
# CHANGELOG:
#	0.1 - 
#
# ====================================================================================================================

def Version():

	return '1.0'

def RigRatAttributes(nodeName, objType, system, numInSystem, side, limbType):
	# Remove pre-existing Rig Rat attribute categories
	if cmds.attributeQuery('rigRatVersion', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatVersion')
	if cmds.attributeQuery('rigRatObjectType', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatObjectType')
	if cmds.attributeQuery('rigRatSystem', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatSystem')
	if cmds.attributeQuery('rigRatObjectNumberInSystem', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatObjectNumberInSystem')
	if cmds.attributeQuery('rigRatSide', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatSide')
	if cmds.attributeQuery('rigRatLimbType', node=nodeName, exists=True):
		cmds.deleteAttr(f'{nodeName}.rigRatLimbType')

	# Add new Rig Rat attribute categories
	cmds.addAttr(nodeName, longName='rigRatVersion', niceName='rigRatVersion', attributeType='enum', enumName=Version(), readable=False, )
	cmds.addAttr(nodeName, longName='rigRatObjectType', niceName='rigRatObjectType', attributeType='enum', enumName=objType, readable=False)
	cmds.addAttr(nodeName, longName='rigRatSystem', niceName='rigRatSystem', attributeType='enum', enumName=system, readable=False)
	cmds.addAttr(nodeName, longName='rigRatObjectNumberInSystem', niceName='rigRatObjectNumberInSystem', attributeType='enum', enumName=numInSystem, readable=False)
	cmds.addAttr(nodeName, longName='rigRatSide', niceName='rigRatSide', attributeType='enum', enumName=side, readable=False)
	cmds.addAttr(nodeName, longName='rigRatLimbType', niceName='rigRatLimbType', attributeType='enum', enumName=limbType, readable=False)

import maya.cmds as cmds
from RigRatToolkit.Controls import *
from RigRatToolkit.Joints import *
from RigRatToolkit.IkFk import IkFkUiData
from RigRatToolkit.Ribbon import RibbonUiData
from RigRatToolkit.Experimental import *

# ====================================================================================================================
#
# SIGNATURE:
#	Window()
#
# DESCRIPTION:
#	Window and interface.
#
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================

def Window():

	# Check if the window exists
	if cmds.window('rigRatToolkit', exists=True):
		cmds.deleteUI('rigRatToolkit')

	# Create the window
	window = cmds.window('rigRatToolkit', title='Rig Rat Toolkit - ' + Version(), width=300, height=530, maximizeButton=False, sizeable=False)

	# Create the main layout and tabs
	cmds.formLayout('mainForm', numberOfDivisions=100)

	tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
	cmds.formLayout( 'mainForm', edit=True, attachForm=[(tabs, 'top', 0), (tabs, 'bottom', 0), (tabs, 'left', 0), (tabs, 'right', 0)] )

	# -------------------------------------------------------------------------------------------------------------------
	# Control tab layout
	cmds.formLayout('controlForm')

	cmds.separator('separator01', height=10, style='in')
	cmds.text('controlNameText', label='Only uses name when selection is empty')
	cmds.textFieldGrp('controlName', label='Control Name:	', placeholderText='c_cog_ctrl', columnWidth2=(95,230))
	cmds.text('controlAimText', label='Control Aim Axis:')
	cmds.radioButtonGrp('controlAim', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth3=(40,40,40))
	cmds.colorIndexSliderGrp('controlColor', label='Control Color	', changeCommand=UpdateControlColor, columnWidth3=(94,80,100), width=350, min=0, max=20, value=6)
	cmds.button('updateControlColor', label="Update Selected's Color", command=UpdateControlColor)
	cmds.checkBox('updateControlColorLive', label='Update Live', value=1, changeCommand=UpdateControlColorLive)
	cmds.floatSliderGrp('controlSize', label='Control Size	', field=True, columnWidth3=(93,40,10), min=0.01, max=20, fieldMaxValue=100, value=1, changeCommand=DoNothing)
	cmds.button('updateControlSize', label="Update Selected's Size", command=UpdateControlSize)
	cmds.checkBox('updateControlSizeLive', label='Update Live', changeCommand=UpdateControlSizeLive)
	cmds.symbolButton('shape01', image='rigRatCircle.png', width=35, command=CreateControlCircle, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape02', image='rigRatSquare.png', width=35, command=CreateControlSquare, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape03', image='rigRatRomb.png', width=35, command=CreateControlRomb, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape04', image='rigRatPlus.png', width=35, command=CreateControlPlus, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape05', image='rigRatArrow.png', width=35, command=CreateControlArrow, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape06', image='rigRatLollipop.png', width=35, command=CreateControlLollipop, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape07', image='rigRatCube.png', width=35, command=CreateControlCube, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape08', image='rigRatSphere.png', width=35, command=CreateControlSphere, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape09', image='rigRatOrient.png', width=35, command=CreateControlOrient, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape10', image='rigRatOrientHalf.png', width=35, command=CreateControlOrientHalf, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape11', image='rigRatArrows.png', width=35, command=CreateControlArrows, annotation='Create at origo or on selected object/s')
	cmds.symbolButton('shape12', image='rigRatCuteHead.png', width=35, command=CreateControlCuteHead, annotation='Create at origo or on selected object/s')
	cmds.button('replaceControlShape', label="Replace Selected Control's Shape", command=replaceControlShape, annotation='Select the new control followed by the one to be replaced')
	cmds.button('SelectControlCvs', label="Select Control CV's", command=SelectControlCvs)
	cmds.separator('separator02', height=10)
	cmds.text('controlSnapping', label='Snapping', annotation='Works like constraints')
	cmds.button('parentConstrain', label="Parent", width=108, command=SnappingParent, annotation='Works like a constraint')
	cmds.button('pointConstrain', label="Point", width=108, command=SnappingPoint, annotation='Works like a constraint')
	cmds.button('orientConstrain', label="Orient", width=108, command=SnappingOrient, annotation='Works like a constraint')

	controlTab = cmds.formLayout( 'controlForm', edit=True, attachForm=[
																		('separator01', 'top', 0),
																		('separator01', 'left', 0),
																		('separator01', 'right', 0),

																		('controlNameText', 'top', 10),
																		('controlNameText', 'left', 0),
																		('controlNameText', 'right', 0),

																		('controlName', 'top', 25),
																		('controlName', 'left', 0),

																		('controlAimText', 'top', 55),
																		('controlAimText', 'left', 0),
																		('controlAimText', 'right', 0),

																		('controlAim', 'top', 70),
																		('controlAim', 'left', 120),

																		('controlColor', 'top', 100),
																		('controlColor', 'left', 0),
																		('controlColor', 'right', 5),

																		('updateControlColor', 'top', 125),
																		('updateControlColor', 'left', 97),

																		('updateControlColorLive', 'top', 128),
																		('updateControlColorLive', 'left', 240),

																		('controlSize', 'top', 160),
																		('controlSize', 'left', 0),
																		('controlSize', 'right', 5),

																		('updateControlSize', 'top', 185),
																		('updateControlSize', 'left', 97),

																		('updateControlSizeLive', 'top', 188),
																		('updateControlSizeLive', 'left', 240),

																		('shape01', 'top', 225),
																		('shape01', 'left', 60),

																		('shape02', 'top', 225),
																		('shape02', 'left', 110),

																		('shape03', 'top', 225),
																		('shape03', 'left', 160),

																		('shape04', 'top', 225),
																		('shape04', 'left', 210),

																		('shape05', 'top', 225),
																		('shape05', 'left', 260),

																		('shape06', 'top', 270),
																		('shape06', 'left', 60),

																		('shape07', 'top', 270),
																		('shape07', 'left', 110),

																		('shape08', 'top', 270),
																		('shape08', 'left', 160),

																		('shape09', 'top', 270),
																		('shape09', 'left', 210),

																		('shape10', 'top', 270),
																		('shape10', 'left', 260),

																		('shape11', 'top', 315),
																		('shape11', 'left', 135),

																		('shape12', 'top', 315),
																		('shape12', 'left', 185),

																		('replaceControlShape', 'top', 360),
																		('replaceControlShape', 'left', 90),

																		('SelectControlCvs', 'top', 395),
																		('SelectControlCvs', 'left', 125),

																		('separator02', 'top', 425),
																		('separator02', 'left', 5),
																		('separator02', 'right', 5),

																		('controlSnapping', 'top', 440),
																		('controlSnapping', 'left', 0),
																		('controlSnapping', 'right', 0),

																		('parentConstrain', 'top', 465),
																		('parentConstrain', 'left', 8),

																		('pointConstrain', 'top', 465),
																		('pointConstrain', 'left', 123),

																		('orientConstrain', 'top', 465),
																		('orientConstrain', 'left', 238)
																		] )
	cmds.setParent( '..' )

	# -------------------------------------------------------------------------------------------------------------------
	# Joint tab layout
	cmds.formLayout('jointForm')

	# Joint creation
	cmds.separator('separator01', height=10, style='in')
	cmds.textFieldGrp('jointPrefix', label='Joint Prefix:	', placeholderText='c', columnWidth2=(105,225))
	cmds.textFieldGrp('jointDescription', label='Joint Description:	', placeholderText='cog', columnWidth2=(105,225))
	cmds.textFieldGrp('jointSuffix', label='Joint Suffix:	', placeholderText='jnt', columnWidth2=(105,225))
	cmds.intSliderGrp('jointAmount', label='Joint Amount	', field=True, columnWidth3=(105,40,10), min=1, max=20, fieldMaxValue=100, value=1)
	cmds.floatSliderGrp('jointSpacing', label='Joint Spacing	', field=True, columnWidth3=(105,40,10), min=1, value=1)
	cmds.optionMenuGrp('jointSpacingDirection', label='Spacing Direction', columnWidth=(1,120))
	cmds.menuItem(label='X+')
	cmds.menuItem(label='Y+')
	cmds.menuItem(label='Z+')
	cmds.checkBox('invertJointSpacingDirection', label='Invert Direction')
	cmds.optionMenuGrp('jointRotationOrder', label='Rotation Order', columnWidth=(1,120))
	cmds.menuItem(label='xyz')
	cmds.menuItem(label='yzx')
	cmds.menuItem(label='zxy')
	cmds.menuItem(label='xzy')
	cmds.menuItem(label='yxz')
	cmds.menuItem(label='zyx')
	cmds.button('buildJoints', label="Create Joints", width=108, command=CreateJoints)
	cmds.separator('separator02', height=10)
	cmds.text('locatorJointOnCenter', label='Placed at center of selected object(s)/components')
	cmds.optionMenuGrp('jointOnCenterRotationOrder', label='Rotation Order', enable=False, columnWidth=(1,120))
	cmds.menuItem(label='xyz')
	cmds.menuItem(label='yzx')
	cmds.menuItem(label='zxy')
	cmds.menuItem(label='xzy')
	cmds.menuItem(label='yxz')
	cmds.menuItem(label='zyx')
	cmds.radioButtonGrp('locatorOrJoint', numberOfRadioButtons=2, labelArray2=('Locator','Joint'), select=1, columnWidth2=(80,80),
							onCommand2=LocatorOrJointOnCenter, offCommand2=LocatorOrJointOnCenter)
	cmds.textFieldGrp('locatorJointName', label='Name:	', columnWidth2=(75,225))
	cmds.button('buildLocatorOrJoint', label="Create Locator/Joint", width=108, command=CreateLocatorJointOnCenter)
	cmds.text('jointsTooltip', font='boldLabelFont', label='Tooltip')
	cmds.text('jointsTooltipContent1', wordWrap=True, label='If joints created with this tool disappear:')
	cmds.text('jointsTooltipContent2', wordWrap=True, label="Create a joint with Maya's own tool.")
	cmds.text('jointsTooltipContent3', wordWrap=True, label='Tends to happen when origo is not in the viewport')
	cmds.text('jointsTooltipContent4', wordWrap=True, label="until Maya's tool is used.")
	'''
	# Joint Orientation
	cmds.separator('separator03', height=10, style='in')
	cmds.button('showAxisAll', label="Show axis on all", width=108)
	cmds.button('hideAxisAll', label="Hide axis on all", width=108)
	cmds.button('showAxisSelected', label="Show axis on selected", width=108)
	cmds.button('hideAxisSelected', label="Hide axis on selected", width=108)
	cmds.checkBox('orientJointsToWorld', label='Orient Joints to World', onCommand=OrientJointToWorld, offCommand=OrientJointToWorld)
	cmds.radioButtonGrp('orientPrimaryAxis', label='Primary Axis	', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth4=(120,40,40,40))
	cmds.optionMenuGrp('orientPrimaryAxisInvert')
	cmds.menuItem(label='+')
	cmds.menuItem(label='-')
	cmds.radioButtonGrp('orientSecondaryAxis', label='Secondary Axis	', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth4=(120,40,40,40))
	cmds.radioButtonGrp('orientSecondaryAxisAim', label='Secondary Axis Aim	', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth4=(120,40,40,40))
	cmds.optionMenuGrp('orientSecondaryAxisInvert')
	cmds.menuItem(label='+')
	cmds.menuItem(label='-')
	cmds.checkBox('orientAffectChildren', label='Orient Children of Selected Joints')
	cmds.button('orientJoints', label="Orient Joints", width=108)
	cmds.separator('separator04', height=10)
	cmds.floatFieldGrp('orientRotationTweak', label='Rotation Tweak per Axis', extraLabel='degrees', numberOfFields=3, columnWidth5=(135,50,50,50,40))
	cmds.text('orientRotationTweakText', label='Tweak')
	cmds.button('orientRotationTweakAllPlus', label="All +", width=40)
	cmds.button('orientRotationTweakAllMinus', label="All -", width=40)
	cmds.button('orientRotationTweakXPlus', label="X +", width=40)
	cmds.button('orientRotationTweakXMinus', label="X -", width=40)
	cmds.button('orientRotationTweakYPlus', label="Y +", width=40)
	cmds.button('orientRotationTweakYMinus', label="Y -", width=40)
	cmds.button('orientRotationTweakZPlus', label="Z +", width=40)
	cmds.button('orientRotationTweakZMinus', label="Z -", width=40)
	'''
	jointTab = cmds.formLayout( 'jointForm', edit=True, attachForm=[
																	# Joint Creation
																	('separator01', 'top', 0),
																	('separator01', 'left', 0),
																	('separator01', 'right', 0),

																	('jointPrefix', 'top', 10),
																	('jointPrefix', 'left', 0),

																	('jointDescription', 'top', 30),
																	('jointDescription', 'left', 0),

																	('jointSuffix', 'top', 50),
																	('jointSuffix', 'left', 0),

																	('jointAmount', 'top', 80),
																	('jointAmount', 'left', 0),
																	('jointAmount', 'right', 10),

																	('jointSpacing', 'top', 110),
																	('jointSpacing', 'left', 0),
																	('jointSpacing', 'right', 10),

																	('jointSpacingDirection', 'top', 140),
																	('jointSpacingDirection', 'left', 0),
																	('jointSpacingDirection', 'right', 0),

																	('invertJointSpacingDirection', 'top', 143),
																	('invertJointSpacingDirection', 'left', 195),

																	('jointRotationOrder', 'top', 170),
																	('jointRotationOrder', 'left', 0),
																	('jointRotationOrder', 'right', 0),

																	('buildJoints', 'top', 200),
																	('buildJoints', 'left', 20),
																	('buildJoints', 'right', 20),

																	('separator02', 'top', 230),
																	('separator02', 'left', 5),
																	('separator02', 'right', 5),

																	('locatorJointOnCenter', 'top', 245),
																	('locatorJointOnCenter', 'left', 0),
																	('locatorJointOnCenter', 'right', 0),

																	('locatorOrJoint', 'top', 260),
																	('locatorOrJoint', 'left', 115),

																	('jointOnCenterRotationOrder', 'top', 285),
																	('jointOnCenterRotationOrder', 'left', 60),
																	('jointOnCenterRotationOrder', 'right', 0),

																	('locatorJointName', 'top', 315),
																	('locatorJointName', 'left', 0),
																	('locatorJointName', 'right', 0),

																	('buildLocatorOrJoint', 'top', 345),
																	('buildLocatorOrJoint', 'left', 20),
																	('buildLocatorOrJoint', 'right', 20),

																	('jointsTooltip', 'top', 395),
																	('jointsTooltip', 'left', 20),
																	('jointsTooltip', 'right', 20),

																	('jointsTooltipContent1', 'top', 415),
																	('jointsTooltipContent1', 'left', 20),
																	('jointsTooltipContent1', 'right', 20),

																	('jointsTooltipContent2', 'top', 430),
																	('jointsTooltipContent2', 'left', 20),
																	('jointsTooltipContent2', 'right', 20),

																	('jointsTooltipContent3', 'top', 450),
																	('jointsTooltipContent3', 'left', 20),
																	('jointsTooltipContent3', 'right', 20),

																	('jointsTooltipContent4', 'top', 465),
																	('jointsTooltipContent4', 'left', 20),
																	('jointsTooltipContent4', 'right', 20)
																	
																	# Joint Orientation
																	#('separator03', 'top', 375),
																	#('separator03', 'left', 5),
																	#('separator03', 'right', 5),

																	#('showAxisAll', 'top', 400),
																	#('showAxisAll', 'left', 20),
																	#('showAxisAll', 'right', 185),

																	#('hideAxisAll', 'top', 400),
																	#('hideAxisAll', 'left', 185),
																	#('hideAxisAll', 'right', 20),

																	#('showAxisSelected', 'top', 430),
																	#('showAxisSelected', 'left', 20),
																	#('showAxisSelected', 'right', 185),

																	#('hideAxisSelected', 'top', 430),
																	#('hideAxisSelected', 'left', 185),
																	#('hideAxisSelected', 'right', 20),

																	#('orientJointsToWorld', 'top', 472),
																	#('orientJointsToWorld', 'left', 100),

																	#('orientPrimaryAxis', 'top', 500),
																	#('orientPrimaryAxis', 'left', 0),

																	#('orientPrimaryAxisInvert', 'top', 500),
																	#('orientPrimaryAxisInvert', 'left', 250),

																	#('orientSecondaryAxis', 'top', 530),
																	#('orientSecondaryAxis', 'left', 0),

																	#('orientSecondaryAxisAim', 'top', 560),
																	#('orientSecondaryAxisAim', 'left', 0),

																	#('orientSecondaryAxisInvert', 'top', 560),
																	#('orientSecondaryAxisInvert', 'left', 250),

																	#('orientAffectChildren', 'top', 590),
																	#('orientAffectChildren', 'left', 100),

																	#('orientJoints', 'top', 620),
																	#('orientJoints', 'left', 20),
																	#('orientJoints', 'right', 20),

																	#('separator04', 'top', 650),
																	#('separator04', 'left', 5),
																	#('separator04', 'right', 5),

																	#('orientRotationTweak', 'top', 670),
																	#('orientRotationTweak', 'left', 5),
																	#('orientRotationTweak', 'right', 5),

																	#('orientRotationTweakText', 'top', 717),
																	#('orientRotationTweakText', 'left', 50),

																	#('orientRotationTweakAllPlus', 'top', 700),
																	#('orientRotationTweakAllPlus', 'left', 94),

																	#('orientRotationTweakAllMinus', 'top', 730),
																	#('orientRotationTweakAllMinus', 'left', 94),

																	#('orientRotationTweakXPlus', 'top', 700),
																	#('orientRotationTweakXPlus', 'left', 147),

																	#('orientRotationTweakXMinus', 'top', 730),
																	#('orientRotationTweakXMinus', 'left', 147),

																	#('orientRotationTweakYPlus', 'top', 700),
																	#('orientRotationTweakYPlus', 'left', 200),

																	#('orientRotationTweakYMinus', 'top', 730),
																	#('orientRotationTweakYMinus', 'left', 200),

																	#('orientRotationTweakZPlus', 'top', 700),
																	#('orientRotationTweakZPlus', 'left', 253),

																	#('orientRotationTweakZMinus', 'top', 730),
																	#('orientRotationTweakZMinus', 'left', 253)

																	] )
	cmds.setParent( '..' )

	# -------------------------------------------------------------------------------------------------------------------
	# Limb tab layout
	cmds.formLayout('limbForm')

	cmds.separator('separator01', height=10, style='in')
	cmds.radioButtonGrp('fkOrIkFk', numberOfRadioButtons=2, labelArray2=('FK','IK / FK'), select=1, columnWidth2=(60,60),
							onCommand2=fkOrIkFkSetting, offCommand2=fkOrIkFkSetting)
	cmds.optionMenuGrp('ikFkSystemChoice', enable=False, label='Limb Type', columnWidth=(1,128), changeCommand=LimbType)
	cmds.menuItem(label='Biped - Arm')
	cmds.menuItem(label='Biped - Leg')
	cmds.menuItem(divider=True)
	cmds.menuItem(label='Quadruped - Front', enable=False)
	cmds.menuItem(label='Quadruped - Rear', enable=False)
	cmds.optionMenuGrp('sideChoice', enable=False, label='Side / Center', columnWidth=(1,128),  changeCommand=Side)
	cmds.menuItem(label='Left')
	cmds.menuItem(label='Right')
	cmds.menuItem(label='Center')
	cmds.textFieldGrp('customGlobalControlName', enable=False, label='Global Control Name:', placeholderText='l_arm_ctrl', columnWidth2=(129,200))
	cmds.radioButtonGrp('ikControlOrientation', enable=False, label='IK Control Orientation', numberOfRadioButtons=2, labelArray2=('Joint','World'), select=1, columnWidth3=(128,60,60))
	cmds.checkBoxGrp('twistStretchCheck', enable=False, label='Addons	', numberOfCheckBoxes=2, labelArray2=['Twist', 'Stretch'], columnWidth3=[127,60,50], changeCommand1=TwistSetting)
	cmds.intSliderGrp('twistJointAmount', enable=False, label='Twist Joint Amount	', field=True, columnWidth3=(128,40,10), min=2, max=4, fieldMaxValue=10, value=2)
	cmds.text('jointPrimaryAxisText', label='Joint Primary Axis:')
	cmds.radioButtonGrp('jointPrimaryAxis', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth3=(40,40,40))
	cmds.checkBox('invertJointPrimaryAxis', label='Invert')
	cmds.colorIndexSliderGrp('ikFkControlColor', label='Control Color	', columnWidth3=(90,80,100), width=350, min=0, max=20, value=6)
	cmds.floatSliderGrp('ikFkControlSize', label='Control Size	', field=True, columnWidth3=(90,40,10), min=1, max=20, fieldMaxValue=100, value=1)
	cmds.textFieldGrp('constraintSystemTo', label='Constraint System To:', placeholderText='None', columnWidth2=(129,200))
	cmds.button('buildIkFk', label="Build FK or IK/FK", width=108, command=IkFkUiData)
	cmds.text('limbTooltip', font='boldLabelFont', label='Tooltip')
	cmds.text('limbTooltipContent1', wordWrap=True, label='The joints require a prefix and suffix indicated with an "_"')
	cmds.text('limbTooltipContent2', wordWrap=True, label='Eg. "l_armUpper_jnt"')
	cmds.text('limbTooltipContent3', wordWrap=True, label='Select the first and last joint in the limb chain.')
	cmds.text('limbTooltipContent4', wordWrap=True, label='Eg. the upper arm and wrist.')

	limbTab = cmds.formLayout( 'limbForm', edit=True, attachForm=[
																	('separator01', 'top', 0),
																	('separator01', 'left', 0),
																	('separator01', 'right', 0),

																	('fkOrIkFk', 'top', 10),
																	('fkOrIkFk', 'left', 130),

																	('ikFkSystemChoice', 'top', 40),
																	('ikFkSystemChoice', 'left', 0),
																	('ikFkSystemChoice', 'right', 0),

																	('sideChoice', 'top', 70),
																	('sideChoice', 'left', 0),
																	('sideChoice', 'right', 0),

																	('customGlobalControlName', 'top', 100),
																	('customGlobalControlName', 'left', 0),

																	('ikControlOrientation', 'top', 130),
																	('ikControlOrientation', 'left', 0),

																	('twistStretchCheck', 'top', 160),
																	('twistStretchCheck', 'left', 0),

																	('twistJointAmount', 'top', 190),
																	('twistJointAmount', 'left', 0),
																	('twistJointAmount', 'right', 5),

																	('jointPrimaryAxisText', 'top', 220),
																	('jointPrimaryAxisText', 'left', 0),
																	('jointPrimaryAxisText', 'right', 0),

																	('jointPrimaryAxis', 'top', 235),
																	('jointPrimaryAxis', 'left', 120),

																	('invertJointPrimaryAxis', 'top', 237),
																	('invertJointPrimaryAxis', 'left', 250),

																	('ikFkControlColor', 'top', 265),
																	('ikFkControlColor', 'left', 0),
																	('ikFkControlColor', 'right', 5),

																	('ikFkControlSize', 'top', 295),
																	('ikFkControlSize', 'left', 0),
																	('ikFkControlSize', 'right', 5),

																	('constraintSystemTo', 'top', 325),
																	('constraintSystemTo', 'left', 0),

																	('buildIkFk', 'top', 355),
																	('buildIkFk', 'left', 20),
																	('buildIkFk', 'right', 20),

																	('limbTooltip', 'top', 400),
																	('limbTooltip', 'left', 20),
																	('limbTooltip', 'right', 20),

																	('limbTooltipContent1', 'top', 420),
																	('limbTooltipContent1', 'left', 20),
																	('limbTooltipContent1', 'right', 20),

																	('limbTooltipContent2', 'top', 435),
																	('limbTooltipContent2', 'left', 20),
																	('limbTooltipContent2', 'right', 20),

																	('limbTooltipContent3', 'top', 455),
																	('limbTooltipContent3', 'left', 20),
																	('limbTooltipContent3', 'right', 20),

																	('limbTooltipContent4', 'top', 470),
																	('limbTooltipContent4', 'left', 20),
																	('limbTooltipContent4', 'right', 20)
																	] )
	cmds.setParent( '..' )
	
	# -------------------------------------------------------------------------------------------------------------------
	# Ribbon tab layout
	cmds.formLayout('ribbonForm')

	# Ribbon
	cmds.separator('separator01', height=10, style='in')
	cmds.textFieldGrp('ribbonName', label='Ribbon Name:	', placeholderText='l_leg_ribbon', columnWidth2=(95,230))
	cmds.floatSliderGrp('ribbonLength', label='Ribbon Length	', field=True, columnWidth3=(95,40,10), min=1, value=1)
	cmds.text('ribbonOrientationText', label='Ribbon Facing Orientation:', annotation='Which axis should the ribbon face be facing?')
	cmds.radioButtonGrp('ribbonOrientation', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth3=(40,40,40), annotation='Which axis should the ribbon face be facing?')
	cmds.radioButtonGrp('ribbonDirection', label='Ribbon Direction	', numberOfRadioButtons=2, labelArray2=('Horizontal','Vertical'), select=1, columnWidth3=(118,82,80), 
							annotation='If orientation = Y, then "Horizontal" lays the ribbon along the X axis "Vertical" lays it along the Z axis.')
	cmds.intSliderGrp('ribbonJointNumber', label='Joint Number	', field=True, columnWidth3=(95,40,10), min=3, max=20, fieldMaxValue=100, value=1)
	cmds.text('ribbonJointOrientText', label='Joint Axis Aimed Along Ribbon:')
	cmds.radioButtonGrp('ribbonJointOrient', numberOfRadioButtons=3, labelArray3=('X','Y','Z'), select=1, columnWidth3=(40,40,40))
	cmds.checkBox('invertRibbonJointOrient', label='Invert')
	cmds.checkBoxGrp('ribbonAddControls', label='Add Controls	', columnWidth2=(117,40), changeCommand1=AddControls)
	cmds.colorIndexSliderGrp('ribbonControlColor', enable=False, label='Control Color	', columnWidth3=(95,80,100), width=350, min=0, max=20, value=6)
	cmds.button('buildRibbon', label="Build Ribbon", width=108, command=RibbonUiData)

	ribbonTab = cmds.formLayout( 'ribbonForm', edit=True, attachForm=[
																	# Ribbon
																	('separator01', 'top', 0),
																	('separator01', 'left', 0),
																	('separator01', 'right', 0),

																	('ribbonName', 'top', 10),
																	('ribbonName', 'left', 0),

																	('ribbonLength', 'top', 40),
																	('ribbonLength', 'left', 0),
																	('ribbonLength', 'right', 5),

																	('ribbonOrientationText', 'top', 70),
																	('ribbonOrientationText', 'left', 0),
																	('ribbonOrientationText', 'right', 0),

																	('ribbonOrientation', 'top', 85),
																	('ribbonOrientation', 'left', 120),

																	('ribbonDirection', 'top', 115),
																	('ribbonDirection', 'left', 0),

																	('ribbonJointNumber', 'top', 145),
																	('ribbonJointNumber', 'left', 0),
																	('ribbonJointNumber', 'right', 5),

																	('ribbonJointOrientText', 'top', 175),
																	('ribbonJointOrientText', 'left', 0),
																	('ribbonJointOrientText', 'right', 0),

																	('ribbonJointOrient', 'top', 190),
																	('ribbonJointOrient', 'left', 120),

																	('invertRibbonJointOrient', 'top', 192),
																	('invertRibbonJointOrient', 'left', 250),

																	('ribbonAddControls', 'top', 220),
																	('ribbonAddControls', 'left', 0),

																	('ribbonControlColor', 'top', 247),
																	('ribbonControlColor', 'left', 0),
																	('ribbonControlColor', 'right', 5),

																	('buildRibbon', 'top', 275),
																	('buildRibbon', 'left', 20),
																	('buildRibbon', 'right', 20)
																	] )
	cmds.setParent( '..' )

	# -------------------------------------------------------------------------------------------------------------------
	# Experimental tab layout
	cmds.formLayout('experimentalForm')

	cmds.separator('separator01', height=10, style='in')

	# Label joints in the scene
	cmds.text('labelJointsText', label='Label all joints according to their name.\n'
										'Removes the chosen prefix from the label.')
	cmds.textFieldGrp('labelLeftPrefix', label='Left Prefix:	', placeholderText='l_', columnWidth2=(105,225))
	cmds.textFieldGrp('labelRightPrefix', label='Right Prefix:	', placeholderText='r_', columnWidth2=(105,225))
	cmds.button('labelJoints', label="Label Joints", width=108, command=LabelJoints)
	cmds.separator('separator02', height=10)

	# Constraint group 1 to group 2
	cmds.text('constraintGroupText', label='Constraint first selection to second selection.\n'
										'See help tab for more info.')
	cmds.optionMenuGrp('constraintGroupType', label='Constraint Type', columnWidth=(1,110))
	cmds.menuItem(label='Parent')
	cmds.menuItem(label='Point')
	cmds.menuItem(label='Orient')
	cmds.checkBox('constraintGroupsOffset', label='Maintain Offset')
	cmds.button('constraintGroups', label="Constraint Selected Groups", width=108, command=ConstraintGroups)
	cmds.separator('separator03', height=10)

	# Parent group 1 to group 2
	cmds.text('parentGroupText', label='Parent first selection to second selection.\n'
										'See help tab for more info.')
	cmds.button('parentGroups', label="Parent Selected Groups", width=108, command=ParentGroups)

	experimentalTab = cmds.formLayout( 'experimentalForm', edit=True, attachForm=[
																				('separator01', 'top', 0),
																				('separator01', 'left', 0),
																				('separator01', 'right', 0),

																				# Label joints in the scene

																				('labelJointsText', 'top', 10),
																				('labelJointsText', 'left', 0),
																				('labelJointsText', 'right', 0),

																				('labelLeftPrefix', 'top', 40),
																				('labelLeftPrefix', 'left', 0),

																				('labelRightPrefix', 'top', 60),
																				('labelRightPrefix', 'left', 0),

																				('labelJoints', 'top', 90),
																				('labelJoints', 'left', 20),
																				('labelJoints', 'right', 20),

																				('separator02', 'top', 120),
																				('separator02', 'left', 5),
																				('separator02', 'right', 5),

																				# Constraint group 1 to group 2

																				('constraintGroupText', 'top', 135),
																				('constraintGroupText', 'left', 0),
																				('constraintGroupText', 'right', 0),

																				('constraintGroupType', 'top', 165),
																				('constraintGroupType', 'left', 0),
																				('constraintGroupType', 'right', 0),

																				('constraintGroupsOffset', 'top', 168),
																				('constraintGroupsOffset', 'left', 215),

																				('constraintGroups', 'top', 195),
																				('constraintGroups', 'left', 20),
																				('constraintGroups', 'right', 20),

																				('separator03', 'top', 225),
																				('separator03', 'left', 5),
																				('separator03', 'right', 5),

																				# Parent group 1 to group 2

																				('parentGroupText', 'top', 240),
																				('parentGroupText', 'left', 0),
																				('parentGroupText', 'right', 0),

																				('parentGroups', 'top', 270),
																				('parentGroups', 'left', 20),
																				('parentGroups', 'right', 20)
																				] )
	cmds.setParent( '..' )

	# -------------------------------------------------------------------------------------------------------------------
	# Help tab layout
	cmds.formLayout('helpForm')

	cmds.separator('separator01', height=10, style='in')
	cmds.button('controlsTab', label="Controls Tab", width=108, command=ControlsHelp)
	cmds.button('jointsTab', label="Joints Tab", width=108, command=JointsHelp)
	cmds.button('limbTab', label="Limb Tab", width=108, command=LimbHelp)
	cmds.button('ribbonTab', label="Ribbon Tab", width=108, command=RibbonHelp)
	cmds.button('experimentalTab', label="Experimental Tab", width=108, command=ExperimentalHelp)
	cmds.text('generalTips', font='boldLabelFont', label='General Tips')
	cmds.text('textFields', label='All text fields can be left empty.')
	cmds.text('contactMe', font='boldLabelFont', label='Contact Me')
	cmds.text('contactInfo1', label="I will gladly talk about this or other tools,\nimprovements and ideas in general :)")
	cmds.text('contactInfo2', font='boldLabelFont', label='jonnyheinonen.com')

	helpTab = cmds.formLayout( 'helpForm', edit=True, attachForm=[
																	('separator01', 'top', 0),
																	('separator01', 'left', 0),
																	('separator01', 'right', 0),

																	('controlsTab', 'top', 15),
																	('controlsTab', 'left', 20),
																	('controlsTab', 'right', 20),

																	('jointsTab', 'top', 65),
																	('jointsTab', 'left', 20),
																	('jointsTab', 'right', 20),

																	('limbTab', 'top', 115),
																	('limbTab', 'left', 20),
																	('limbTab', 'right', 20),

																	('ribbonTab', 'top', 165),
																	('ribbonTab', 'left', 20),
																	('ribbonTab', 'right', 20),

																	('experimentalTab', 'top', 215),
																	('experimentalTab', 'left', 20),
																	('experimentalTab', 'right', 20),

																	('generalTips', 'top', 265),
																	('generalTips', 'left', 20),
																	('generalTips', 'right', 20),

																	('textFields', 'top', 280),
																	('textFields', 'left', 20),
																	('textFields', 'right', 20),

																	('contactMe', 'top', 365),
																	('contactMe', 'left', 20),
																	('contactMe', 'right', 20),

																	('contactInfo1', 'top', 380),
																	('contactInfo1', 'left', 20),
																	('contactInfo1', 'right', 20),

																	('contactInfo2', 'top', 425),
																	('contactInfo2', 'left', 20),
																	('contactInfo2', 'right', 20)
																	] )
	cmds.setParent( '..' )

	# -------------------------------------------------------------------------------------------------------------------
	# Add the layouts to one tab each
	cmds.tabLayout( tabs, edit=True, tabLabel=((controlTab, 'Controls'), (jointTab, 'Joints'), (limbTab, 'Limb'), (ribbonTab, 'Ribbon'), (experimentalTab, 'Experimental'), (helpTab, 'Help')) )

	# Show the window
	cmds.showWindow(window)

# ====================================================================================================================
#
# SIGNATURES:
#	UpdateControlSizeLive(onOff=1)
#	DoNothing(*args)
#	CreateControlCircle(*args):
#	CreateControlSquare(*args):
#	CreateControlRomb(*args):
#	CreateControlPlus(*args):
#	CreateControlArrow(*args):
#	CreateControlCube(*args):
#	CreateControlSphere(*args):
#	CreateControlLollipop(*args):
#	CreateControlOrient(*args):
#	CreateControlOrientHalf(*args):
#	CreateControlArrows(*args):
#	CreateControlCuteHead(*args):
#
#	LocatorOrJointOnCenter(onOff=1)
#	OrientJointToWorld(onOff=1)
#
#	fkOrIkFkSetting(onOff=1)
#	LimbType(*args)
#	Side(*args)
#	TwistSetting(onOff=1)
#
#	AddControls(onOff=1)
#
# DESCRIPTION:
#	Checks the condition of the an option to lock/unlock related options.
# 
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# ====================================================================================================================

# Controls tab query
def UpdateControlColorLive(onOff=1):

	if onOff == 1:
		cmds.colorIndexSliderGrp('controlColor', edit=True, changeCommand=UpdateControlColor)
	elif onOff == 0:
		cmds.colorIndexSliderGrp('controlColor', edit=True, changeCommand=DoNothing)

def UpdateControlSizeLive(onOff=1):

	if onOff == 1:
		cmds.floatSliderGrp('controlSize', edit=True, changeCommand=UpdateControlSize)
	elif onOff == 0:
		cmds.floatSliderGrp('controlSize', edit=True, changeCommand=DoNothing)

# Controls tab query
def DoNothing(*args):

	nothing = None

# Control tab control creation
def CreateControlCircle(*args):
	CreateControl('circle')

def CreateControlSquare(*args):
	CreateControl('square')

def CreateControlRomb(*args):
	CreateControl('romb')

def CreateControlPlus(*args):
	CreateControl('plus')

def CreateControlArrow(*args):
	CreateControl('arrow')

def CreateControlCube(*args):
	CreateControl('cube')

def CreateControlSphere(*args):
	CreateControl('sphere')

def CreateControlLollipop(*args):
	CreateControl('lollipop')

def CreateControlOrient(*args):
	CreateControl('orient')

def CreateControlOrientHalf(*args):
	CreateControl('orientHalf')

def CreateControlArrows(*args):
	CreateControl('arrows')

def CreateControlCuteHead(*args):
	CreateControl('cuteHead')


# -------------------------------------------------------------------------------------------------------------------
# Joint tab query
def LocatorOrJointOnCenter(onOff=1):

	if onOff == 1:
		cmds.optionMenuGrp('jointOnCenterRotationOrder', edit=True, enable=True)
	elif onOff == 0:
		cmds.optionMenuGrp('jointOnCenterRotationOrder', edit=True, enable=False)

# Joint tab query
def OrientJointToWorld(onOff=1):

	if onOff == 1:
		cmds.radioButtonGrp('orientPrimaryAxis', edit=True, enable=False)
		cmds.optionMenuGrp('orientPrimaryAxisInvert', edit=True, enable=False)
		cmds.radioButtonGrp('orientSecondaryAxis', edit=True, enable=False)
		cmds.radioButtonGrp('orientSecondaryAxisAim', edit=True, enable=False)
		cmds.optionMenuGrp('orientSecondaryAxisInvert', edit=True, enable=False)
	elif onOff == 0:
		cmds.radioButtonGrp('orientPrimaryAxis', edit=True, enable=True)
		cmds.optionMenuGrp('orientPrimaryAxisInvert', edit=True, enable=True)
		cmds.radioButtonGrp('orientSecondaryAxis', edit=True, enable=True)
		cmds.radioButtonGrp('orientSecondaryAxisAim', edit=True, enable=True)
		cmds.optionMenuGrp('orientSecondaryAxisInvert', edit=True, enable=True)

# -------------------------------------------------------------------------------------------------------------------
# IK/FK tab query
def fkOrIkFkSetting(onOff=1):

	if onOff == 1:
		cmds.optionMenuGrp('ikFkSystemChoice', edit=True, enable=True)
		cmds.optionMenuGrp('sideChoice', edit=True, enable=True)
		cmds.textFieldGrp('customGlobalControlName', edit=True, enable=True)
		cmds.radioButtonGrp('ikControlOrientation', edit=True, enable=True)
		cmds.checkBoxGrp('twistStretchCheck', edit=True, enable=True)
	elif onOff == 0:
		cmds.optionMenuGrp('ikFkSystemChoice', edit=True, enable=False)
		cmds.optionMenuGrp('sideChoice', edit=True, enable=False)
		cmds.textFieldGrp('customGlobalControlName', edit=True, enable=False)
		cmds.radioButtonGrp('ikControlOrientation', edit=True, enable=False)
		cmds.checkBoxGrp('twistStretchCheck', edit=True, enable=False)
		cmds.intSliderGrp('twistJointAmount', edit=True, enable=False)
	if onOff == 1 and cmds.checkBoxGrp('twistStretchCheck', query=True, value1=1):
		cmds.intSliderGrp('twistJointAmount', edit=True, enable=True)

# IK/FK tab query
def LimbType(*args):

	side = cmds.optionMenuGrp('sideChoice', query=True, value=True)
	if side == 'Left':
		side = 'l'
	if side == 'Right':
		side = 'r'
	if side == 'Center':
		side = 'c'

	limbType = cmds.optionMenuGrp('ikFkSystemChoice', query=True, value=True)

	if limbType == 'Biped - Arm':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'{side}_arm_ctrl')
	elif limbType == 'Biped - Leg':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'{side}_leg_ctrl')
	elif limbType == 'Quadruped - Front':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'{side}_frontLeg_ctrl')
	elif limbType == 'Quadruped - Rear':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'{side}_rearLeg_ctrl')

# IK/FK tab query
def Side(*args):

	limbType = cmds.optionMenuGrp('ikFkSystemChoice', query=True, value=True)
	if limbType == 'Biped - Arm':
		limbType = 'arm_ctrl'
	if limbType == 'Biped - Leg':
		limbType = 'leg_ctrl'
	if limbType == 'Quadruped - Front':
		limbType = 'frontLeg_ctrl'
	if limbType == 'Quadruped - Rear':
		limbType = 'rearLeg_ctrl'

	side = cmds.optionMenuGrp('sideChoice', query=True, value=True)

	if side == 'Left':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'l_{limbType}')
	elif side == 'Right':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'r_{limbType}')
	elif side == 'Center':
		cmds.textFieldGrp('customGlobalControlName', edit=True, placeholderText=f'c_{limbType}')

# IK/FK tab query
def TwistSetting(onOff=1):

	if onOff == 1:
		cmds.intSliderGrp('twistJointAmount', edit=True, enable=True)
	elif onOff == 0:
		cmds.intSliderGrp('twistJointAmount', edit=True, enable=False)

# -------------------------------------------------------------------------------------------------------------------
# Ribbon tab query
def AddControls(onOff=1):

	if onOff == 1:
		cmds.colorIndexSliderGrp('ribbonControlColor', edit=True, enable=True)
	elif onOff == 0:
		cmds.colorIndexSliderGrp('ribbonControlColor', edit=True, enable=False)

# ====================================================================================================================
#
# SIGNATURES:
#	ControlsHelp(*args)
#	JointsHelp(*args)
#	LimbHelp(*args)
#	RibbonHelp(*args)
#	ExperimentalHelp(*args)
#
# DESCRIPTION:
#	Creates a window with help text.
# 
# REQUIRES:
# 	Nothing
#
# RETURNS:
#	Nothing
#
# NOTES:
#	Spacing of 30 to a new category + 10 per line of text in the previous category
#
# ====================================================================================================================

def ControlsHelp(*args):
	if cmds.window('controlsHelpWindow', exists=True):
		cmds.deleteUI('controlsHelpWindow')

	controlsHelpWindow = cmds.window('controlsHelpWindow', title='Controls Help', width=720, height=365, sizeable=False)

	cmds.formLayout('controlsHelpForm', numberOfDivisions=100)

	cmds.text('creating1', wordWrap=False, font='boldLabelFont', label='CREATING')
	cmds.text('creating2', wordWrap=False, label=
		'A control of the desired shape is created for each selected object, placed at and named based on the object.\n'
		'If nothing is selected, one control is created at origo.')
	cmds.text('color1', wordWrap=False, font='boldLabelFont', label='COLOR')
	cmds.text('color2', wordWrap=False, label=
		'The control color "Update Live" checkbox enables the color to be updated at the release of the slider.')
	cmds.text('scaling1', wordWrap=False, font='boldLabelFont', label='SCALING')
	cmds.text('scaling2', wordWrap=False, label=
		'The control size "Update Live" checkbox enables the size to be updated at the release of the slider.\n\n'
		'A control with multiple shapes can currently not update its size.')
	cmds.text('replace1', wordWrap=False, font='boldLabelFont', label='REPLACING SHAPES')
	cmds.text('replace2', wordWrap=False, label=
		"The control's shapes can't share the same name.\n\n"
		'Make sure both controls are in the same position in world space and are zeroed out (frozen).\nThe resulting control could become invisible when executing the script, but moving it and undoing the movement should make it visible.')
	cmds.text('other1', wordWrap=False, font='boldLabelFont', label='OTHER')
	cmds.text('other2', wordWrap=False, label=
		'''"Select Control CV's" puts the user in component selection mode.\n\n'''
		"The snapping options work like constraints but don't maintain a connection between the objects.")

	cmds.formLayout('controlsHelpForm', edit=True, attachForm=[
															('creating1', 'top', 10),
															('creating1', 'left', 0),
															('creating1', 'right', 0),

															('creating2', 'top', 25),
															('creating2', 'left', 0),
															('creating2', 'right', 0),

															('color1', 'top', 75),
															('color1', 'left', 0),
															('color1', 'right', 0),

															('color2', 'top', 90),
															('color2', 'left', 0),
															('color2', 'right', 0),

															('scaling1', 'top', 130),
															('scaling1', 'left', 0),
															('scaling1', 'right', 0),

															('scaling2', 'top', 145),
															('scaling2', 'left', 0),
															('scaling2', 'right', 0),

															('replace1', 'top', 205),
															('replace1', 'left', 0),
															('replace1', 'right', 0),

															('replace2', 'top', 220),
															('replace2', 'left', 0),
															('replace2', 'right', 0),

															('other1', 'top', 290),
															('other1', 'left', 0),
															('other1', 'right', 0),

															('other2', 'top', 305),
															('other2', 'left', 0),
															('other2', 'right', 0)
															])
	cmds.showWindow(controlsHelpWindow)

def JointsHelp(*args):
	if cmds.window('jointsHelpWindow', exists=True):
		cmds.deleteUI('jointsHelpWindow')

	jointsHelpWindow = cmds.window('jointsHelpWindow', title='Joints Help', width=440, height=200, sizeable=False)

	cmds.formLayout('jointsHelpForm', numberOfDivisions=100)

	cmds.text('creatingFirst1', wordWrap=False, font='boldLabelFont', label='CREATE JOINTS')
	cmds.text('creatingFirst2', wordWrap=False, label=
		'"Joint Spacing" is the distance between each joint when created.\n\n'
		'"Spacing Direction" is the world axis that the joint chain will build along.')
	cmds.text('creatingSecond1', wordWrap=False, font='boldLabelFont', label='CREATE LOCATOR/JOINT')
	cmds.text('creatingSecond2', wordWrap=False, label=
		'Places a locator or joint at the center of your object or component selection.')
	cmds.text('tooltip1', wordWrap=False, font='boldLabelFont', label='GENERAL TIP')
	cmds.text('tooltip2', wordWrap=False, label=
		"If joints created with this tool disappear: Create a joint with Maya's own tool.\n"
		"This tends to happen when origo is not in the viewport until Maya's tool is used.")

	cmds.formLayout('jointsHelpForm', edit=True, attachForm=[
															('creatingFirst1', 'top', 10),
															('creatingFirst1', 'left', 0),
															('creatingFirst1', 'right', 0),

															('creatingFirst2', 'top', 25),
															('creatingFirst2', 'left', 0),
															('creatingFirst2', 'right', 0),

															('creatingSecond1', 'top', 85),
															('creatingSecond1', 'left', 0),
															('creatingSecond1', 'right', 0),

															('creatingSecond2', 'top', 100),
															('creatingSecond2', 'left', 0),
															('creatingSecond2', 'right', 0),

															('tooltip1', 'top', 140),
															('tooltip1', 'left', 0),
															('tooltip1', 'right', 0),

															('tooltip2', 'top', 155),
															('tooltip2', 'left', 0),
															('tooltip2', 'right', 0)
															])
	cmds.showWindow(jointsHelpWindow)

def LimbHelp(*args):
	if cmds.window('limbHelpWindow', exists=True):
		cmds.deleteUI('limbHelpWindow')

	limbHelpWindow = cmds.window('limbHelpWindow', title='Limb Help', width=655, height=290, sizeable=False)

	cmds.formLayout('limbHelpForm', numberOfDivisions=100)

	cmds.text('howTo1', wordWrap=False, font='boldLabelFont', label='HOW TO')
	cmds.text('howTo2', wordWrap=False, label=
		'Select the first and last joint in a chain that you want to build the system on.\n'
		'The joints require a prefix and suffix indicated with an underscore, eg. "l_wrist_jnt".\n\n'
		'The joint primary axis is used to align controls during creation.\n\n'
		'"Constraint System To" will be the object that drives the fk or ik/fk system, eg. the clavicle when creating an arm.')
	cmds.text('fk1', wordWrap=False, font='boldLabelFont', label='FK')
	cmds.text('fk2', wordWrap=False, label=
		"The FK system currently needs a start and an end and therefore can't build an FK system for a single joint.")
	cmds.text('ikFk1', wordWrap=False, font='boldLabelFont', label='IK/FK')
	cmds.text('ikFk2', wordWrap=False, label=
		'"Limb Type" for now only changes the attributes given to objects of the system, as quadruped limbs are yet to be supported.\n'
		'Same goes for "Side / Center".')
	cmds.text('twist1', wordWrap=False, font='boldLabelFont', label='TWIST')
	cmds.text('twist2', wordWrap=False, label=
		'The twist amount for each twist joint can be changed on the global control.')

	cmds.formLayout('limbHelpForm', edit=True, attachForm=[
															('howTo1', 'top', 10),
															('howTo1', 'left', 0),
															('howTo1', 'right', 0),

															('howTo2', 'top', 25),
															('howTo2', 'left', 0),
															('howTo2', 'right', 0),

															('fk1', 'top', 125),
															('fk1', 'left', 0),
															('fk1', 'right', 0),

															('fk2', 'top', 140),
															('fk2', 'left', 0),
															('fk2', 'right', 0),

															('ikFk1', 'top', 180),
															('ikFk1', 'left', 0),
															('ikFk1', 'right', 0),

															('ikFk2', 'top', 195),
															('ikFk2', 'left', 0),
															('ikFk2', 'right', 0),

															('twist1', 'top', 245),
															('twist1', 'left', 0),
															('twist1', 'right', 0),

															('twist2', 'top', 260),
															('twist2', 'left', 0),
															('twist2', 'right', 0)
															])
	cmds.showWindow(limbHelpWindow)

def RibbonHelp(*args):
	if cmds.window('ribbonHelpWindow', exists=True):
		cmds.deleteUI('ribbonHelpWindow')

	ribbonHelpWindow = cmds.window('ribbonHelpWindow', title='Ribbon Help', width=575, height=120, sizeable=False)

	cmds.formLayout('ribbonHelpForm', numberOfDivisions=100)

	cmds.text('howTo1', wordWrap=False, font='boldLabelFont', label='HOW TO')
	cmds.text('howTo2', wordWrap=False, label=
		'"Ribbon Facing Orientetion" is the world axis that the nurbs face will be facing.\n\n'
		'"Ribbon Direction" is the direction based on the "Ribbon Facing Orientation",\n'
		'eg. going up/down or left/right when looking in the world axis the user have chosen.\n\n'
		'Controls are added to the start and end of the ribbon, and the middle when using an odd number of joints.')

	cmds.formLayout('ribbonHelpForm', edit=True, attachForm=[
															('howTo1', 'top', 10),
															('howTo1', 'left', 0),
															('howTo1', 'right', 0),

															('howTo2', 'top', 25),
															('howTo2', 'left', 0),
															('howTo2', 'right', 0)
															])
	cmds.showWindow(ribbonHelpWindow)

def ExperimentalHelp(*args):
	if cmds.window('experimentalHelpWindow', exists=True):
		cmds.deleteUI('experimentalHelpWindow')

	experimentalHelpWindow = cmds.window('experimentalHelpWindow', title='Experimental Help', width=580, height=104, sizeable=False)

	cmds.formLayout('experimentalHelpForm', numberOfDivisions=100)

	cmds.text('groupConstrantOrParent1', wordWrap=False, font='boldLabelFont', label='GROUP CONSTRAINING / PARENTING')
	cmds.text('groupConstrantOrParent2', wordWrap=False, label=
		'Constraints / parents the first half of your selection to the second half of your selection. One for one in order.\n\n'
		'If you select "control 1", "control 2", "joint 1" and "joint 2" in this order,\n'
		'then "control 1" will be constrained / parented to "joint 1"\n'
		'and "control 2" will be constrained / parented to joint 2".')

	cmds.formLayout('experimentalHelpForm', edit=True, attachForm=[
															('groupConstrantOrParent1', 'top', 10),
															('groupConstrantOrParent1', 'left', 0),
															('groupConstrantOrParent1', 'right', 0),

															('groupConstrantOrParent2', 'top', 25),
															('groupConstrantOrParent2', 'left', 0),
															('groupConstrantOrParent2', 'right', 0)
															])
	cmds.showWindow(experimentalHelpWindow)