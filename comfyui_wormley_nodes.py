# Good Luck


import json
import re
import os
import comfy.sd
from nodes import *
from folder_paths import *
import random

if __name__ == os.path.splitext(os.path.basename(__file__))[0] :
    from ConsoleColor import print, console, ccolor
    from mypath import *
else:
    from .ConsoleColor import print, console, ccolor
    from .mypath import *




class CheckpointVAELoaderSimpleText:
    @classmethod
    def INPUT_TYPES(s):
        t_checkpoints=folder_paths.get_filename_list("checkpoints")
        t_vae=folder_paths.get_filename_list("vae")
        #print(f"checkpoints count : {len(t_checkpoints)}", Colors.BGREEN)
        return {
            "required": { 
                "ckpt_name": (
                    "STRING", {
                        "multiline": False, 
                        "default": random.choice(t_checkpoints)
                    }
                ),
             },
            "optional": { 
                "vae_name": (
                    "STRING", {
                        "multiline": False, 
                        "default": ""
                    }
                ),
             },
         }
    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_checkpoint_vae"

    CATEGORY = "loaders"
# If vae_name is provided, or incoming text has |vaename... then use that,

    def load_checkpoint_vae(self, ckpt_name, vae_name=None, output_vae=True, output_clip=True):
        if (vae_name is None or vae_name == "" ):
            m = re.search(r'^(.*)\|(.*)$',ckpt_name)
            if (m):
                ckpt_name = m.group(1)
                vae_name = m.group(2)
        
        print(f"[{ccolor}]ckpt_name : [/{ccolor}]", ckpt_name)
        ckpt_path=folder_paths.get_full_path("checkpoints", ckpt_name)
        if ckpt_path is None:
            ckpt_path=getFullPath(ckpt_name,"checkpoints")
        print(f"[{ccolor}]ckpt_path : [/{ccolor}]", ckpt_path)
        if (vae_name is not None):
            print(f"[{ccolor}]vae_name : [/{ccolor}]", vae_name)
            vae_path=getFullPath(vae_name,"vae")
        try:
            output_vae = True
            vae = None
            if (vae_name is not None):
                sd = comfy.utils.load_torch_file(vae_path)
                vae = comfy.sd.VAE(sd=sd)
                output_vae = False
            out = comfy.sd.load_checkpoint_guess_config(ckpt_path, output_vae=output_vae, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))
            return (out[0],out[1],out[2] if vae is None else vae)
        except Exception as e:
            console.print_exception()
            return 


# Text output checkpoint and vae selector
class CheckpointVAESelectorText:

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": { "ckpt_name": (folder_paths.get_filename_list("checkpoints"),),
                              "vae_name": (["Baked VAE"] + folder_paths.get_filename_list("vae"),),
                              "appendvae": ("BOOLEAN",{"default":False })
                }
        }

    RETURN_TYPES = ("STRING","STRING")
    RETURN_NAMES = ("CHECKPOINT_NAME" , "VAE_NAME" )
    FUNCTION = "checkpoint_vae_selector"
    CATEGORY = "utils"
    def checkpoint_vae_selector(self, ckpt_name,vae_name,appendvae):
        vae_out = ""
        if (vae_name is not None and vae_name != "None" and vae_name != "Baked VAE"):
            if (appendvae):
                ckpt_name += "|"+vae_name
            vae_out = vae_name

        return(ckpt_name,vae_name)

class LoRA_Tag_To_Stack:
    def __init__(self):
        self.tag_pattern = "\<[0-9a-zA-Z\:\_\-\.\s\/\(\)]+\>"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "text": ("STRING", {"multiline": True}),
                              },
                "optional": {"lora_stack": ("LORA_STACK",)
                },
}
    RETURN_TYPES = ("LORA_STACK", "STRING")
    RETURN_NAMES = ("LORA_STACK", "PROMPT")
    FUNCTION = "load_lora_tags_stack"

    CATEGORY = "utils"

    def load_lora_tags_stack(self, text, lora_stack=None):
        # print(f"\nLoraTagLoader input text: { text }")
        lora_list=list()
        if lora_stack is not None:
            lora_list.extend([l for l in lora_stack if l[0] != "None"])


        founds = re.findall(self.tag_pattern, text)
        print(f"\nfoound lora tags: { founds }")

        if len(founds) < 1:
            return (lora_list,text)
        
        lora_files = folder_paths.get_filename_list("loras")
        for f in founds:
            tag = f[1:-1]
            pak = tag.split(":")
            (type,name,wModel) = pak[:3]
            wClip = wModel
            if len(pak)>3:
                wClip = pak[3]
            if type != 'lora':
                continue
            lora_name = None
            for lora_file in lora_files:
                if Path(lora_file).name.startswith(name) or lora_file.startswith(name):
                    lora_name = lora_file
                    break
            if lora_name == None:
                print(f"bypassed lora tag: { (type, name, wModel, wClip) } >> { lora_name }")
                continue
            print(f"detected lora tag: { (type, name, wModel, wClip) } >> { lora_name }")

            lora_path = folder_paths.get_full_path("loras", lora_name)

            strength_model = float(wModel)
            strength_clip = float(wClip)
            lora_list.extend([(lora_name, strength_model, strength_clip)]),

        plain_prompt = re.sub(self.tag_pattern, "", text)
        return (lora_list, plain_prompt)


# Node List
NODE_CLASS_MAPPINGS = {
    "CheckpointVAELoaderSimpleText": CheckpointVAELoaderSimpleText,
    "CheckpointVAESelectorText": CheckpointVAESelectorText,
    "LoRA_Tag_To_Stack": LoRA_Tag_To_Stack,
}

