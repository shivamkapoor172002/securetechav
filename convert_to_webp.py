import os
from PIL import Image

def convert_to_webp(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                name, _ = os.path.splitext(file_path)
                webp_path = f"{name}.webp"
                
                # Check if it's already there or if we should skip
                if not os.path.exists(webp_path):
                    try:
                        with Image.open(file_path) as img:
                            # Using high quality (95) to ensure no noticeable loss
                            img.save(webp_path, "WEBP", quality=95, method=6)
                        print(f"Converted: {file_path} -> {webp_path}")
                    except Exception as e:
                        print(f"Failed to convert {file_path}: {e}")

if __name__ == "__main__":
    static_dir = os.path.join("secure", "static")
    convert_to_webp(static_dir)
