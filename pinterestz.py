from telethon.tl.types import Message

from .. import loader, utils

@loader.tds
class PinterestDLMod(loader.Module):
    """Download videos from Pinterest"""

    strings = {
        "name": "PinterestDL",
        "args": "🚫 <b>URL not specified</b>",
        "loading": "🔍 <b>Loading...</b>",
        "404": "🚫 <b>Video not found</b>",
    }

    strings_ru = {
        "args": "🚫 <b>URL не указан</b>",
        "loading": "🔍 <b>Загрузка...</b>",
        "404": "🚫 <b>Видео не найдено</b>",
    }

    async def client_ready(self, *_):
        # Use the correct GitHub raw file URL and branch/tag name
        github_raw_url = "https://raw.githubusercontent.com/zolotarevinc/pinterest/main/pinterestz.py"

        self.pinterestz = await self.import_lib(
            github_raw_url,
            suspend_on_error=True,
        )

    @loader.command(ru_doc="<url> - Download video from Pinterest")
    async def pdl(self, message: Message):
        """<url> - Download video from Pinterest"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["args"])
            return

        message = await utils.answer(message, self.strings["loading"])
        video_url = await self.pinterestz.get_video_url(args)

        if not video_url:
            await utils.answer(message, self.strings["404"])
            return

        await self._client.send_file(
            message.peer_id,
            video_url,
            caption=f"🎥 {utils.ascii_face()}",
            reply_to=getattr(message, "reply_to_msg_id", None),
        )
        if message.out:
            await message.delete()