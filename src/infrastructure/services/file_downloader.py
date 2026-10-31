from pathlib import Path

from loguru import logger

from .bot_registry import BotRegistry


class AiogramFileDownloader:
    def __init__(self, bots: BotRegistry) -> None:
        self.bots = bots

    async def download_to_path(self, file_id: str, destination: Path) -> None:
        # file_ids are bot-specific; the current bot is the one the file was sent to.
        bot = self.bots.current
        file = await bot.get_file(file_id)
        if not file.file_path:
            raise ValueError(f"File path not found for file_id '{file_id}'")
        await bot.download_file(file.file_path, destination=destination)
        logger.debug(f"Downloaded file '{file_id}' to '{destination}'")
