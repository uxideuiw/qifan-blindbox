import os
from PIL import Image

input_folder = "images"
output_folder = "images_webp"

MAX_WIDTH = 500
QUALITY = 65  # WebP 质量

for root, dirs, files in os.walk(input_folder):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(root, file)
            rel_path = os.path.relpath(root, input_folder)
            out_dir = os.path.join(output_folder, rel_path)
            os.makedirs(out_dir, exist_ok=True)
            out_name = os.path.splitext(file)[0] + ".webp"
            output_path = os.path.join(out_dir, out_name)

            with Image.open(input_path) as img:
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                img.save(output_path, 'WEBP', quality=QUALITY, optimize=True)
                print(f"压缩: {input_path} -> {output_path} ({os.path.getsize(output_path)//1024}KB)")

print("完成！替换 images 文件夹即可。")