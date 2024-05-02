import maya.cmds as cmds

def createFingerControls(prefix, num_joints):
    finger_controls = []
    for i in range(num_joints):
        control_name = '{}_Finger{}_Ctrl'.format(prefix, i+1)
        control = cmds.circle(name=control_name, normal=[1, 0, 0])[0]
        cmds.scale(0.5, 0.5, 0.5, control)
        cmds.makeIdentity(control, apply=True, t=1, r=1, s=1, n=0)
        finger_controls.append(control)
        
        if i > 0:
            cmds.parent(control, finger_controls[i-1])
        
    return finger_controls

def createFingerControlsUI():
    if cmds.window('fingerControlsWindow', exists=True):
        cmds.deleteUI('fingerControlsWindow', window=True)
        
    cmds.window('fingerControlsWindow', title='Finger Controls', widthHeight=(200, 100))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.text(label='Select finger root joint:')
    cmds.button(label='Create Finger Controls', command=createControlsCallback)
    
    cmds.showWindow('fingerControlsWindow')

def createControlsCallback(*args):
    selection = cmds.ls(selection=True, dag=True, type='joint')
    
    if not selection:
        cmds.warning('Please select a finger root joint.')
        return
    
    finger_root_joint = selection[0]
    finger_name = finger_root_joint.split('_')[0]
    num_joints = cmds.getAttr(finger_root_joint + '.numChildren')
    
    finger_controls = createFingerControls(finger_name, num_joints)
    
    for i, joint in enumerate(cmds.listRelatives(finger_root_joint, allDescendents=True, type='joint')):
        cmds.parentConstraint(finger_controls[i], joint, maintainOffset=True)
        
createFingerControlsUI()