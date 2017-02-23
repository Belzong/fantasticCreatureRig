"""


name @ utils


"""


def removeSuffix(name):
    """
    remove suffix from given name string
    
    @param name: give name string to process
    
    @return: str, name without suffix
    """
    
    edits = name.split('_')
    
    
    if len(edits)<2:
        return name
    
    suffix = '_' + edits[-1]
    nameNoSuffix = name[:-len(suffix)]
    
    return nameNoSuffix

def addSuffix(objList, suffix):
    """
    add suffix to given object
    
    @param objList: list(str), list of object to add suffix
    @param suffix: suffix to add for each object
    
    @return: new object list with suffix added
    """
    newObjList = []
    if len(objList)>0:
        for obj in objList:
            newObj = mc.rename(obj, '%s_%s' % (obj, suffix))
            newObjList.append(newObj)
            
    return newObjList
    
def removePrefix(name):
    """
    remove prefix from given name string
    
    @param name: give name string to process
    
    @return: str, name without prefix
    """
    
    edits = name.split('_')
    
    if len(edits)<2:
        return name
    
    prefix = edits[1:]
    nameNoPrefix = ''
    for i in range(len(prefix)):
        if i == 0:
            nameNoPrefix = prefix[0]
        else:
            nameNoPrefix = nameNoPrefix + '_' + prefix[i]

    return nameNoPrefix

def addPrefix(objList, prefix):
    """
    add suffix to given object
    
    @param objList: list(str), list of object to add prefix
    @param suffix: prefix to add for each object
    
    @return: None
    """
    newObjList = []
    if len(objList)>0:
        for obj in objList:
            newObj = mc.rename(obj, '%s_%s' % (prefix, obj))
            newObjList.append(newObj)
            
    return newObjList
    