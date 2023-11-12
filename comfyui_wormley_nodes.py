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
    CATEGORY = "Loaders"
    def checkpoint_vae_selector(self, ckpt_name,vae_name,appendvae):
        vae_out = ""
        if (vae_name is not None and vae_name != "None" and vae_name != "Baked VAE"):
            if (appendvae):
                ckpt_name += "|"+vae_name
            vae_out = vae_name

        return(ckpt_name,vae_name)



# Node List
NODE_CLASS_MAPPINGS = {
    "CheckpointVAELoaderSimpleText": CheckpointVAELoaderSimpleText,
    "CheckpointVAESelectorText": CheckpointVAESelectorText,
}

