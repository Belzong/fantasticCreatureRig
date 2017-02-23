"""

komodo dragon rig setup
main module
"""

import maya.cmds as mc
from rigLib.base import module
from rigLib.rig import ikChain
from rigLib.rig import leg
from rigLib.rig import neck
from rigLib.rig import spine
from rigLib.utils import joint

from . import komodo_deform
from . import project

sceneScale = project.sceneScale


# path files
mainProjectPath = project.mainProjectPath
modelFilePath = '%s/%s/model/%s_model.mb'
builderSceneFilePath = '%s/%s/builder/%s_builder.mb'

rootJnt = 'root1_jnt'
headJnt = 'head1_jnt'
pelvisJnt = 'pelvis1_jnt'
jawJnt = 'jaw1_jnt'
 
def build(characterName):
    """
    main function to build character rig
    
    """
    
    # new scene
    mc.file(new = True, force = True)
    
    # import builder scene
    builderFile = builderSceneFilePath % (mainProjectPath, characterName, characterName)
    mc.file(builderFile, i = True)
    
    # make base structure
    baseRig = module.Base(characterName = characterName, sceneSetup = sceneScale, mainCtrlAttachObj = headJnt)
    
    # import model
    modelFile = modelFilePath % (mainProjectPath, characterName, characterName)
    mc.file(modelFile, i = True)
    
    # parent model
    modelGrp = '%s_model_grp' % characterName
    mc.parent(modelGrp, baseRig.modelGrp)
    
    # parent skeleton
    mc.parent(rootJnt, baseRig.skeletonGrp)
    
    # deform setup
    komodo_deform.build(baseRig, characterName)
    

    
    # make controls for the spine
    makeControlSetup(baseRig)
    
