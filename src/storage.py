import asyncio
import aiofiles
import os
from pathlib import Path

FILES_PATH = './media/'


def validate_path(path):
    Path(FILES_PATH + path).mkdir(parents=True, exist_ok=True)
    return FILES_PATH + path


def decode_filename(name):
    pass


def encode_filename(name):
    pass
    # class StaticAsyncStorage:
    #     @staticmethod
    #     async def save_file(travel_id, file_name, file_content):
    #         file_path = f'{travel_id}/{file_name}'
    #         async with aiofiles.open(file_path, 'wb') as f:
    #             await f.write(file_content)
    #         return file_path
    #
    #     @staticmethod
    #     def get_path(travel_id, file_name)
    #
    #     @staticmethod
    #     async def read_file(travel_id, file_name):
    #         file_path = f'{travel_id}/{file_name}'
    #         async with aiofiles.open(file_path, 'rb') as f:
    #             file_content = await f.read()
    #         return file_content
    #
    #     @staticmethod
    #     async def list_files(storage_path):
    #         files = os.listdir(storage_path)
    #         return files
