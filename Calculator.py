from .. import loader, utils
import re

@loader.tds
class CalculatorMod(loader.Module):
    """Калькулятор для Hikka Userbot"""
    strings = {"name": "Calculator"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command()
    async def calc(self, message):
        """<выражение> - Вычислить математическое выражение"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>❌ Введите выражение для вычисления</b>")
            return
        
        # Безопасная проверка выражения
        if not re.match(r'^[\d+\-*/(). ]+$', args):
            await message.edit("<b>❌ Недопустимые символы в выражении</b>")
            return

        try:
            result = eval(args)
            await message.edit(f"<b>🔢 Результат:</b> <code>{result}</code>")
        except ZeroDivisionError:
            await message.edit("<b>❌ Ошибка: Деление на ноль</b>")
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка:</b> <code>{str(e)}</code>")

async def register(client):
    return CalculatorMod(client)
