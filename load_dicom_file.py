import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread

path = r'D:\HCC_DataSet\manifest-1643035385102\HCC-TACE-Seg\HCC_014\09-22-1998-NA-ABDPEL LIVER PROTOCOL-49588\103.000000-LIVER 3 PHASE AP-40451/1-01.dcm'

dicom_object = dcmread(path)
print(dicom_object)

# plt.imshow(dicom_object.pixel_array, cmap=plt.cm.gray)
# plt.show()
