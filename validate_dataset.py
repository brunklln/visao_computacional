import os
import glob

def validate_yolo_dataset(dataset_path):
    splits = ['train', 'valid', 'test']
    issues = []
    total_images = 0
    total_labels = 0
    total_bboxes = 0
    total_polygons = 0
    
    for split in splits:
        images_dir = os.path.join(dataset_path, split, 'images')
        labels_dir = os.path.join(dataset_path, split, 'labels')
        
        if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
            issues.append(f"Missing images or labels directory in split: {split}")
            continue
            
        images = glob.glob(os.path.join(images_dir, '*.*'))
        labels = glob.glob(os.path.join(labels_dir, '*.txt'))
        
        image_basenames = {os.path.splitext(os.path.basename(img))[0] for img in images}
        label_basenames = {os.path.splitext(os.path.basename(lbl))[0] for lbl in labels}
        
        total_images += len(images)
        total_labels += len(labels)
        
        # Check for images without labels
        missing_labels = image_basenames - label_basenames
        for name in missing_labels:
            issues.append(f"[{split}] Image without label: {name}")
            
        # Check for labels without images
        missing_images = label_basenames - image_basenames
        for name in missing_images:
            issues.append(f"[{split}] Label without image: {name}")
            
        # Validate label contents
        for label_path in labels:
            with open(label_path, 'r') as f:
                lines = f.readlines()
                
            for line_idx, line in enumerate(lines):
                parts = line.strip().split()
                if not parts:
                    continue # Empty line
                    
                if len(parts) < 5:
                    issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): expected at least 5 values, got {len(parts)}")
                    continue
                    
                try:
                    class_id = int(parts[0])
                    coords = list(map(float, parts[1:]))
                    
                    if class_id != 0:
                        issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): Invalid class ID {class_id}. Expected 0.")
                        
                    if len(parts) == 5:
                        total_bboxes += 1
                        x_center, y_center, width, height = coords
                        if not (0.0 <= x_center <= 1.0) or not (0.0 <= y_center <= 1.0):
                            issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): Center out of bounds: x={x_center}, y={y_center}")
                        if not (0.0 <= width <= 1.0) or not (0.0 <= height <= 1.0):
                            issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): W/H out of bounds: w={width}, h={height}")
                    else:
                        if len(coords) % 2 != 0:
                            issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): Polygon has odd number of coordinates ({len(coords)})")
                        else:
                            total_polygons += 1
                            for i in range(0, len(coords), 2):
                                x, y = coords[i], coords[i+1]
                                if not (0.0 <= x <= 1.0) or not (0.0 <= y <= 1.0):
                                    issues.append(f"[{split}] {os.path.basename(label_path)} (line {line_idx+1}): Polygon coordinate out of bounds: x={x}, y={y}")
                        
                except ValueError:
                    issues.append(f"[{split}] Non-numeric values in {os.path.basename(label_path)} (line {line_idx+1})")

    print(f"Dataset Validation Report:")
    print(f"Total Images Checked: {total_images}")
    print(f"Total Labels Checked: {total_labels}")
    print(f"Total Bounding Boxes: {total_bboxes}")
    print(f"Total Polygons/OBBs:  {total_polygons}")
    print("-" * 30)
    
    if not issues:
        print("No issues found! The dataset format and annotations are valid.")
    else:
        print(f"Found {len(issues)} issues:")
        for issue in issues[:50]: # Print up to 50 issues
            print(issue)
        if len(issues) > 50:
            print(f"... and {len(issues) - 50} more issues.")

if __name__ == '__main__':
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(
        BASE_DIR,
        'Larva Aedes Aegypti.v4i.yolov8'
    )
    validate_yolo_dataset(dataset_path)
