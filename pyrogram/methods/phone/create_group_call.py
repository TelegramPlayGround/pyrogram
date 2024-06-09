#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import types, raw, utils
from datetime import datetime


class CreateGroupCall:
    async def create_group_call(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rtmp: bool = None,
        title: str = None,
        schedule_date: datetime = None,
    ) -> "types.Message":
        """Create a group/channel call or livestream

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat. A chat can be either a basic group, supergroup or a channel.

            rtmp (``bool``, *optional*):
                Whether RTMP stream support should be enabled: only the group/supergroup/channel owner can use this parameter.

            title (``str``, *optional*):
                Call title.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                For scheduled group call or livestreams, the absolute date when the group call will start.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent service message is returned.

        Example:
            .. code-block:: python

                await app.create_group_call(chat_id)

        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            raise ValueError("Target chat should be group, supergroup or channel.")

        r = await self.invoke(
            raw.functions.phone.CreateGroupCall(
                peer=peer,
                random_id=self.rnd_id(),
                rtmp_stream=rtmp,
                title=title,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
            )
        )

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateNewChannelMessage,
                    raw.types.UpdateNewMessage,
                    raw.types.UpdateNewScheduledMessage,
                ),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                )
