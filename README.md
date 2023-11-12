These probably don't work.

Stolen from:

https://github.com/lilly1987/ComfyUI_node_Lilly

Inspired by others.

CheckpointVAELoaderSimpleText: Adds another text entry for the checkpoint loader to choose a VAE, if input is blank or "None" then uses the Baked VAE. Also, if the checkpoint text has  checkpoint.safetensors|vae.safetensors then it will load the VAE after the |

CheckpointVAESelectorText: Allows choosing a checkpoint and optionally a VAE in a friendly format. "appendvae" makes the output CHECKPOINT_NAME include the VAE at the end following a "|" symbol. Compatible with the above node. Can make it easier if there's a switch.

I use these with a text switch to select between a list of random Checkpoints and to select a specific one. But some need a non-baked VAE.

