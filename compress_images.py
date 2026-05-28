import os
from PIL import Image

input_folder = "images"
output_folder = "images_compressed"

# 更激进的压缩参数
QUALITY = 60  # 之前 75，现在 60
MAX_WIDTH = 500  # 之前 800，现在 500（手机上足够清晰）


def compress_images():
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_subdir = os.path.join(output_folder, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_path = os.path.join(output_subdir, file)

                try:
                    with Image.open(input_path) as img:
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        if img.width > MAX_WIDTH:
                            ratio = MAX_WIDTH / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                        output_path = os.path.splitext(output_path)[0] + '.jpg'
                        img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
                        size_kb = os.path.getsize(output_path) / 1024
                        print(f"✓ {file} -> {size_kb:.1f}KB")
                except Exception as e:
                    print(f"✗ 失败: {file} - {e}")


if __name__ == "__main__":
    compress_images()
    print("完成！请检查 images_compressed 文件夹，替换原 images 文件夹后重新推送。")