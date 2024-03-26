import asyncio
from io import BytesIO
from os import getenv, remove
from random import randint

import assemblyai as aai
from translate import Translator

from templates.translate import Templates

aai.settings.api_key = getenv('AAI_TOKEN')


async def translate(voice: BytesIO, lang_from: str, lang_to: str) -> str:
    translator = Translator(to_lang=lang_to, from_lang=lang_from)
    config = aai.TranscriptionConfig(language_code=lang_from)  # noqa #type: ignore
    transcriber = aai.Transcriber()

    filename = f'{randint(1000, 10000)}.wav'
    with open(filename, "wb") as out_f:
        out_f.write(voice.read())

    transcript = await asyncio.to_thread(transcriber.transcribe, data=filename, config=config)
    remove(filename)

    if transcript.status == aai.TranscriptStatus.error:
        return Templates.TRANSLATE_ERROR.value
    else:
        return await asyncio.to_thread(translator.translate, transcript.text)
