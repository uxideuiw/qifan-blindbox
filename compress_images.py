import os
from PIL import Image

# 原始图片文件夹（你的 images 目录）
input_folder = "images"
# 压缩后输出文件夹（新建，避免覆盖原图）
output_folder = "images_compressed"

# 压缩质量（1-100，推荐 70-80）
QUALITY = 75
# 最大宽度（像素），手机屏幕足够，高度自动等比缩放
MAX_WIDTH = 800


def compress_images():
    # 遍历所有子文件夹和文件
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(root, file)

                # 保持子文件夹结构（如 熟食盲盒/xxx.jpg）
                relative_path = os.path.relpath(root, input_folder)
                output_subdir = os.path.join(output_folder, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                output_path = os.path.join(output_subdir, file)

                try:
                    with Image.open(input_path) as img:
                        # 转换 RGBA 为 RGB（处理 PNG 透明背景）
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')

                        # 等比例缩放宽度
                        if img.width > MAX_WIDTH:
                            ratio = MAX_WIDTH / img.width
                            new_height = int(img.height * ratio)
                            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

                        # 保存为 JPEG（统一格式，体积小）
                        # 注意：如果你的原图需要保留 PNG（如图标），可以按原格式保存，这里统一 JPEG 方便
                        output_path = os.path.splitext(output_path)[0] + '.jpg'
                        img.save(output_path, 'JPEG', quality=QUALITY, optimize=True)
                        print(f"✓ 压缩成功: {input_path} -> {output_path} ({img.width}x{img.height})")
                except Exception as e:
                    print(f"✗ 压缩失败: {input_path} - {e}")

    print("\n全部压缩完成！请检查 images_compressed 文件夹，然后替换原 images 文件夹。")


if __name__ == "__main__":
    compress_images()
