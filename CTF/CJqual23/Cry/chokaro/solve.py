import numpy as np
from PIL import Image

a = Image.open("mixed.png")
print(len(np.array(a)[0]))