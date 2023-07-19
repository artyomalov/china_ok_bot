__all__ = ['convert_id_to_url_service']

from aiogram import Bot
from config_reader import config


async def convert_id_to_url_service(
    bot: Bot,
    file_id: str
):
    '''
    supporting function needed to convert photo to url that will be
    send to google sheets
    '''
    file_data = await bot.get_file(str(file_id))
    file_url = f'=IMAGE("https://api.telegram.org/file/bot{config.bot_token.get_secret_value()}/{file_data.file_path}")'
    file_paths = {
        'file_id': file_id,
        'file_url': file_url,
    }
    return file_paths
