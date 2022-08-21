import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
import os
import math
import csv


### Add-on INFO

bl_info={
    "name": "OpenFace FACS Data to Bones",
    "author": "Andras Csefalvay",
    "description": "Can apply OpenFace FACS Data to Bones from a .csv file that OpenFace exports",
    "version": (1,2,8,),
    "location": "View3D>FACS>OpenFace FACS Data to Bones",
    "category": "FACS",
    "support": "COMMUNITY",
    "blender": (2,91,1)
}

dir= 0
actionUnitNumber = 20
FirstAU = 0

class MYADDON_PT_my_panel (bpy.types.Panel):
    bl_label ="CSV2FACS READING ADDON"
    bl_idname = "MYADDON_PT_my_panel"
    bl_space_type ="VIEW_3D"
    bl_region_type = "UI"
    bl_category = "FACS "



    def draw(self,context):
        scene=context.object
        layout= self.layout

        row = layout.row()
        row.label(text="OpenFace FACS Data to Bones")

        row1 = layout.row()
        row1.operator("test.open_filebrowser")

        row2 = layout.row()
        row2.operator("myaddon.my_operator")


        row3 = layout.row()
        row3.operator("function.my_operator")

        row4 = layout.row()
        row4.operator("function.my_head")

        row5 = layout.row()
        row5.operator("function.my_driver")



###################################################    button creates FACS controllers

class MYADDON_OT_my_operator(bpy.types.Operator):
    bl_idname = "myaddon.my_operator"
    bl_label = "Create FACS_Controller"

    def execute(self, context):
        #theCODE

        #conflict checks
        global dir
        #print(dir)

        if not dir:
            print("No file selected!")
            return {'FINISHED'}
        else:
            print (dir)

            if bpy.data.objects.get("FACS_Controller") is not None:
                print("FACS Controller present already present, delete the previous one")
            else:



                ###################################################
                ## set number of Action Units, from file (name of AU from first ROW) or set manually
                actionunits = ["AU01", "AU02", "AU03", "AU04", "AU05"]
                longlist = ['Frame', 'MouthOpen', 'MouthWide','MouthPucker', 'JawOpen',
                    'MouthCorner_Left', 'MouthCorner_Right', 'UpperLipRaiser',
                    'LowerLipRaiser', 'LipPresser', 'EyeBlink', 'InnerBrowRaiser',
                    'OuterBrowRaiser', 'BrowLowerer', 'EyeHoriz', 'EyeVert']

                ## access CSV
                #dir= "C:/Users/Andras/Desktop/tester.csv"


                ## read first row
                with open(dir) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    column_list = next(csv_reader)

                print ("Columnlist:" , column_list)
                #print ("The original list is : " + str(column_list))
                #subs = '_r'
                actionunits = longlist
                #actionunits = [o for o in column_list if subs in o]
                #print ("All strings with given substring are : " + str(actionunits))

                ### get number of AU
                actionUnitNumber = len(actionunits)
                #print (actionUnitNumber)
                print ("ActionUnit number: " , actionUnitNumber )

                indices = [i for i, s in enumerate(column_list) if 'MouthOpen' in s]
                #FirstAU = indices[0]
                FirstAU = 1


                ## create bones that correspond to the AUs
                bpy.ops.object.armature_add(enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
                sel = bpy.context.active_object
                for sel in bpy.context.selected_objects:
                    sel.name = "FACS_Controller"

                ########for created armature delete all (initiaL) bones
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.data.objects["FACS_Controller"].select_set(True)
                sel = bpy.context.active_object
                if sel.type == 'ARMATURE':
                 armature = sel.data

                for bone in armature.edit_bones:
                    armature.edit_bones.remove(bone)

                ###  bones named according to AU row number

                x_coord = 0

                while x_coord <= actionUnitNumber-1:
                    bpy.data.objects["FACS_Controller"].select_set(True)
                    sel = bpy.context.active_object #get the armature object
                    boney_edit = sel.data.edit_bones
                    boney = boney_edit.new(actionunits[x_coord])
                    boney.head = (x_coord/5, 0, 0) # if the head and tail are the same, the bone is deleted
                    boney.tail = (x_coord/5, 0, 1)
                    x_coord += 1

                ### all parented to a root
                sel = bpy.context.active_object
                bpy.ops.object.mode_set(mode='EDIT')
                RootBone = armature.edit_bones['Frame']
                RootBone.name = "FaceRoot"
                RootBone.head = (0, 0, 0)
                RootBone.tail = (0, -1, 0)

                i = 1
                while  i <= actionUnitNumber-1:
                    armature.edit_bones[actionunits[i]].parent= armature.edit_bones['FaceRoot']
                    i += 1

                bpy.ops.object.mode_set(mode='OBJECT')



                print("ok, ok, ok, the FACS controls are created")
            return {'FINISHED'}

###################################################  button opens csv
class OT_TestOpenFilebrowser(Operator, ImportHelper):
    bl_idname = "test.open_filebrowser"
    bl_label = "Open FACS Data .csv file"

    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)

        #print('Selected file:', self.filepath)
        #print('File name:', filename)
        #print('File extension:', extension)
        global dir
        dir = self.filepath
        if extension != ".csv":
            print ("You have to pick a correct .csv file")
            dir = ''
        else:
            print('Selected file:', self.filepath)
        #Do something with the selected file(s).
        return {'FINISHED'}

