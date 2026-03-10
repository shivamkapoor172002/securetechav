import os
import shutil

base_dir = r"c:\Users\shiva\OneDrive\Desktop\anu_bhai"
dest_img_dir = os.path.join(base_dir, r"secure\static\images\profile")

with open(os.path.join(base_dir, 'images_list.txt'), 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

basenames_needed = set([os.path.basename(u) for u in urls if u.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp'))])

# Find all matching files in base_dir
found = {}
for root, dirs, files in os.walk(base_dir):
    if r"secure\static" in root:
        continue
    for file in files:
        if file in basenames_needed:
            if file not in found:
                found[file] = os.path.join(root, file)

for basename in basenames_needed:
    dest = os.path.join(dest_img_dir, basename)
    if os.path.exists(dest):
        continue  # already copied
    if basename in found:
        try:
            shutil.copy2(found[basename], dest)
            print(f"Copied {basename} from {found[basename]}")
        except Exception as e:
            print(f"Error copying {basename}: {e}")
    else:
        print(f"Still missing: {basename}")
