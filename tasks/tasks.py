from celery import Celery
from tempfile import TemporaryDirectory
from config import Config
import ffmpeg
import math
from os import path


app = Celery('tasks', broker=Config.REDIS_URL, backend=Config.REDIS_URL)


@app.task
def split_file(
    output_dir: str,
    filepath: str,
    max_size: int,
    title: str,
):
    """
    Разбивает аудиофайл на части по заданному максимальному размеру.

    Parameters:
    - output_dir (str): Путь к директории, куда будут сохранены аудиочасти.
    - filepath (str): Полный путь к исходному аудиофайлу.
    - max_size (int): Максимальный допустимый размер одной части в байтах.
    - title (str): Название файла.

    Returns:
        list[str] : Список путей к созданным частям аудиофайла.
    """

    file_size = path.getsize(filepath)
    probe = ffmpeg.probe(filepath)
    duration = float(probe["format"]["duration"])
    num_parts = math.ceil(file_size / max_size)
    part_duration = duration / num_parts

    list_of_files = []
    for i in range(num_parts):
        start = i * part_duration
        end = start + part_duration
        if end > duration:
            end = duration

        output_file_path = path.join(output_dir, f"{i}_{title}")
        ffmpeg.input(filepath, ss=start, t=part_duration).output(
            output_file_path, acodec="copy"
        ).run(quiet=True, overwrite_output=True)

        list_of_files.append(output_file_path)
    return list_of_files