###################################################  button to apply data

class FUNCTION_OT_my_operator(bpy.types.Operator):
    bl_idname = "function.my_operator"
    bl_label = "Apply FACS Data"

    def execute(self, context):




        #conflict checks
        if bpy.data.objects.get("FACS_Controller") is None:
            print("No FACS Controller present")
        else:

            #bpy.ops.object.select_all(action='DESELECT')
            #bpy.ops.object.select_pattern(pattern="FACS_Controller")
            #deselect all
            bpy.context.active_object.select_set(False)
            bpy.ops.object.select_all(action='DESELECT')

            bpy.data.objects["FACS_Controller"].select_set(True)

            #theCODE
            longlist = ['Frame', 'MouthOpen', 'MouthWide','MouthPucker', 'JawOpen',
                'MouthCorner_Left', 'MouthCorner_Right', 'UpperLipRaiser',
                'LowerLipRaiser', 'LipPresser', 'EyeBlink', 'InnerBrowRaiser',
                'OuterBrowRaiser', 'BrowLowerer', 'EyeHoriz', 'EyeVert']

            actionunits= longlist
            actionUnitNumber = len(longlist)
            #print ("actionunit number:" + str(max))

            k = 1
            while (k < actionUnitNumber):
                with open( dir ) as csvfile:
                    csv_reader = csv.reader( csvfile )
                    for i, row in enumerate( csv_reader ):
                        if i == 0: continue # Skip column titles
                        frame_number = row[0]
                        frame_number_float = float (frame_number)
                        index = k
                        #print (index)
                        movement = float(row [index])

                        #bpy.ops.object.select_all(action='DESELECT')
                        #bpy.ops.object.select_pattern(pattern="FACS_Controller")

                        sel = bpy.data.objects["FACS_Controller"]


                        #make Selected object Active
                        bpy.context.active_object.select_set(False)
                        for obj in bpy.context.selected_objects:
                            bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.mode_set(mode='POSE')


                        pbone = sel.pose.bones.get(actionunits[k])
                        pbone.location = (0, movement , 0)
                        bpy.ops.object.mode_set(mode='OBJECT')
                        #insert a keyframe
                        pbone.keyframe_insert("location" ,frame=frame_number_float)
                k += 1

            print("Mocap data applied!")
        return {'FINISHED'}

###################################################  button import a collection with basehead
class FUNCTION_OT_my_head(bpy.types.Operator):
    bl_idname = "function.my_head"
    bl_label = "Import Basehead"

    def execute(self, context):

        import addon_utils

        for mod in addon_utils.modules():
            if mod.bl_info['name'] == "OpenFace FACS Data to Bones":
                filepath = mod.__file__
                #filefolder = bpy.path.abspath(filepath)
                #print (filepath)

                filepath_split = os.path.split(filepath)   #list with [path, name]
                #print (filepath_split[0])


            else:
                pass



        #conflict checks
        if bpy.data.objects.get("BaseHead") is not None:
            print("Head is already present")
        else:

            #file_path = 'C:/Users/Andras/github/FaceLogger/base.blend'
            file_path = filepath_split[0] + '/base.blend'
            inner_path = 'Collection'
            object_name = 'Collection'

            bpy.ops.wm.append(
                filepath=os.path.join(file_path, inner_path, object_name),
                directory=os.path.join(file_path, inner_path),
                filename=object_name
                )

            head = bpy.data.objects["BaseHead"]
            head.location[0]= -2
            head.location[2]= 2
            head.scale= (10,10,10)


            print("Basehead imported!")
        return {'FINISHED'}

