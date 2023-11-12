These probably don't work.

Stolen from:

https://github.com/lilly1987/ComfyUI_node_Lilly

Inspired by others.

__CheckpointVAELoaderSimpleText__: Adds another text entry for the checkpoint loader to choose a VAE, if input is blank or "None" then uses the Baked VAE. Also, if the checkpoint text has  checkpoint.safetensors|vae.safetensors then it will load the VAE after the |

__CheckpointVAESelectorText__: Allows choosing a checkpoint and optionally a VAE in a friendly format. "appendvae" enabled makes the output CHECKPOINT_NAME include the VAE at the end following a "|" symbol. Compatible with the above node. Can make it easier if there's a switch.

I use these with a text switch to select between a list of random Checkpoints and to select a specific one. But some need a non-baked VAE.

The selector makes it easier to choose one than cut and paste the name.


__LoRA_Tag_To_Stack__: Converts embedded lora tags in prompt to LORA_STACK for use with Comfyroll's stack.

Stack code stolen from: https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes

Tag code stolen from: https://github.com/badjeff/comfyui_lora_tag_loader

