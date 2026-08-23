from aiogram.types import Message


async def filter_message(
    plugin,
    message: Message,
) -> bool:

    if not message.text:
        return False
    
    text = message.text.lower()

    for word in plugin.filtered_words:

        if word.lower() in text:

            try:
                await message.delete()
                return True
            
            except Exception as exc:

                print(
                    f"[content_filter] "
                    f"Failed to delete message: {exc}"
                )
                return False
    return False