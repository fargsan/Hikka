# Hikkafrom telethon import events
from telethon.tl.types import Message
import re

class CalculatorModule:
    """Модуль калькулятора для Hikka Userbot"""

    def __init__(self, client):
        self.client = client
        self.name = "Calculator"
        self.version = "1.0"
        self.author = "Your Name"
        self.description = "Простой калькулятор для вычисления выражений"

    async def calculate(self, expr: str) -> float:
        """Вычисляет математическое выражение"""
        try:
            # Убираем все пробелы и проверяем на безопасность
            expr = expr.replace(" ", "")
            if not re.match(r'^[\d+\-*/(). ]+$', expr):
                return "❌ Ошибка: Недопустимые символы"
            
            # Вычисляем выражение
            result = eval(expr)  # Осторожно! В реальном боте лучше использовать safer_eval
            return f"🔢 Результат: {result}"
        except ZeroDivisionError:
            return "❌ Ошибка: Деление на ноль"
        except SyntaxError:
            return "❌ Ошибка: Неправильное выражение"
        except Exception as e:
            return f"❌ Ошибка: {str(e)}"

    async def cmd_calc(self, event: Message):
        """Вычисляет математическое выражение"""
        args = event.raw_text.split(maxsplit=1)
        if len(args) < 2:
            await event.edit("**❌ Используйте:** `.calc <выражение>`\n**Пример:** `.calc 2+2*3`")
            return
        
        expr = args[1]
        result = await self.calculate(expr)
        await event.edit(result)

    async def install(self):
        """Вызывается при установке модуля"""
        await self.client.send_message(
            "me",
            "✅ **Модуль Calculator успешно установлен!**\n"
            "Используйте `.calc <выражение>` для вычислений."
        )

async def setup(client):
    """Установка модуля"""
    module = CalculatorModule(client)
    client.add_event_handler(
        module.cmd_calc,
        events.NewMessage(pattern=r"^\.calc\s+.+")
    )
    await module.install()
    return module
