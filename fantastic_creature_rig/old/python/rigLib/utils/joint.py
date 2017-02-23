"""

joint utils @utils

"""

import maya.cmds as mc


def listHierarchy(topJnt, withEndJnt = True):
    
    """
    list joint hierarchy starting with the top joint
    
    @param topJnt: str, name of the joint to select
    @param withEndJnt: bool, list hierarchy including end joints
    
    @return: list(str), listed joints starting with top joint
    """
    
    listJnt = mc.listRelatives(topJnt, type ='joint', ad = True)
    listJnt.append(topJnt)
    listJnt.reverse()
    
    completeHierarchy = listJnt[:]
    
    if not withEndJnt:
        completeHierarchy = [ jnt for jnt in listJnt if mc.listRelatives(jnt, child = True, type = 'joint')]
        
    return completeHierarchy
    
    
def matchPosAndRot(objList, objSource):
    """
    match the obj position and rotation to the objSource
    
    @param objList: list(str), list object to transform and rotate
    @param objSource: str, master object for set transform and rotation
    @return: None
    """
    
    if len(objList)!=0:
        for obj in objList:
            mc.delete(mc.parentConstraint(obj, objSource, mo = False))


