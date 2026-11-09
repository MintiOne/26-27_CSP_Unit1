from PIL import Image
import os

# Ensure the directory exists
tiles_dir = "tiles"
if os.path.exists(tiles_dir):
    # 1. Filter only for PNG files to avoid system/hidden files
    png_files = [f for f in os.listdir(tiles_dir) if f.lower().endswith('.png')]

    for img_file in png_files:
        input_path = os.path.join(tiles_dir, img_file)

        # 2. Create the new output path with a .gif extension
        base_name = os.path.splitext(img_file)[0]
        output_path = os.path.join(tiles_dir, f"{base_name}.gif")

        try:
            with Image.open(input_path) as im:
                # 3. Convert to RGB/P mode if needed (GIF doesn't support full RGBA transparency well)
                if im.mode in ('RGBA', 'LA'):
                    im = im.convert('P', palette=Image.ADAPTIVE)
                im.save(output_path, "GIF")

            # Optional: Delete the original PNG if you want a true replacement
            # os.remove(input_path)

        except Exception as e:
            print(f"Could not convert {img_file}: {e}")

from pathlib import Path

# Specify the directory and target extension
directory_path = Path("tiles/")
file_extension = "*.png"  # Change to your target type (e.g., "*.jpg", "*.log")

# Find and delete matching files
for file_path in directory_path.glob(file_extension):
    try:
        if file_path.is_file():
            file_path.unlink()
            print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
