bl_info = {
    "name": "Armature_to_shapekeys",
    "author": "Maik Arnold",
    "category": "Animation",
    "blender": (3, 0, 0),
    "version": (1, 1),
    "support": "TESTING",
    "location": "Object > Animation > Apply Armature to Shapekeys",
    "warning": "Bei Fehlermeldungen und Frust, wenden Sie sich bitte an Ihren Arzt oder Apotheker. Alternativ an Maik, der hat das Script geschrieben",
    "wiki_url": "",
}

import bpy, bpy.ops, bpy.props, bpy.types, bpy.utils, bgl, blf, mathutils, math
from mathutils import *

class VIEW3D_PT_polipolArmatureTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Polipol'
    bl_label = 'Armature to Shapekeys'
    
    def draw(self, context):
        sc = context.scene
        layout = self.layout
        row = layout.row(align=False)
        
        
        self.layout.operator('object.toshapekeys', 
        text='Armature to Shapekeys', icon='OUTLINER_OB_ARMATURE')

   
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class ArmatureToShapekeys(bpy.types.Operator):
    """Origin für Export setzen"""
    bl_idname = "object.toshapekeys"
    bl_label = "Polipol Armature Macro"
    bl_options = {'REGISTER', 'UNDO'}
    
    
    count_maxframes: bpy.props.IntProperty(
            name="End_Frame",
            description="Amount of frames for the deformation animation",
            default=100
            )
            
    count_keys: bpy.props.IntProperty(
        name="Keys",
        description="Amount of frames for the deformation animation",
        soft_min=1,
        soft_max=100,
        default=5
        )
    
    def execute(self, context):
        
        print(test)
        
        obj = bpy.context.object
        #Checks if an Armature modifier exists
        modifierExists = bool(bpy.context.object.modifiers.items())
        #Checks if the Armature modifier has an Object
        modArmObjectExists = bool(obj.modifiers["Armature"].object)
        #Converts Armature modifier object to string
        modArmObject = obj.modifiers["Armature"].object
        #Checks if ShapeKeys exists
        shapeKeysExist = bool(bpy.context.object.data.shape_keys)
        print("modifierExists: " + str(modifierExists) + "\n" + "modArmObjectExists: " + str(modArmObjectExists) + "\n" + "modArmObject: " + str(modArmObject) + "\n" + "shapeKeysExist: " + str(shapeKeysExist))
        
        
        
        keys = self.count_keys
        maxframes = self.count_maxframes
        
        if(modifierExists == True and modArmObjectExists == True):
            
            S = bpy.context.scene
            O = bpy.context.object
            
            S.frame_end = maxframes
            frameInterval = round(maxframes/keys)
            cframe = S.frame_current
            
            O.active_shape_key_index = 0
            if(shapeKeysExist == True):
                bpy.ops.object.shape_key_remove(all=True)
                print("shape keys geloescht")
            
            #Zum Frame springen
            S.frame_set(1)
            print("zum ersten Frame gesprungen")
            bpy.data.objects[obj.name].modifiers["Armature"].show_viewport = True
            bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier="Armature", report=True)
            bpy.data.shape_keys["Key"].key_blocks["Armature"].mute = True
            bpy.ops.object.modifier_add(type="ARMATURE")
            bpy.data.objects[obj.name].modifiers["Armature"].object = modArmObject
            
            index = O.data.shape_keys.key_blocks
            print(index.keys())
            print("starting ShapeKey Loop" + "\n" )
            
            if(index.find("Armature") != 0):
                x = 0
                prior = S.frame_current
                print("Armature ShapeKey found")
                bpy.data.scenes['Scene'].frame_current = 1
                
                while(cframe<=maxframes) or  (x<=keys): 
                    x=x+1
                    print("cFrame is in Range")
                    
                    index["Armature"].name = str(cframe)
                    O.active_shape_key_index = index.find(str(cframe))
                    
                    print("next ShapeKey initiated " + str(cframe))
                    
                    if(O.active_shape_key_index == "1"):
                        index[str(cframe)].value = 1
                        index[str(cframe)].keyframe_insert(data_path="value")
                    else:
                        if(prior != cframe):
                            O.active_shape_key_index = index.find(str(prior))
                            index[str(prior)].value = 0
                            index[str(prior)].keyframe_insert(data_path="value")
                            print("shape key " + str(prior) + " wurde auf " + str(index[str(prior)].value) +  " gesetzt")
                        
                        O.active_shape_key_index = index.find(str(cframe))
                        index[str(cframe)].value = 1
                        index[str(cframe)].keyframe_insert(data_path="value")
                        print("shape key " + str(prior) + " wurde auf " + str(index[str(cframe)].value) +  " gesetzt")
                        
                        
                    prior = S.frame_current
                    print("Interval: " +str(frameInterval) + " --- " + str(x))
                    
                    cframe = (x*frameInterval)
                    S.frame_current = cframe
                    print(str(cframe))
                    
                    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=False, modifier="Armature", report=True)
                    bpy.data.shape_keys["Key"].key_blocks["Armature"].mute = True
                    bpy.ops.object.modifier_add(type="ARMATURE")
                    bpy.data.objects[obj.name].modifiers["Armature"].object = modArmObject
                    O.active_shape_key_index = index.find("Arma ture")
                    S.frame_current = prior
                    index["Armature"].value = 0
                    index["Armature"].keyframe_insert(data_path="value")
                    #index["Armature"].interpolation_type(type='LINEAR')
                    S.frame_current = cframe
                        
                    print("end of while-loop" + "\n")
                    print("--------------------------------------" + "\n")
                
            
            O.active_shape_key_index = index.find("Armature")
            index["Armature"].keyframe_delete(data_path="value")
            bpy.ops.object.shape_key_remove(all=False)
            
            
            bpy.data.objects[obj.name].modifiers["Armature"].show_viewport = False
            S.frame_set(1)
            
            print("Shape Keys gesetzt")
            
                
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Modifier inkompatibel")
            
            return {'FINISHED'}

def register():
    bpy.utils.register_class(VIEW3D_PT_polipolArmatureTools)
    bpy.utils.register_class(ArmatureToShapekeys)
    

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_polipolArmatureTools)
    bpy.utils.unregister_class(ArmatureToShapekeys)
    
if __name__ == "__main__":
    register()