import cv2
import numpy as np
import os
from scipy import misc

ksize = 25
arrow_weight = 2
tipLength = 0.3

flow_dir = "."
sat_dir = "2016-05-29"
out_dir = "arrowed_image"

def calc_point(w_start, w_end, h_start, h_end, x, y, amp_ratio=1):
    w = w_end - w_start
    h = h_end - h_start
    w_center = w_start + int(w / 2)
    h_center = h_start + int(h / 2)

    x_ratio = x / 127.
    y_ratio = y / 127.
    w_span = int(w * x_ratio) * amp_ratio
    h_span = int(h * y_ratio) * amp_ratio

    pt1_x = w_center - int(w_span / 2)
    pt2_x = w_center + int(w_span / 2)

    pt1_y = h_center - int(h_span / 2)
    pt2_y = h_center + int(h_span / 2)
    return (pt1_x, pt1_y), (pt2_x, pt2_y)

if __name__ == '__main__':
    os.makedirs(out_dir, exist_ok=True)

    # First satellite image does not have optical flow
    img_idx = 1
    img_path = [os.path.join(sat_dir, path) for path in sorted(os.listdir(sat_dir))]
    
    for path in sorted(os.listdir(flow_dir)):
        if not path.startswith("flow_x"):
            continue
    
        path = os.path.join(flow_dir, path)
    
        flow_x = misc.imread(path)
        flow_x = flow_x.astype(np.float32) - 128.
    
        flow_y_path = path.replace("x", "y")
        flow_y = misc.imread(flow_y_path)
        flow_y = flow_y.astype(np.float32) - 128.
    
        print("Draawing arrows on %s..." % img_path[img_idx])
        img = misc.imread(img_path[img_idx])
        if len(img.shape) == 3:
            img = np.dot(img[:, ..., :].astype(np.float32), np.asarray([.2126, .7152, .0722]))
            img = img.astype(np.uint8)

        out_path = os.path.join(out_dir, os.path.basename(img_path[img_idx]))
        img_idx += 1
    
        h, w = flow_x.shape
        n_hregion = int(h / ksize)
        n_wregion = int(w / ksize)
    
        for h_idx in range(n_hregion):
            for w_idx in range(n_wregion):
                w_start = ksize * w_idx
                w_end = w_start + ksize
    
                h_start = ksize * h_idx
                h_end = h_start + ksize
    
                mean_x = np.mean(flow_x[h_start:h_end, w_start:w_end])
                mean_y = np.mean(flow_y[h_start:h_end, w_start:w_end])
                #print("(h, w) = (%d, %d), (y, x) = (%d, %d)" % (h_start, w_start, mean_y, mean_x))
    
                pt1, pt2 = calc_point(w_start, w_end, h_start, h_end, mean_x, mean_y)
                cv2.arrowedLine(img, pt1, pt2, (255,0,0), arrow_weight, tipLength=tipLength)

        misc.imsave(out_path, img)
