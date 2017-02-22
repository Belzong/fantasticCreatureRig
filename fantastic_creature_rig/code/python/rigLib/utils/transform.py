"""

transform @ utils

functions to manipulate and create transform

"""

import maya.cmds as mc

from . import name

def makeOffsetGrp(object, nameObj = ''):
    """
    make an offset group for given object
    
    @param object: str, transform object to get offset grp
    @param name: name of the new object
    @return: str, name of the new offset grp
    
    """
    if not nameObj:
        nameObj = name.removeSuffix(object)
        
    offsetGrp = mc.group(n = '%s_offset_grp' % nameObj, em = True)
    
    
    objectParents = mc.listRelatives(object, p = True)
    
    if objectParents:
        mc.parent(offsetGrp, objectParents[0])
        
    # match parent    
    mc.delete(mc.parentConstraint(object, offsetGrp), mo = False)
    mc.delete(mc.scaleConstraint(object, offsetGrp), mo = False)
    
    # parent object under offset grp
    mc.parent(object, offsetGrp)
    
    return offsetGrp