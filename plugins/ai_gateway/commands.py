from aiogram.types import Message

from . import repository


def register(command_manager, plugin) -> None:

    command_manager.register(
        name="llm_list",
        handler=_bind(_cmd_list_models, plugin),
    )

    command_manager.register(
        name="add_model",
        handler=_bind(_cmd_add_model, plugin),
    )

    command_manager.register(
        name="set_active_model",
        handler=_bind(_cmd_set_active_model, plugin),
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
            "/add_model <label> <base_url> <api_key> <model_id>"
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
            "/add_model <label> <base_url> <api_key> <model_id>"
        )
        return

    _, label, base_url, api_key, model_id = parts

    try:
        await repository.add_model(
            db=plugin.db,
            plugin_id=plugin.plugin_id,
            label=label,
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
        )
    except Exception as exc:
        await message.reply(f"اضافه کردن مدل شکست خورد: {exc}")
        return

    await message.reply(
    f"مدل «{label}» اضافه شد.\n"
    "برای فعال کردن آن از /set_active_model استفاده کنید."
)
    # پیام حاوی api_key رو پاک می‌کنیم که توی تاریخچه‌ی چت نمونه
    try:
        await message.delete()
    except Exception:
        pass

async def _cmd_set_active_model(message: Message, plugin) -> None:

    if not message.text:
        return

    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        await message.reply(
            "فرمت درست:\n"
            "/set_active_model <label>"
        )
        return

    _, label = parts
    label = label.strip()

    success = await repository.set_active_model(
        plugin.db,
        label,
    )

    if not success:
        await message.reply(
            f"مدلی با label «{label}» پیدا نشد."
        )
        return

    await message.reply(
        f"مدل فعال به «{label}» تغییر کرد."
    )