from aiogram.types import Message

from . import repository


def register(command_manager, plugin) -> None:

    command_manager.register(
        name="mioo",
        handler=_bind(_cmd_list_models, plugin),
    )

    command_manager.register(
        name="addmodel",
        handler=_bind(_cmd_add_model, plugin),
    )


def _bind(func, plugin):
    async def handler(message: Message) -> None:
        await func(message, plugin)
    return handler


async def _cmd_list_models(message: Message, plugin) -> None:

    models = await repository.list_models(plugin.db)

    if not models:
        await message.reply(
            "هیچ مدلی ثبت نشده.\n"
            "/addmodel <label> <base_url> <api_key> <model_id>"
        )
        return

    lines = [
        f"{'✅' if row['is_active'] else '▫️'} {row['label']} — {row['model_id']}"
        for row in models
    ]
    await message.reply("\n".join(lines))


async def _cmd_add_model(message: Message, plugin) -> None:

    if not message.text:
        return

    parts = message.text.split(maxsplit=4)

    if len(parts) < 5:
        await message.reply(
            "فرمت درست:\n"
            "/addmodel <label> <base_url> <api_key> <model_id>"
        )
        return

    _, label, base_url, api_key, model_id = parts

    try:
        await repository.add_model(
            plugin.db,
            label=label,
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
        )
    except Exception as exc:
        await message.reply(f"اضافه کردن مدل شکست خورد: {exc}")
        return

    await message.reply(f"مدل «{label}» اضافه و فعال شد.")

    # پیام حاوی api_key رو پاک می‌کنیم که توی تاریخچه‌ی چت نمونه
    try:
        await message.delete()
    except Exception:
        pass