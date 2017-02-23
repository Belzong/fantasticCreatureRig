"""
komodo rig setup
deform part

"""



import os
import maya.cmds as mc
import maya.mel as mel
from rigLib.utils import name
from . import project
from rigTools import bSkinSaver

skinWeightDir = 'weights/skinCluster'
swExt = '.swt'

bodyGeo = 'body_geo'
bodyMidResGeo = 'body_midres_geo'


def build(baseRig, characterName, ):
    
    # make twist joint 
    parentJoints = ['l_elbow1_jnt', 'r_elbow1_jnt', 'l_knee1_jnt', 'r_knee1_jnt']
    makeTwistJoint(baseRig, parentJoints)

    # load skin weight
    modelGrp = '%s_model_grp' % characterName
  
    geoList = _getModelGeoObject(modelGrp)

    loadSkinWeights(characterName, geoList)
    
    # apply delta mush deformer
    _applyDeltaMushDeformer(bodyMidResGeo)
    
    # wrap hires body mesh
    _applyWrapDeformer([bodyGeo], bodyMidResGeo)


def _getModelGeoObject(modelGrp):   

    geoList = [mc.listRelatives(o, p = True)[0] for o in mc.listRelatives(modelGrp, ad = 1, type = 'mesh')]
    return geoList

def _applyDeltaMushDeformer(geo):
    deltaMushDf = mc.deltaMush(geo, smoothingIterations = 50)[0]

def _applyWrapDeformer(wrappedObjs, wrapperObj):
    mc.select(wrappedObjs,wrapperObj, r = True )
    mel.eval('doWrapArgList "7" {"1","0","1","2","1","1","0","0"}; ')
        
    
def makeTwistJoint(baseRig, parentJoints):
    
    twistJntMainGrp = mc.group(n = 'twistJoints_grp', p = baseRig.skeletonGrp, em = True)
    
    for parentJnt in parentJoints:
        prefix = name.removeSuffix(parentJnt)
        prefix = prefix[:-1]
        parentJntChild = mc.listRelatives(parentJnt, c = 1, type = 'joint')[0]
        
        # make twist joint
        twistJntGrp = mc.group(n = prefix + 'TwistJoint_grp', p = twistJntMainGrp, em = True)
        
        twistParentJnt = mc.duplicate(parentJnt, n = prefix + 'Twist1_jnt', parentOnly = True)[0]
        twistChildJnt = mc.duplicate(parentJntChild, n = prefix + 'Twist2_jnt', parentOnly = True)[0]
        
        # adjust twist joint
        origJntRadius = mc.getAttr(parentJnt + '.radius')
        
        for j in [twistParentJnt, twistChildJnt]:
            mc.setAttr('%s.radius' % j, origJntRadius * 2)
            mc.color(j, ud = 1)
            
        mc.parent(twistChildJnt, twistParentJnt)
        mc.parent(twistParentJnt, twistJntGrp)
        
        # attach twist joints
        mc.pointConstraint(parentJnt, twistParentJnt, mo = False)
        
        # ik handle 
        twistIk = mc.ikHandle(n='%sTwistJoint_ikhl' % prefix, solver = 'ikSCsolver', sj = twistParentJnt, ee = twistChildJnt)[0]
        mc.hide(twistIk)
        mc.parent(twistIk,twistJntGrp)
        mc.parentConstraint(parentJntChild,twistIk, mo = True)
        
def saveSkinWeights(characterName, geoList = []):
    """
    
    save weights for character geometry object
    
    """
    
    for obj in geoList:
        # weight file
        wtFile = os.path.join(project.mainProjectPath, characterName, skinWeightDir, obj + swExt )
        # save skin weight file
        mc.select(obj)
        bSkinSaver.bSaveSkinValues(wtFile)

def loadSkinWeights(characterName, geoList = []):
    """
    
    load weight for character geometry object
    
    """       
    # weight folder:
    wtDir= os.path.join(project.mainProjectPath, characterName, skinWeightDir)
    # permet de checker les fichiers se trouvant dans le directory
    wtFiles = os.listdir(wtDir)

    # load skin weight    
    for file in wtFiles:
        extRes = os.path.splitext(file)
        baseName = os.path.basename(file)
        


        # check extension format
        if not extRes > 1:
            continue

        # check skin weight file
        if not extRes[1] == swExt:
            continue
        
        # check gemoetry list
        if geoList and not extRes[0]in geoList:
            continue
        # check if object exists
        if not mc.objExists(extRes[0]):
            continue
        
        fullpathWtFile = os.path.join(wtDir, file)
        bSkinSaver.bLoadSkinValues(loadOnSelection = False, inputFile = fullpathWtFile)
        
        
        
        
        