###################################################  button connects drivers
class FUNCTION_OT_my_drivers(bpy.types.Operator):
    bl_idname = "function.my_driver"
    bl_label = "Connect Drivers"



    def execute(self, context):

        #conflict checks
        if bpy.data.objects.get("FACS_Controller") is None:
            print("No FACS Controller present")
        else:
            if bpy.data.objects.get("BaseHead") is None:
                print("Import a Basehead to connect drivers")
            else:



                longlist = ['MouthOpen', 'MouthWide', 'MouthWide','MouthPucker','MouthOpen','JawOpen',
                    'MouthCorner_Left', 'MouthCorner_Right', 'MouthCorner_Left', 'MouthCorner_Right','UpperLipRaiser', 'UpperLipRaiser',
                    'LowerLipRaiser', 'LipPresser', 'LipPresser', 'EyeBlink', 'EyeBlink','InnerBrowRaiser',
                    'OuterBrowRaiser','OuterBrowRaiser', 'BrowLowerer', 'BrowLowerer']

                antelist = ['mouthClose', 'mouthDimpleLeft' ,'mouthDimpleRight', 'mouthPucker', 'mouthFunnel','jawOpen',
                    'mouthStretchLeft', 'mouthStretchRight', 'mouthSmileLeft', 'mouthSmileRight','mouthUpperUpLeft', 'mouthUpperUpRight',
                    'mouthRollLower', 'mouthPressLeft', 'mouthPressRight','eyeBlinkLeft', 'eyeBlinkRight','browInnerUp',
                    'browOuterUpLeft','browOuterUpRight', 'browDownRight' ,'browDownLeft']

                direction= [-1,1,1,2,-1,-1,
                            1,1,3,3,1,1,
                            1,2,2,1,1,3,
                            3,3,3,3]

                actionunits= longlist
                actionUnitNumber = len(longlist)



                def add_driver(
                    source, target, prop, bonetarget, index = -1, negative = False, func = '', bool = 0):

                    if bool == 0 :
                        source.driver_remove(prop)
                    else: pass
                    ##Add driver to source prop (at index), driven by target dataPath '''
                    if index != -1:
                        d = source.driver_add( prop, index ).driver
                    else:
                        d = source.driver_add( prop ).driver

                    d.type = 'SCRIPTED'
                    v = d.variables.new()
                    v.name                 = 'var'


                    #to where
                    v.type        = 'TRANSFORMS'
                    v.targets[0].id        = target
                    v.targets[0].bone_target = bonetarget
                    v.targets[0].transform_space = 'LOCAL_SPACE'
                    v.targets[0].transform_type = 'LOC_Y'
                    d.expression = func + "(" + v.name + ")" if func else v.name
                    d.expression = d.expression if not negative else "-1 * " + d.expression





                k = 0
                while (k < actionUnitNumber):

                    target = bpy.data.objects["FACS_Controller"]
                    shape_key = bpy.data.objects['BaseHead'].data.shape_keys
                    source = shape_key

                    bonetarget = longlist[k]
                    endtarget = antelist[k]
                    shapetarget = f'key_blocks["{endtarget}"].value'
                    functionshape = f"{direction[k]} * "

                    add_driver( source, target, shapetarget, bonetarget, -1, func = functionshape , bool = 0)
                    k += 1

                Eyelist = ['RightEye', 'LeftEye']
                k = 0
                while (k < 2):
                    target = bpy.data.objects["FACS_Controller"]
                    source = bpy.data.objects[Eyelist [k]]
                    add_driver(source, target, "rotation_euler", "EyeHoriz", 0, func = '-0.3*', bool = 1)
                    print("1")

                    k += 1

                k = 0
                while (k < 2):
                    target = bpy.data.objects["FACS_Controller"]
                    source = bpy.data.objects[Eyelist [k]]
                    add_driver(source, target, "rotation_euler", "EyeVert", 2, func = '-0.3*', bool =  1)
                    print("2")

                    k += 1


                print("Drivers connected!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MYADDON_PT_my_panel)
    bpy.utils.register_class(MYADDON_OT_my_operator)
    bpy.utils.register_class(OT_TestOpenFilebrowser)
    bpy.utils.register_class(FUNCTION_OT_my_operator)
    bpy.utils.register_class(FUNCTION_OT_my_head)
    bpy.utils.register_class(FUNCTION_OT_my_drivers)

def unregister():
    bpy.utils.unregister_class(MYADDON_PT_my_panel)
    bpy.utils.unregister_class(MYADDON_OT_my_operator)
    bpy.utils.unregister_class(OT_TestOpenFilebrowser)
    bpy.utils.unregister_class(FUNCTION_OT_my_operator)
    bpy.utils.register_class(FUNCTION_OT_my_head)
    bpy.utils.unregister_class(FUNCTION_OT_my_drivers)

if __name__ == "__main__":
    register()
