"""
Match IKFK SCRIPT
Created by Alva Stenhammar

Match the pose of FK to IK controls and vice versa.

"""

import maya.cmds as cmds
import functools



def _______________UI_______________(): pass


def toggleAttributeOptions(attributeObjectBox: str,
                           attributeObjectField: str,
                           *args):
    """ Toggle the attribute options. """

    if cmds.checkBox(attributeObjectBox, query=True, value=True) == True:
        cmds.textField(attributeObjectField, edit=True, enable=True)
    else:
        cmds.textField(attributeObjectField, edit=True, enable=False)



def insertSeparator(parent: str):
    """ Create custom separator. """

    cmds.separator(height=2,
                  style="none",
                  backgroundColor=(0.2, 0.2, 0.2),
                  parent=parent)



def createColumnLayout(parent: str) -> str:
    """
    Create row/column layout with custom settings.

    Return layout's full path name.
    """

    layout = cmds.rowColumnLayout(numberOfColumns=2,
                                  columnWidth=[(1, 130), (2, 130)],
                                  columnOffset=[(1, "right", 10), (2, "left", 10)],
                                  rowSpacing=(1, 5),
                                  parent=parent)
    
    return cmds.rowColumnLayout(layout, query=True, fullPathName=True)



def createFrameLayout(label: str, parent: str) -> str:
    """
    Create frame layout layout with custom settings.

    Return layout's full path name.
    """

    layout = cmds.frameLayout(label=label,
                              width=300,
                              marginWidth=20,
                              marginHeight=10,
                              backgroundShade=True,
                              font="boldLabelFont",
                              parent=parent)
    
    return cmds.frameLayout(layout, query=True, fullPathName=True)



def createButton(label: str, parent: str) -> str:
    """
    Create button with custom settings.
    
    Return button's full path name.
    """

    cmds.rowLayout(numberOfColumns=1,
                   columnWidth=(1, 260),
                   parent=parent)
    
    button = cmds.button(label=label,
                         width=260)
    
    return cmds.button(button, query=True, fullPathName=True)



def createUI(matchFKtoIK, matchIKtoFK):
    """ Create and open the UI. """


    # WINDOW CREATION
    windowID = "matchIKFKWindowID"
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, title=f"Match IK/FK", sizeable=True)


    # LAYOUTS
    mainLayout = cmds.columnLayout(width=310, margins=5)

    cmds.columnLayout(margins=10,
                      parent=mainLayout)
    cmds.text(label="Match IK/FK Tool",
              width=280,
              font="boldLabelFont")
    cmds.separator(height=10, style="none")


    # LAYOUT SETUP
    layout = createFrameLayout("Options", mainLayout)
    cmds.separator(height=5, style="none", parent=mainLayout)
    
    cmds.text(label="Select the shoulder or hip bind joint to match poses.",
                width=260, height=10,
                font="smallPlainLabelFont")
    insertSeparator(layout)

    cmds.separator(height=5, style="none", parent=mainLayout)


    createColumnLayout(parent=layout)
    

    matchFKtoIKbutton = createButton("Match FK > IK", layout)
    matchIKtoFKbutton = createButton("Match IK > FK", layout)


    # CREDITS TEXT
    cmds.columnLayout(margins=10,
                        parent=mainLayout)
    
    cmds.separator(height=5,
                    style="none")
    
    cmds.text(label="Created by Alva Stenhammar", width=280,
                font="obliqueLabelFont")
    

    # ADD COMMANDS
    # control options
    cmds.button(matchFKtoIKbutton, edit=True,
                command=functools.partial(matchFKtoIK))

    cmds.button(matchIKtoFKbutton, edit=True,
                command=functools.partial(matchIKtoFK))


    cmds.showWindow()



def _______________BUILD_______________(): pass


def matchFKtoIK(*args):
    """ Match the FK controls to the IK joints' position. """

    # create list of ik joints
    ikJointList = []

    rootJoint = cmds.ls(selection=True, type="joint")[0]
    midJoint = cmds.listRelatives(rootJoint, type="joint")[0]
    endJoint = cmds.listRelatives(midJoint, type="joint")[0]

    jointChain = [rootJoint, midJoint, endJoint]

    for joint in jointChain:
        ikJointList.append(joint.replace("BIND", "IK"))

    # create list of fk controls
    fkControlList = []

    for joint in jointChain:
        fkControlList.append(joint.replace("BIND_JNT", "FK_CTRL"))


    # match fk control's transform to ik joints
    for i in range(3):
        cmds.matchTransform(fkControlList[i], ikJointList[i])

    cmds.select(clear=True)



def matchIKtoFK(*args):
    """ Match the IK controls to the FK joints' position. """

    # create list of fk joints
    fkJointList = []
    
    rootJoint = cmds.ls(selection=True, type="joint")[0]
    midJoint = cmds.listRelatives(rootJoint, type="joint")[0]
    endJoint = cmds.listRelatives(midJoint, type="joint")[0]

    jointChain = [rootJoint, midJoint, endJoint]

    for joint in jointChain:
        fkJointList.append(joint.replace("BIND", "FK"))

    # get ik controls
    if rootJoint.split("_")[1] == "shoulder":
        limbType = "arm"
    else:
        limbType = "leg"

    limbSide = rootJoint[0]
    limb = f"{limbSide}_{limbType}"

    ikControl = f"{limb}_IK_CTRL"
    pvControl = f"{limb}_PV_CTRL"


    # match ik control's transform to fk joint + ev. locators

    if limbType == "arm":
        cmds.matchTransform(ikControl, fkJointList[2])
    else:
        cmds.matchTransform(ikControl, fkJointList[2].replace("FK_JNT", "LOC"))

    cmds.matchTransform(pvControl, fkJointList[1].replace("FK_JNT", "PV_LOC"))

    cmds.select(clear=True)


createUI(matchFKtoIK, matchIKtoFK)