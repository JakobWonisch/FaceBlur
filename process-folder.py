
import argparse

from detect import detect
import os


def detect_folder(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and allowed_extension(f)]

    counter = 0
    for f in files:
        print(f"[{counter}/{len(files)}] Processing: {f}")
        counter += 1

        setup_opts(path, f)

        try:
            detect(opt)
        except:
            print(f"skipping image {f}")

def allowed_extension(file):
    extensions = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']
    
    for e in extensions:
        if file.endswith(e):
            return True
        
    return False

def setup_opts(path, file):
    global opt
    opt = argparse.Namespace(weights=['models/pts/yolov7-tiny.pt'], source=os.path.join(path, file), img_size=640, conf_thres=0.1, iou_thres=0.45, device='cpu', view_img=False, save_txt=False, save_conf=False, nosave=False, classes=None, agnostic_nms=False, augment=False, update=False, project=path, name='output', exist_ok=True, no_trace=False, blurratio=25, hidedetarea=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='.', help='path of folder to process')
    args = parser.parse_args()

    detect_folder(args.path)