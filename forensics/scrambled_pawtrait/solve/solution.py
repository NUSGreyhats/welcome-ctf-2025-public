from PIL import Image
import numpy as np

A = np.array(Image.open("pawtrait_a.png").convert("RGB"), dtype=np.uint8)
B = np.array(Image.open("pawtrait_b.png").convert("RGB"), dtype=np.uint8)
Image.fromarray(A ^ B).save("recovered.png")

