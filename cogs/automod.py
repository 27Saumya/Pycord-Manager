import asyncio
from contextlib import suppress

from discord import Forbidden, HTTPException, Message

from utils import Cog


class Automod(Cog):
    def __init__(self, bot) -> None:
        super().__init__(bot)
        self.mod_role = bot.get_role(881407111211384902)
        self.muted_role = bot.get_role(881532095661494313)

    @Cog.listener()
    async def on_message(self, message: Message):
        mentions = sum(not member.bot for member in message.mentions)
        if mentions >= 5 and self.mod_role not in message.author.roles:
            await message.delete()
            if mentions >= 8:
                await message.guild.ban(
                    message.author, reason=f"Too many mentions ({mentions})"
                )
                return

            await message.channel.send(f"{message.author.mention} Too many mentions.")
            await message.author.add_roles(
                self.muted_role, reason=f"Too many mentions ({mentions})"
            )

            async def unmute():
                await asyncio.sleep(10800)  # 3 hours
                with suppress(Forbidden, HTTPException):
                    await message.author.remove_roles(
                        self.muted_role, reason="Mute duration expired."
                    )

            asyncio.create_task(unmute())


def setup(bot):
    bot.add_cog(Automod(bot))