from .. import loader, utils
import re

@loader.tds
class CalculatorMod(loader.Module):
    """Калькулятор для Hikka"""
    strings = {"name": "Calculator"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command()
    async def calc(self, message):
        """<выражение> - Вычислить пример"""
        args = utils.get_args_raw(message)
        
        if not args:
            await message.edit("❌ Введите выражение (например: <code>.calc 2+2</code>)")
            return

        # Безопасная проверка ввода
        if not re.match(r'^[\d+\-*/(). ]+$', args):
            await message.edit("❌ Недопустимые символы в выражении!")
            return

        try:
            result = eval(args)
            await message.edit(f"🔢 Результат: <code>{result}</code>")
        except ZeroDivisionError:
            await message.edit("❌ Ошибка: Деление на ноль")
        except Exception as e:
            await message.edit(f"❌ Ошибка: {str(e)}")

async def register(client):
    return CalculatorMod(client)     
