"""
leg@rig
"""

import maya.cmds as mc

from ..base import control
from ..base import module
from ..utils import joint


def build(legJoints, topToeJoints, pvLocator, scapulaJoint = '', prefix = 'leg', side = 'C', rigScale = 1.00, baseRig = None):
    """
    @param legJoints: list(str), shoulder / elbow / toe / toe end
    @param topToeJoints: list(str), top metacarpal toe joints
    @param pvLocator: str, reference locator for position of pole vector control
    @param scapulaJoint: str, optional, scapula joint, parent of top leg joint
    @param side: L / R / C by default on C
    @param prefix: str, prefix to name new objects
    @param rigScale: float, scale factor for size controls
    @param baseRig: instance of base.module.Base class
    @return dictionary with rig module objects
    """
    # make rig Module
    rigModule = module.Module(name = prefix, side = side, baseObj = baseRig)
    
    # make attach group
    bodyAttachGrp = mc.group(n = prefix + 'BodyAttach_grp',p = rigModule.partsGrp ,em = True)
    baseAttachGrp = mc.group(n = prefix + 'BaseAttach_grp',p = rigModule.partsGrp ,em = True)
    # make controls
    if scapulaJoint:
        scapulaCtrl = control.Control(name ='%sScapula' % prefix, side = side, translateTo = scapulaJoint, rotateTo = scapulaJoint, radius =rigScale * 3, parent = rigModule.controlGrp, shape ='sphere', lockChannels = ['ty', 'rx', 'rz', 's', 'v'])
        
    footCtrl = control.Control(name ='%sFoot' % prefix, side = side, translateTo = legJoints[2], radius =rigScale * 3, parent = rigModule.controlGrp, shape ='sphere')
    
    ballCtrl = control.Control(name ='%sBall' % prefix, side = side, translateTo = legJoints[3], rotateTo = legJoints[3], radius =rigScale * 2, parent = footCtrl.ctrl, shape ='sphere', normal = [0, 0, 1])
    
    poleVectorCtrl = control.Control(name ='%sPV' % prefix, side = side, translateTo = pvLocator, radius = rigScale, parent = rigModule.controlGrp, shape ='sphere')
        
    toeIkControls = []
    
    for topToeJnt in topToeJoints:
        topPrefix = topToeJnt.split('_')[1]
        sideToe = topToeJnt.split('_')[0]
        toeEndJnt = mc.listRelatives(topToeJnt, ad = True, type = 'joint')[0]
        toeIkCtrl = control.Control(name = topPrefix, side = sideToe, translateTo= toeEndJnt, scale = rigScale, parent = footCtrl.ctrl, shape ='circle', normal = [0, 1, 0])
        toeIkControls.append(toeIkCtrl)
        
        
    # make ik handle
    if scapulaJoint:
        scapulaIk = mc.ikHandle(n = side + '_' + prefix + 'Scapula_ikhl', sol = 'ikSCsolver', sj = scapulaJoint, ee = legJoints[0])[0]
        
    legIk= mc.ikHandle(n = side + '_' + prefix + 'Main_ikhl', sol ='ikRPsolver', sj = legJoints[0], ee = legJoints[2])[0]
    ballIk= mc.ikHandle(n = side + '_' + prefix + 'Ball_ikhl', sol = 'ikSCsolver', sj = legJoints[2], ee = legJoints[3])[0]
    mainToeIk= mc.ikHandle(n = side + '_' + prefix + 'MainToe_ikhl', sol = 'ikSCsolver', sj = legJoints[3], ee = legJoints[4])[0]   
    mc.hide(legIk, ballIk, mainToeIk)
        
    for i, topToeJoint in enumerate(topToeJoints):
        toePrefix = topToeJoint.split('_')[1]
        side = topToeJoint.split('_')[0]
        toeJoints = joint.listHierarchy(topToeJoint)
        
        toeIk = mc.ikHandle(n = '%s_%s_ikhl' % (side, toePrefix), sol = 'ikSCsolver', sj = toeJoints[1], ee= toeJoints[-1])[0]
        mc.hide(toeIk)
        mc.parent(toeIk, toeIkControls[i].ctrl)
        
    # attach controls 
    mc.parentConstraint(bodyAttachGrp, poleVectorCtrl.ctrlOff, mo = True)

    if scapulaJoint:
        mc.parentConstraint(baseAttachGrp, scapulaCtrl.ctrlOff, mo = True)
        
    # attach objects to Controls 
    mc.parent(legIk, ballCtrl.ctrl)
    mc.parent(ballIk, mainToeIk, footCtrl.ctrl)
    mc.poleVectorConstraint(poleVectorCtrl.ctrl, legIk)
    
    if scapulaJoint:
        mc.parent(scapulaIk, scapulaCtrl.ctrl)
        mc.pointConstraint(scapulaCtrl.ctrl, scapulaJoint)
        
    # make pole vector connection line
    pvLinePos1 = mc.xform(legJoints[1], q = True, t = True, ws = True  )
    pvLinePos2 = mc.xform(pvLocator, q = True, t = True, ws = True  ) 
    poleVectorCrv = mc.curve(n = '%s_%sPV_crv' % (side, prefix), d = True, p = [pvLinePos1, pvLinePos2])
    mc.cluster(poleVectorCrv + '.cv[0]', n = side + '_' + prefix + 'Pv1_cls',wn = [legJoints[1], legJoints[1]], bs = True)
    mc.cluster(poleVectorCrv + '.cv[1]', n = side + '_' + prefix + 'Pv2_cls',wn = [poleVectorCtrl.ctrl, poleVectorCtrl.ctrl], bs = True)
    mc.parent(poleVectorCrv, rigModule.controlGrp)
    mc.setAttr(poleVectorCrv + '.template', 1)
    
    return {'module':rigModule, 'baseAttachGrp':baseAttachGrp, 'bodyAttachGrp':bodyAttachGrp}
    