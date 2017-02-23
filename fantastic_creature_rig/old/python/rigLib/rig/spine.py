"""
spine 
"""

import maya.cmds as mc

from ..base import control
from ..base import module


def build(spineJoints,
          rootJoint,
          spineCurve,
          bodyLocator,
          chestLocator,
          pelvisLocator,
          prefix = 'spine',
          rigScale = 1.00,
          side = 'C',
          baseRig = None
        ):
    
    """
    @param spineJoints: list (str), list of spine joints
    @param rootJoint: str, root joint
    @param spineCurve: str, name of spine cubic curve with 5 CVs matching first 5 spine joints
    @param bodyLocator: str, reference transform for body control
    @param chestLocator: str, reference transform for chest control
    @param pelvis: str, reference transform for pelvis control
    @param prefix: str, prefix to name new objects
    @param rigScale: float, scale factor for size of controls
    @param baseRig: instance of base.module.Base class
    @return: dictionary with rig module objects
    """
    # make rig module
    
    rigModule = module.Module(name = prefix, side=side, baseObj = baseRig)
    
    # make spine curve clusters
    spineCurvesCVs = mc.ls('%s.cv[*]' % spineCurve, fl = True)
    nbCls = len(spineCurvesCVs)
    spineCurveCls = []
    
    for i in range(nbCls):
        cls = mc.cluster(spineCurvesCVs[i], n = '%s_cluster%d' % (prefix,i+1))[1]
        spineCurveCls.append(cls)
        
    mc.hide(spineCurveCls)
    
    # parent neck Curve

    mc.parent(spineCurve, rigModule.partsNoTransGrp)
    
    # make controls
    bodyCtrl =  control.Control(side ='C', name ='%sBody' % prefix, translateTo= bodyLocator, radius =rigScale * 3, normal= [1, 0, 0], parent = rigModule.controlGrp)
    pelvisCtrl = control.Control(side ='C', name ='%sPelvis' % prefix, translateTo= pelvisLocator, radius =rigScale * 5, normal= [0, 0, 1], parent = bodyCtrl.ctrl)
    chestCtrl = control.Control(side ='C', name ='%sChest' % prefix, translateTo= chestLocator, radius =rigScale * 6, normal= [0, 0, 1], parent = bodyCtrl.ctrl)
    midCtrl = control.Control(side ='C', name ='%sMiddle' % prefix, translateTo= spineCurveCls[2], radius =rigScale * 4, normal= [0, 0, 1], parent = bodyCtrl.ctrl)
    
    _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale)
    
    # attach controls
    mc.parentConstraint(chestCtrl.ctrl, pelvisCtrl.ctrl, midCtrl.ctrlOff, sr = ['x','y','z'], mo = True)
    
    # attach clusters
    mc.parent(spineCurveCls[3:], chestCtrl.ctrl)
    mc.parent(spineCurveCls[2], midCtrl.ctrl)
    mc.parent(spineCurveCls[:2], pelvisCtrl.ctrl)
    
    # attach chest joint
    mc.orientConstraint(chestCtrl.ctrl, spineJoints[-2], mo = True)
    
    # make ik handle
    spineIk = mc.ikHandle(n = '%s_ikhl' % prefix, sol = 'ikSplineSolver', sj = spineJoints[0], ee = spineJoints[-2], c = spineCurve, ccv = 0, parentCurve = False)[0]
    
    mc.hide(spineIk)
    mc.parent(spineIk, rigModule.partsNoTransGrp)

    # make twist for ik handle
    mc.setAttr('%s.dTwistControlEnable' % spineIk, True)
    mc.setAttr('%s.dWorldUpType' % spineIk, 4)
    mc.connectAttr('%s.worldMatrix[0]' % pelvisCtrl.ctrl, '%s.dWorldUpMatrix' % spineIk )
    mc.connectAttr('%s.worldMatrix[0]' % chestCtrl.ctrl, '%s.dWorldUpMatrixEnd' % spineIk )

    # attach root joint
    mc.parentConstraint(pelvisCtrl.ctrl, rootJoint, mo = True)
    
    return {'module':rigModule, 'bodyCtrl':bodyCtrl}


def _adjustBodyCtrlShape(bodyCtrl, spineJoints, rigScale):
    """
    offset body control along spine Y axis
    """
    
    offsetGrp = mc.group(em = True, p = bodyCtrl.ctrl)
    mc.parent(offsetGrp, spineJoints[2])
    ctrlCls = mc.cluster(mc.listRelatives(bodyCtrl.ctrl, s = True))[1]
    mc.parent(ctrlCls, offsetGrp)
    mc.move(10 * rigScale, offsetGrp, moveY = True, relative = True, objectSpace = True)
    mc.delete(bodyCtrl.ctrl, ch = True)
    
    
