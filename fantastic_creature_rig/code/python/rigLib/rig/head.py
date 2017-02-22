"""


"""

import maya.cmds as mc

from ..base import module
from ..base import control


def build(headJoint, jawJoint, muzzleJoints, leftEyeJoint, rightEyeJoint, prefix = 'head', side = 'C', rigScale = 1.00, baseRig = None):
    
    
    """
    @param headJoint: str, name of head joint
    @param jawJoint: str, name of jaw joint
    @param muzzleJoints: list(str), list with 2 muzzle joints chain
    @param leftEyeJoint: str, name of left eye joint
    @param rightEyeJoint: str, name of right eye joint
    @param prefix: str, name of the head part
    @param rigScale: scale factor rig
    @param baseRig: instance of base.module.Base class
    @return dictionary with rig module objects
    
    """
    
    # make module rig
    rigModule = module.Module(side = side, prefix = prefix, rigScale = rigScale, baseRig = baseRig)