def makeControlSetup(baseRig):
    
    # SPINE
    spineJoints = mc.ls('*spine*', type = 'joint')
    spineCurve = mc.ls('*spine*', type = 'nurbsCurve')[0] 
    spineCurve = spineCurve.split('Shape')[0]       
    spineRig = spine.build(spineJoints, rootJnt, spineCurve, bodyLocator = 'body_loc', chestLocator = 'chest_loc', pelvisLocator = 'pelvis_loc', prefix = 'spine', baseRig = baseRig, rigScale = sceneScale)
  
    # NECK
    neckJoints = mc.ls('*neck*', type = 'joint')
    neckCurve = mc.ls('*neck*', type = 'nurbsCurve')[0]
    neckCurve = neckCurve.split('Shape')[0] 
    
    neckRig = neck.build(neckJoints, headJnt, neckCurve, prefix = 'neck', side = 'C', baseRig = baseRig, rigScale = sceneScale)
    
    # attach neck rig to the rest of body
    mc.parentConstraint(spineJoints[-2], neckRig['baseAttachGrp'], mo = True)
    mc.parentConstraint(spineRig['bodyCtrl'].ctrl, neckRig['bodyAttachGrp'], mo = True)
    
    
    # TAIL 
    tailJoints =joint.listHierarchy('tail1_jnt')
    tailCurve = mc.ls('*tail*', type = 'nurbsCurve')[0]
    tailCurve = tailCurve.split('Shape')[0] 
    
    tailRig = ikChain.build(chainJoints = tailJoints, chainCurve = tailCurve,prefix = 'tail', side = 'C', rigScale = sceneScale*0.8, smallestScalePercent = 0.4,fkParenting = False,baseRig = baseRig)

    mc.parentConstraint(pelvisJnt, tailRig['baseAttachGrp'], mo = True)
    
    # TONGUE
    tongueJoints =joint.listHierarchy('tongue1_jnt')
    tongueCurve = mc.ls('*tongue*', type = 'nurbsCurve')[0]
    tongueCurve = tongueCurve.split('Shape')[0] 
    
    tongueRig = ikChain.build(chainJoints = tongueJoints, chainCurve = tongueCurve,prefix = 'tongue', rigScale = sceneScale*0.4, smallestScalePercent = 0.3,fkParenting = True,baseRig = baseRig)

    mc.parentConstraint(jawJnt, tongueRig['baseAttachGrp'], mo = True)
    
    # LEGS
    # Left Arm
    legJoints = ['l_shoulder1_jnt', 'l_elbow1_jnt', 'l_hand1_jnt', 'l_hand2_jnt', 'l_hand3_jnt']
    topToeJoints = ['l_foreToeA1_jnt','l_foreToeB1_jnt','l_foreToeC1_jnt','l_foreToeD1_jnt','l_foreToeE1_jnt']
    lArmRig = leg.build(legJoints = legJoints, topToeJoints = topToeJoints, pvLocator = 'l_arm_pole_vector_loc', scapulaJoint = 'l_scapula1_jnt', prefix = 'Arm', side = 'L', rigScale = sceneScale, baseRig = baseRig)
    
    mc.parentConstraint(spineJoints[-2], lArmRig['baseAttachGrp'], mo = True)
    mc.parentConstraint(spineRig['bodyCtrl'].ctrl, lArmRig['bodyAttachGrp'], mo = True)
    
    
    # Right Arm
    legJoints = ['r_shoulder1_jnt', 'r_elbow1_jnt', 'r_hand1_jnt', 'r_hand2_jnt', 'r_hand3_jnt']
    topToeJoints = ['r_foreToeA1_jnt','r_foreToeB1_jnt','r_foreToeC1_jnt','r_foreToeD1_jnt','r_foreToeE1_jnt']
    rArmRig = leg.build(legJoints = legJoints, topToeJoints = topToeJoints, pvLocator = 'r_arm_pole_vector_loc', scapulaJoint = 'r_scapula1_jnt', prefix = 'Arm', side = 'R', rigScale = sceneScale, baseRig = baseRig)
    
    mc.parentConstraint(spineJoints[-2], rArmRig['baseAttachGrp'], mo = True)
    mc.parentConstraint(spineRig['bodyCtrl'].ctrl, rArmRig['bodyAttachGrp'], mo = True)
    
    # Left Legs
    legJoints = ['l_hip1_jnt','l_knee1_jnt', 'l_foot1_jnt', 'l_foot2_jnt', 'l_foot3_jnt']
    topToeJoints = ['l_hindToeA1_jnt','l_hindToeB1_jnt','l_hindToeC1_jnt','l_hindToeD1_jnt','l_hindToeE1_jnt']
    lLegRig = leg.build(legJoints = legJoints, topToeJoints = topToeJoints, pvLocator = 'l_leg_pole_vector_loc', prefix = 'Leg', side = 'L', rigScale = sceneScale, baseRig = baseRig)
    
    mc.parentConstraint(spineJoints[-2], lLegRig['baseAttachGrp'], mo = True)
    mc.parentConstraint(spineRig['bodyCtrl'].ctrl, lLegRig['bodyAttachGrp'], mo = True)
    
    # Right Legs
    legJoints = ['r_hip1_jnt','r_knee1_jnt', 'r_foot1_jnt', 'r_foot2_jnt', 'r_foot3_jnt']
    topToeJoints = ['r_hindToeA1_jnt','r_hindToeB1_jnt','r_hindToeC1_jnt','r_hindToeD1_jnt','r_hindToeE1_jnt']
    rLegRig = leg.build(legJoints = legJoints, topToeJoints = topToeJoints, pvLocator = 'r_leg_pole_vector_loc', prefix = 'Leg', side = 'R', rigScale = sceneScale, baseRig = baseRig)
    
    mc.parentConstraint(spineJoints[-2], rLegRig['baseAttachGrp'], mo = True)
    mc.parentConstraint(spineRig['bodyCtrl'].ctrl, rLegRig['bodyAttachGrp'], mo = True)
