"""
neck construction
"""


import maya.cmds as mc

from ..base import control
from ..base import module


def build(neckJoints,
          headJoint,
          neckCurve,
          prefix = 'neck',
          side = 'C',
          rigScale = 1.00,
          baseRig = None
        ):
    
    """
    @param neckJoints: list (str), list of spine joints
    @param headJoint: str, head joint
    @param neckCurve: str, name of spine cubic curve with 5 CVs matching first 5 spine joints
    @param prefix: str, prefix to name new objects
    @param rigScale: float, scale factor for size of controls
    @param baseRig: instance of base.module.Base class
    @return: dictionary with rig module objects
    """
    # make rig module
    
    rigModule = module.Module(name = prefix, side = side, baseObj = baseRig)
    
    # make curve cluster
    neckCurveCVs = mc.ls('%s.cv[*]' % neckCurve, fl = True)
    numNeck = len(neckCurveCVs)
    neckCurveClusters = []
    
    for i in range(numNeck):
        cls = mc.cluster(neckCurveCVs[i], n = prefix + 'Cluster%d' % (i + 1))[1]
        neckCurveClusters.append(cls)

    mc.hide(neckCurveClusters)
    
    # parent neck Curve
    mc.parent(neckCurve, rigModule.partsNoTransGrp)
    
    # make attach group
    bodyAttachGrp = mc.group(n = prefix + 'BodyAttach_grp',p = rigModule.partsGrp ,em = True)
    baseAttachGrp = mc.group(n = prefix + 'BaseAttach_grp',p = rigModule.partsGrp ,em = True)
    
    mc.delete(mc.pointConstraint(neckJoints[0], baseAttachGrp, mo = False))
    
    # make controls
    headMainCtrl = control.Control(side = 'C', name = '%sHeadMain' % prefix, translateTo= neckJoints[-1], radius = rigScale*5, normal= [0,0,1], parent = rigModule.controlGrp)  
    headLocalCtrl = control.Control(side = 'C', name = '%sHeadLocal' % prefix, translateTo= headJoint, rotateTo = headJoint, radius = rigScale*4, normal= [1,0,0], parent = headMainCtrl.ctrl)
    midCtrl = control.Control(side = 'C', name = '%sMiddle' % prefix, translateTo= neckCurveClusters[2], rotateTo = neckJoints[2], radius = rigScale*4, normal= [1,0,0], parent = rigModule.controlGrp)

    # attach controls
    mc.parentConstraint(headMainCtrl.ctrl, baseAttachGrp, midCtrl.ctrlOff, sr = ['x','y','z'], mo = True)
    mc.orientConstraint(baseAttachGrp, midCtrl.ctrlOff, mo = True)
    mc.parentConstraint(bodyAttachGrp, headMainCtrl.ctrlOff, mo = True)
    
    # attach cluster
    mc.parent(neckCurveClusters[3:], headMainCtrl.ctrl)
    mc.parent(neckCurveClusters[2], midCtrl.ctrl)
    mc.parent(neckCurveClusters[:2], baseAttachGrp)
    
    # attach joints
    mc.orientConstraint(headLocalCtrl.ctrl, headJoint, mo = True)
    
    # make ik handle
    neckIk = mc.ikHandle(n = '%s_ikhl' % prefix, sol = 'ikSplineSolver', sj = neckJoints[0], ee = neckJoints[-1], c = neckCurve, ccv = 0, parentCurve = False)[0]
    mc.hide(neckIk)
    mc.parent(neckIk, rigModule.partsNoTransGrp)
    
    # make twist for ik handle
    mc.setAttr('%s.dTwistControlEnable' % neckIk, True)
    mc.setAttr('%s.dWorldUpType' % neckIk, 4)
   
    mc.connectAttr('%s.worldMatrix[0]' % headMainCtrl.ctrl, '%s.dWorldUpMatrixEnd' % neckIk )
    mc.connectAttr('%s.worldMatrix[0]' % baseAttachGrp, '%s.dWorldUpMatrix' % neckIk )
        
    return {'module':rigModule, 'baseAttachGrp':baseAttachGrp, 'bodyAttachGrp':bodyAttachGrp}
