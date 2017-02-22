"""
wing @ rig
"""

import maya.cmds as mc


from ..base import module
from ..base import control

from ..utils import joint
from ..utils import name


def build(wingJoints, featherJoints, side, prefix = 'bWing', side = 'C', rigScale = 1.00, baseRig = None):
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