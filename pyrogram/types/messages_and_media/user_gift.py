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

from datetime import datetime
from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class UserGift(Object):
    """Represents a gift received by a user.

    Parameters:
        sender_user_id (:obj:`~pyrogram.types.User`, *optional*):
            Identifier of the user that sent the gift; None if unknown.

        text (``str``, *optional*):
            Message added to the gift.
        
        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text.

        is_private (``bool``, *optional*):
            True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone are able to see them.

        is_saved (``bool``, *optional*):
            True, if the gift is displayed on the user's profile page; may be False only for the receiver of the gift.

        date (``datetime``):
            Date when the gift was sent.

        gift (:obj:`~pyrogram.types.Gift`, *optional*):
            Information about the gift.
        
        message_id (``int``, *optional*):
            Identifier of the message with the gift in the chat with the sender of the gift; can be None or an identifier of a deleted message; only for the gift receiver.

        sell_star_count (``int``, *optional*):
            Number of Telegram Stars that can be claimed by the receiver instead of the gift; only for the gift receiver.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        sender_user_id: Optional["types.User"] = None,
        text: Optional[str] = None,
        entities: List["types.MessageEntity"] = None,
        date: datetime,
        is_private: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        gift: Optional["types.Gift"] = None,
        message_id: Optional[int] = None,
        sell_star_count: Optional[int] = None
    ):
        super().__init__(client)

        self.date = date
        self.gift = gift
        self.is_private = is_private
        self.is_saved = is_saved
        self.sender_user_id = sender_user_id
        self.text = text
        self.entities = entities
        self.message_id = message_id
        self.sell_star_count = sell_star_count

    @staticmethod
    async def _parse(
        client,
        user_star_gift: "raw.types.UserStarGift",
        users: dict
    ) -> "UserGift":
        text, entities = None, None
        if getattr(user_star_gift, "message", None):
            text, entities = (await utils.parse_text_entities(self, user_star_gift.message.text, None, user_star_gift.message.entities)).values()
        return UserGift(
            date=utils.timestamp_to_datetime(user_star_gift.date),
            gift=await types.Gift._parse(client, user_star_gift.gift),
            is_private=getattr(user_star_gift, "name_hidden", None),
            is_saved=not user_star_gift.unsaved if getattr(user_star_gift, "unsaved", None) else None,
            sender_user_id=types.User._parse(client, users.get(user_star_gift.from_id)) if getattr(user_star_gift, "from_id", None) else None,
            text=user_star_gift.message.text if getattr(user_star_gift, "message", None) else None,
            message_id=getattr(user_star_gift, "msg_id", None),
            sell_star_count=getattr(user_star_gift, "convert_stars", None),
            text=text,
            entities=entities,
            client=client
        )
