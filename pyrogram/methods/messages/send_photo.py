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

import logging
import os
import re
from datetime import datetime
from typing import Union, BinaryIO, List, Optional, Callable

import pyrogram
from pyrogram import raw, enums, types, utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType
from .inline_session import get_session

log = logging.getLogger(__name__)


class SendPhoto:
    async def send_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        photo: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_parameters: "types.ReplyParameters" = None,
        message_thread_id: int = None,
        business_connection_id: str = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        view_once: bool = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional["types.Message"]:
        """Send photos.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            photo (``str`` | ``BinaryIO``):
                Photo to send.
                Pass a file_id as string to send a photo that exists on the Telegram servers,
                pass an HTTP URL as a string for Telegram to get a photo from the Internet,
                pass a file path as string to upload a new photo that exists on your local machine, or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            caption (``str``, *optional*):
                Photo caption, 0-1024 characters.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            has_spoiler (``bool``, *optional*):
                Pass True if the photo needs to be covered with a spoiler animation.

            ttl_seconds (``int``, *optional*):
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct in *ttl_seconds*
                seconds after it was viewed.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Description of the message to reply to

            message_thread_id (``int``, *optional*):
                If the message is in a thread, ID of the original message.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message will be sent.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            view_once (``bool``, *optional*):
                Pass True if the photo should be viewable only once.

            message_effect_id (``int`` ``64-bit``, *optional*):
                Unique identifier of the message effect to be added to the message; for private chats only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            :obj:`~pyrogram.types.Message` | ``None``: On success, the sent photo message is returned, otherwise, in
            case the upload is deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is returned.

        Example:
            .. code-block:: python

                # Send photo by uploading from local file
                await app.send_photo("me", "photo.jpg")

                # Send photo by uploading from URL
                await app.send_photo("me", "https://example.com/example.jpg")

                # Add caption to a photo
                await app.send_photo("me", "photo.jpg", caption="Caption")

                # Send self-destructing photo
                await app.send_photo("me", "photo.jpg", ttl_seconds=10)
        """

        if reply_to_message_id and reply_parameters:
            raise ValueError(
                "Parameters `reply_to_message_id` and `reply_parameters` are mutually "
                "exclusive."
            )
        
        if reply_to_message_id is not None:
            log.warning(
                "This property is deprecated. "
                "Please use reply_parameters instead"
            )
            reply_parameters = types.ReplyParameters(message_id=reply_to_message_id)

        file = None
        ttl_seconds = 0x7FFFFFFF if view_once else ttl_seconds

        try:
            if isinstance(photo, str):
                if os.path.isfile(photo):
                    file = await self.save_file(photo, progress=progress, progress_args=progress_args)
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file,
                        ttl_seconds=ttl_seconds,
                        spoiler=has_spoiler,
                    )
                elif re.match("^https?://", photo):
                    media = raw.types.InputMediaPhotoExternal(
                        url=photo,
                        ttl_seconds=ttl_seconds,
                        spoiler=has_spoiler
                    )
                else:
                    media = utils.get_input_media_from_file_id(
                        photo,
                        FileType.PHOTO,
                        ttl_seconds=ttl_seconds,
                        has_spoiler=has_spoiler
                    )
            else:
                file = await self.save_file(photo, progress=progress, progress_args=progress_args)
                media = raw.types.InputMediaUploadedPhoto(
                    file=file,
                    ttl_seconds=ttl_seconds,
                    spoiler=has_spoiler
                )

            reply_to = await utils._get_reply_message_parameters(
                self,
                message_thread_id,
                reply_parameters
            )
            rpc = raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=media,
                silent=disable_notification or None,
                reply_to=reply_to,
                random_id=self.rnd_id(),
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                effect=message_effect_id,
                **await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
            )
            session = None
            business_connection = None
            if business_connection_id:
                business_connection = self.business_user_connection_cache[business_connection_id]
                if not business_connection:
                    business_connection = await self.get_business_connection(business_connection_id)
                session = await get_session(
                    self,
                    business_connection._raw.connection.dc_id
                )

            while True:
                try:
                    if business_connection_id:
                        r = await session.invoke(
                            raw.functions.InvokeWithBusinessConnection(
                                query=rpc,
                                connection_id=business_connection_id
                            )
                        )
                        # await session.stop()
                    else:
                        r = await self.invoke(rpc)
                except FilePartMissing as e:
                    await self.save_file(photo, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(
                            i,
                            (
                                raw.types.UpdateNewMessage,
                                raw.types.UpdateNewChannelMessage,
                                raw.types.UpdateNewScheduledMessage
                            )
                        ):
                            return await types.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                            )
                        elif isinstance(
                            i,
                            (
                                raw.types.UpdateBotNewBusinessMessage
                            )
                        ):
                            return await types.Message._parse(
                                self,
                                i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                business_connection_id=getattr(i, "connection_id", business_connection_id),
                                raw_reply_to_message=i.reply_to_message
                            )
        except pyrogram.StopTransmission:
            return None
