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
from pyrogram import types, raw


class GetStreamRtmpUrl:
    async def get_stream_rtmp_url(
        self: "pyrogram.Client", chat_id: Union[int, str], revoke: bool = None
    ) -> "types.StreamRtmpUrl":
        """Get RTMP URL and stream key for RTMP livestreams.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat. A chat can be either a basic group, supergroup or a channel.

            revoke (``bool``, *optional*):
                Whether to revoke the previous stream key or simply return the existing one.

        Returns:
            :obj:`~pyrogram.types.StreamRtmpUrl`: On success, the RTMP URL and stream key is returned.

        Example:
            .. code-block:: python

                await app.get_stream_rtmp_url(chat_id)

        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            raise ValueError("Target chat should be group, supergroup or channel.")

        r = await self.invoke(
            raw.functions.phone.GetGroupCallStreamRtmpUrl(peer=peer, revoke=revoke)
        )

        return types.StreamRtmpUrl._parse(r)
