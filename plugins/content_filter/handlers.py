from aiogram.types import Message


async def filter_message(
    plugin,
    message: Message,
) -> None:

    if not message.text:
        return

    text = message.text.lower()

    for word in plugin.filtered_words:

        if word.lower() in text:

            try:
                await message.delete()

            except Exception as exc:

                print(
                    f"[content_filter] "
                    f"Failed to delete message: {exc}"
                )

            return