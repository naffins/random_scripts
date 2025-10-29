import math

import cv2
import numpy as np
from PIL import Image

# Script adapted from https://stackoverflow.com/questions/33311153/python-extracting-and-saving-video-frames
def extract_spc_frames(video_path, frames_list, pixel_bounds, output_path):
    """
Extract listed frames (zero-indexed) from the specified video, crop to specified bounds ([x_min, x_max, y_min, y_max]), and output to output_path.
    """

    img_list = []

    fl = sorted(frames_list)[::-1]

    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()
    count = 0
    while success:
        if len(fl) == 0:
            break
        if count == fl[-1]:
            fl.pop()
            im = image[pixel_bounds[2]:pixel_bounds[3], pixel_bounds[0]:pixel_bounds[1]]
            img_path = "{}/{}.jpg".format(output_path, count)
            cv2.imwrite(img_path, im)
            img_list.append(img_path)    
        success, image = vidcap.read()
        count += 1

    return img_list

def frames_to_pdf(img_list, per_side_w_pad_proportion=0.1, per_side_h_pad_proportion=0.05, width_to_height_ratio=math.sqrt(2), output_path="out.pdf"):
    
    assert len(img_list) > 0
    
    h, w, d = np.array(Image.open(img_list[0])).shape

    per_side_w_pad_size = math.ceil(per_side_w_pad_proportion * w)

    w = w + (2 * per_side_w_pad_size) 

    page_height = math.floor(width_to_height_ratio * w)

    per_side_h_pad_size = math.ceil(page_height * per_side_h_pad_proportion)
    
    count_per_page = (page_height - (2 * per_side_h_pad_size)) // h

    page_count = (len(img_list) // count_per_page) + (1 if len(img_list) % count_per_page else 0)

    pages_list = []

    for p in range(page_count):
        
        img_sublist = img_list[p*count_per_page : (p+1)*count_per_page]
        
        arr_list = [np.array(Image.open(i)) for i in img_sublist]
        page = np.concatenate(arr_list)
        
        if page.shape[0] < page_height:
            offset_arr = np.broadcast_to(np.array([[[255] * d]]).astype(np.uint8), (page_height - page.shape[0], page.shape[1], d))

            page = np.concatenate([page, offset_arr])

        w_pad = np.broadcast_to(np.array([[[255] * d]]).astype(np.uint8), (page.shape[0], per_side_w_pad_size, d))
        page = np.concatenate([w_pad, page, w_pad], axis=1)
        h_pad = np.broadcast_to(np.array([[[255] * d]]).astype(np.uint8), (per_side_h_pad_size, page.shape[1], d))
        page = np.concatenate([h_pad, page, h_pad])
        
        pages_list.append(Image.fromarray(page))
    
    pages_list[0].save(output_path, save_all=True, format="PDF", append_images=pages_list[1:])