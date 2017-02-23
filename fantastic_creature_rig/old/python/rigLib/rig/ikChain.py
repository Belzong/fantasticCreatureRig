"""
ikChain @ rig

"""

import maya.cmds as mc

from ..base import control
from ..base import module


def build(chainJoints, 
          chainCurve,
          prefix = 'tail',
          side = 'C', 
          rigScale = 1.00, 
          smallestScalePercent = 0.5,
          fkParenting = True,
          baseRig = None
          ):
    
    
    """
    @param chainJoints: list(str), list of chain joints
    @param chainCurve: str, name of chain curve
    @param prefix: str, prefix to name new object
    @param rigScale: float, scale factor for size controls
    @param smallestScalePercent: float, scale of smallest control at the end of chain compared to rigScale
    @param fkParenting: bool, parent of each control to previous one to make FK chain
    @param baseRig: instance of base.module.Base class
    
    @return dictionary with rig module objects
    """
    
    
    # make rig module
    rigModule = module.Module(name = prefix, side = side, baseObj = baseRig)
    
    # make spine curve clusters
    chainCurveCVs = mc.ls('%s.cv[*]' % chainCurve, fl = True)
    nbCls = len(chainCurveCVs)
    chainCurveCls = []
    
    for i in range(nbCls):
        cls = mc.cluster(chainCurveCVs[i], n = '%s_cluster%d' % (prefix,i+1))[1]
        chainCurveCls.append(cls)
        
    mc.hide(chainCurveCls)
    
    # parent neck Curve
    mc.parent(chainCurve, rigModule.partsNoTransGrp)

    # make attach groups
    baseAttachGrp = mc.group(n = prefix + 'BaseAttach_grp', em = True, p = rigModule.partsGrp)
    
    mc.delete(mc.pointConstraint(chainJoints[0], baseAttachGrp))
    
    # make controls 
    chainControls = []
    
    controlScaleIncrement = (1.00- smallestScalePercent)/ nbCls
    mainCtrlScaleFactor = 5.0
    for i in range(nbCls):
        ctrlScale  = rigScale * mainCtrlScaleFactor * (1.0- (i * controlScaleIncrement)) 
        ctrl = control.Control(name='%s%d' % (prefix, (i + 1)), translateTo = chainCurveCls[i], radius = ctrlScale, parent = rigModule.controlGrp, shape ='sphere')
        chainControls.append(ctrl)
        
    # parent control
    if fkParenting:    
        for i in range(nbCls):
            if i == 0:
                continue
            mc.parent(chainControls[i].ctrlOff, chainControls[i-1].ctrl)
            
    # attach clusters
    for i in range(nbCls):
        mc.parent(chainCurveCls[i], chainControls[i].ctrl)
        
    # attach controls 
    mc.parentConstraint(baseAttachGrp, chainControls[0].ctrlOff, mo = True)
    
    # make ik handle
    chainIk = mc.ikHandle(n = '%s_ikhl' % prefix, sol = 'ikSplineSolver', sj = chainJoints[0], ee = chainJoints[-1], c = chainCurve, ccv = 0, parentCurve = False)[0]
    
    mc.hide(chainIk)
    mc.parent(chainIk, rigModule.partsNoTransGrp)

    # add twist attribute
    twistAt = 'twist'
    mc.addAttr(chainControls[-1].ctrl, ln = twistAt, k = True)
    mc.connectAttr(chainControls[-1].ctrl + '.' + twistAt, chainIk + '.twist')
    
    return {'module': rigModule, 'baseAttachGrp': baseAttachGrp}
    