import numpy as np
import os
import nibabel as nib
from nibabel.testing import data_path

# List files
files_list = sorted(os.listdir("/mnt/disk3/datasets_rm/data_set_skull"))
for i in range(len(files_list)):
    files_list[i] = "/mnt/disk3/datasets_rm/data_set_skull/" + files_list[i]

# Load
loaded_files = list(map(nib.load, files_list))

# Get max width and height
shapes_width = []
shapes_height = []
for lf in loaded_files:
    shapes_width.append(lf.shape[0])
    shapes_height.append(lf.shape[1])

max_width = max(shapes_width)
max_height = max(shapes_height)

for i in range(50):
    exam = loaded_files[i].get_data()
    exam = np.rollaxis(exam, 2) #put frames at index 0
    new_exam = np.zeros((0, max_width, max_height), dtype=np.int16)
    for cut in exam:
        new_cut = np.zeros((0,max_height), dtype=np.int16)
        for line in cut:
            new_line = np.resize(line, (max_height,))
            new_cut = np.append(new_cut, [new_line], axis=0)
        for i in range(max_width - exam.shape[1]):
            new_cut = np.append(new_cut, [np.zeros((max_height,), dtype=np.int16)], axis=0)
        new_exam = np.append(new_exam, [new_cut], axis=0)

    new_exam = np.rollaxis(new_exam,0,3)

    img = nib.Nifti1Image(new_exam, np.eye(4))
    #Get file name without the file extension in order to add _norm to the end of the name
    new_file_name = files_list[i].split("/")[-1].split(".")[0]
    img.to_filename(os.path.join("",new_file_name + "_norm.nii.gz"))

