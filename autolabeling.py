import cv2 
from glob import glob
import os
import timeit
from PIL import Image                                      # (pip install Pillow)
import numpy as np                                         # (pip install numpy)
from skimage import measure                                # (pip install scikit-image)
from shapely.geometry import Polygon, MultiPolygon         # (pip install Shapely)
import json
import torch2trt
import torch

cuda0  = torch.device('cuda:0')
# Label ids of the dataset
category_ids = {
    # "outlier": 0,
    "vein": 1,
    "needle": 2,
}

# Define which colors match which categories in the images
category_colors = {
    # "(0, 0, 0)": 0, # Outlier
    "(255, 0, 0)": 1, # vein
    "(0, 255, 0)": 2, # needle
}

# Define the ids that are a multiplolygon. In our case: wall, roof and sky
multipolygon_ids = [1]


def create_sub_masks(mask_image, width, height):
    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            pixel = mask_image.getpixel((x,y))[:3]
            # Check to see if we have created a sub-mask...
            if pixel == (0,0,0):
                continue
            pixel_str = str(pixel)
            sub_mask = sub_masks.get(pixel_str)
            if sub_mask is None:
               # Create a sub-mask (one bit per pixel) and add to the dictionary
                # Note: we add 1 pixel of padding in each direction
                # because the contours module doesn"t handle cases
                # where pixels bleed to the edge of the image
                sub_masks[pixel_str] = Image.new("1", (width+2, height+2))

            # Set the pixel value to 1 (default is 0), accounting for padding
            sub_masks[pixel_str].putpixel((x+1, y+1), 1)
    print(sub_masks)
    return sub_masks

def create_sub_mask_annotation(sub_mask):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    contours = measure.find_contours(np.array(sub_mask), 0.5, positive_orientation="low")

    polygons = []
    segmentations = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)
        
        if(poly.is_empty):
            # Go to next iteration, dont save empty values in list
            continue

        polygons.append(poly)

        segmentation = np.array(poly.exterior.coords).ravel().tolist()
        segmentations.append(segmentation)
    
    return polygons, segmentations

def create_category_annotation(category_dict):
    category_list = []

    for key, value in category_dict.items():
        category = {
            "supercategory": key,
            "id": value,
            "name": key
        }
        category_list.append(category)

    return category_list

def create_image_annotation(file_name, width, height, image_id):
    images = {
        "file_name": file_name,
        "height": height,
        "width": width,
        "id": image_id
    }

    return images

def create_annotation_format(polygon, segmentation, image_id, category_id, annotation_id):
    min_x, min_y, max_x, max_y = polygon.bounds
    width = max_x - min_x
    height = max_y - min_y
    bbox = (min_x, min_y, width, height)
    area = polygon.area

    annotation = {
        "segmentation": segmentation,
        "area": area,
        "iscrowd": 0,
        "image_id": image_id,
        "bbox": bbox,
        "category_id": category_id,
        "id": annotation_id
    }

    return annotation

def get_coco_json_format():
    # Standard COCO format 
    coco_format = {
        "info": {},
        "licenses": [],
        "images": [{}],
        "categories": [{}],
        "annotations": [{}]
    }

    return coco_format

# Get "images" and "annotations" info 
def images_annotations_info(maskpath):
    # This id will be automatically increased as we go
    annotation_id = 0
    image_id = 0
    annotations = []
    images = []
    
    for mask_image in glob(maskpath + "*.png"):
        # The mask image is *.png but the original image is *.jpg.
        # We make a reference to the original file in the COCO JSON file
        original_file_name = os.path.basename(mask_image).split(".")[0] + ".jpg"

        # Open the image and (to be sure) we convert it to RGB
        mask_image_open = Image.open(mask_image).convert("RGB")
        w, h = mask_image_open.size
        
        # "images" info 
        image = create_image_annotation(original_file_name, w, h, image_id)
        images.append(image)

        sub_masks = create_sub_masks(mask_image_open, w, h)
        for color, sub_mask in sub_masks.items():
            category_id = category_colors[color]

            # "annotations" info
            polygons, segmentations = create_sub_mask_annotation(sub_mask)

            # Check if we have classes that are a multipolygon
            if category_id in multipolygon_ids:
                # Combine the polygons to calculate the bounding box and area
                multi_poly = MultiPolygon(polygons)
                                
                annotation = create_annotation_format(multi_poly, segmentations, image_id, category_id, annotation_id)

                annotations.append(annotation)
                annotation_id += 1
            else:
                for i in range(len(polygons)):
                    # Cleaner to recalculate this variable
                    segmentation = [np.array(polygons[i].exterior.coords).ravel().tolist()]
                    
                    annotation = create_annotation_format(polygons[i], segmentation, image_id, category_id, annotation_id)
                    
                    annotations.append(annotation)
                    annotation_id += 1
        image_id += 1
    return images, annotations, annotation_id



def slice_detect_image(net, cut_frame):
    file_name = ("MOV","mp4")
    img_dir = './images'
    detect_dir = './detect'
    if not os.path.exists(img_dir):
            os.makedirs(img_dir)
    if not os.path.exists(detect_dir):
            os.makedirs(detect_dir)


    files = [fn for fn in glob('*') if os.path.basename(fn).endswith(file_name)]
    count = 0
    for file in files:
        vidcap = cv2.VideoCapture(f'{file}')
        i = 0
        while(vidcap.isOpened()):
            grab = vidcap.grab()
            if i % cut_frame == 0:
                ret, image = vidcap.retrieve()
                if not ret:
                    i = 0
                    break
                image = cv2.resize(image,(960,960))
                input = (torch.from_numpy(image).cuda().flip(2).permute(2,0,1).unsqueeze(0)/255-0.5)*0.5
                output = net(input)
                output = torch.softmax(output,dim=1)
                output = torch.argmax(output,dim=1)
                mask0 = torch.zeros((960,960),device=cuda0,dtype=torch.uint8)
                mask1 = torch.where(output == 1 , mask0+255, 0).squeeze().type(torch.uint8)
                mask2 = torch.where(output == 2 , mask0+255, 0).squeeze().type(torch.uint8)
                mask = torch.stack((mask0,mask2,mask1),dim=2)
                mask = mask.cpu().numpy()
                file = os.path.basename(file).split(".")[0]
                # print('Saved frame number : ' + str(int(i))) 
                cv2.imwrite(f"{img_dir}/{file}_{i:0>3}.jpg", image) 
                cv2.imwrite(f"{detect_dir}/{file}_{i:0>3}.png", mask) 
                # print(f'Saved {file}_{i:0>3}.jpg') 
                count += 1
            i+=1        
    vidcap.release()





if __name__ == "__main__":
    net = torch2trt.TRTModule().cuda()
    net.load_state_dict(torch.load('./model_epoch_best_deelpab_0215top.pth'))
    cut_frame = 600
    slice_detect_image(net= net, cut_frame=cut_frame)

    # Get the standard COCO JSON format
    coco_format = get_coco_json_format()

    
    mask_path = "./detect/"
    
    # Create category section
    coco_format["categories"] = create_category_annotation(category_ids)

    # Create images and annotations sections
    coco_format["images"], coco_format["annotations"], annotation_cnt = images_annotations_info(mask_path)
    json_dir = './annotations'
    if not os.path.exists(json_dir):
            os.makedirs(json_dir)
    with open(f"{json_dir}/instances_Train.json","w") as outfile:
        json.dump(coco_format, outfile)
    
    print("Created %d annotations for images in folder: %s" % (annotation_cnt, mask_path))