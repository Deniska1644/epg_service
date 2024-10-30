from PIL import Image
import os
from pathlib import Path
import aiofiles
import datetime
import asyncio

from schemas.auth_schemas import UserRegistration


class ImageWorcker:
    def __init__(self):
        self.image_watermak_name = 'watermark.png'
        self.workdir = Path(
            __file__).resolve().parent
        self.file_watermark_path = self.workdir / self.image_watermak_name
        self.image_size_h = 400
        self.image_size_w = 300

    async def save_image(self, user_data: UserRegistration):
        format_image = user_data.file.filename.split('.')[-1]
        cur_date = datetime.datetime.now().strftime("%H-%M-%S")
        file_name = user_data.login + '_' + str(cur_date) + '.' + format_image
        file_path = self.chek_dir() / file_name

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await user_data.file.read()
            await out_file.write(content)
            return file_path

    async def delete_image(self):
        raise NotImplementedError

    @staticmethod
    def chek_dir():
        upload_puth = Path.cwd() / '..'/'uploads'
        cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
        path_today_dir = upload_puth / str(cur_date)
        try:
            if os.path.exists(upload_puth):
                if os.path.exists(path_today_dir):
                    return path_today_dir
                os.makedirs(path_today_dir, exist_ok=True)
                return path_today_dir
            os.makedirs(upload_puth, exist_ok=True)
            os.makedirs(path_today_dir, exist_ok=True)
            return path_today_dir
        except Exception as e:
            print(f'exeption from chek_dir: {e}')


class ImageHandler(ImageWorcker):
    def watermark_image(self, main_image_file_path: str):
        try:
            print(main_image_file_path)
            print(self.file_watermark_path)
            base_image = Image.open(main_image_file_path).convert("RGBA")
            whater_mark = Image.open(self.file_watermark_path).convert("RGBA")
            watermark = whater_mark.resize(
                (base_image.width, base_image.height), Image.LANCZOS)

            watermark = self.set_opacity(watermark, 70)
            transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
            transparent.paste(base_image, (0, 0))
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            transparent.paste(watermark, (0, 0), mask=watermark.split()[3])
            transparent.save(main_image_file_path, format='PNG')
            return main_image_file_path
        except Exception as e:
            print(f'Exception in watermark_image: {e}')

    def set_opacity(self, image, opacity):
        """Изменяет прозрачность изображения."""
        assert 0 <= opacity <= 255, "Opacity must be between 0 and 255"
        alpha = image.split()[3]
        alpha = alpha.point(lambda p: p * (opacity / 255.0)
                            )
        image.putalpha(alpha)
        return image


image_worker = ImageHandler()
