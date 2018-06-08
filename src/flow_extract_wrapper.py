import os
import sys
import shutil

image_dir = sys.argv[1]
output_dir = sys.argv[2]
os.makedirs(output_dir, exist_ok=True)

first = True
for date_dir in sorted(os.listdir(image_dir)):
    flow_dir = os.path.join(output_dir, date_dir)
    os.makedirs(flow_dir, exist_ok=True)

    date_dir = os.path.join(image_dir, date_dir)

    # Copy last image from previous day
    if not first:
        copied_path = os.path.join(date_dir, last_img_name)
        print("Copying %s to %s..." % (last_img_path, copied_path))
        shutil.copyfile(last_img_path, copied_path)

    # First one does not have optical flow
    img_names = sorted(os.listdir(date_dir))[1:]

    cmd = "./extract_warp_gpu" + \
          " -f=%s" % date_dir + \
          " -x=%s/flow_x" % flow_dir + \
          " -y=%s/flow_y" % flow_dir + \
          " -i=%s/image" % flow_dir + \
          " -b=20" + " -t=1" + " -d=0" + " -s=1" + " -o=dir"
    print(cmd)
    os.system(cmd)

    cnt = 0
    for path in sorted(os.listdir(flow_dir)):
        if not path.startswith("flow_x"):
            continue
        name, ext = os.path.splitext(img_names[cnt])

        from_path = os.path.join(flow_dir, path)
        to_path = os.path.join(flow_dir, "%s_x%s" % (name, ext))
        os.rename(from_path, to_path)

        from_path = from_path.replace("flow_x", "flow_y")
        to_path = os.path.join(flow_dir, "%s_y%s" % (name, ext))
        os.rename(from_path, to_path)

        cnt += 1

    last_img_name = img_names[-1] 
    last_img_path = os.path.join(date_dir, last_img_name)

    if first:
        first = False
    else:
        os.remove(copied_path)
        print("Removing %s..." % copied_path)
