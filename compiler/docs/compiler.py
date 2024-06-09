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

import ast
import os
import re
import shutil

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
PYROGRAM_API_DEST = "docs/source/api"

FUNCTIONS_PATH = "pyrogram/raw/functions"
TYPES_PATH = "pyrogram/raw/types"
BASE_PATH = "pyrogram/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snek(s: str):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i, encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name
                        break
                else:
                    continue

                full_path = os.path.basename(path) + "/" + snek(name).replace("_", "-") + ".rst"

                if level:
                    full_path = base + "/" + full_path

                namespace = path.split("/")[-1]
                if namespace in ["base", "types", "functions"]:
                    namespace = ""

                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                os.makedirs(os.path.dirname(DESTINATION + "/" + full_path), exist_ok=True)

                with open(DESTINATION + "/" + full_path, "w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path="pyrogram.raw.{}".format(
                                ".".join(full_path.split("/")[:-1]) + "." + name
                            )
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = []

        for i in v:
            entities.append(f'{i} <{snek(i).replace("_", "-")}>')

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = "pyrogram.raw.{}.{}".format(base, k)
        else:
            for i in sorted(list(all_entities), reverse=True):
                if i != base:
                    entities.insert(0, "{0}/index".format(i))

            inner_path = base + "/index" + ".rst"
            module = "pyrogram.raw.{}".format(base)

        with open(DESTINATION + "/" + inner_path, "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities)
                )
            )

            f.write("\n")


def pyrogram_api():
    def get_title_list(s: str) -> list:
        return [i.strip() for i in [j.strip() for j in s.split("\n") if j] if i]

    # Methods

    categories = dict(
        utilities="""
        Utilities
            start
            stop
            restart
            run
            add_handler
            remove_handler
            export_session_string
            stop_transmission
            set_parse_mode
        """,
        advanced="""
        Advanced
            invoke
            resolve_peer
            save_file
        """,
        authorization="""
        Authorization
            connect
            disconnect
            initialize
            terminate
            send_code
            resend_code
            sign_in
            sign_in_bot
            sign_up
            get_password_hint
            check_password
            send_recovery_code
            recover_password
            accept_terms_of_service
            log_out
        """,
        bots="""
        Bots
            get_inline_bot_results
            send_inline_bot_result
            answer_callback_query
            answer_inline_query
            request_callback_answer
            send_game
            set_game_score
            get_game_high_scores
            set_bot_commands
            get_bot_commands
            delete_bot_commands
            set_bot_default_privileges
            get_bot_default_privileges
            set_chat_menu_button
            get_chat_menu_button
            answer_web_app_query
            send_web_app_custom_request
            set_bot_name
            get_bot_name
            set_bot_info_description
            get_bot_info_description
            set_bot_info_short_description
            get_bot_info_short_description
        """,
        chats="""
        Chats
            join_chat
            leave_chat
            search_chats
            ban_chat_member
            unban_chat_member
            restrict_chat_member
            promote_chat_member
            set_administrator_title
            set_chat_photo
            delete_chat_photo
            set_chat_title
            set_chat_description
            set_chat_permissions
            pin_chat_message
            unpin_chat_message
            unpin_all_chat_messages
            get_chat
            get_chat_member
            get_chat_members
            get_chat_members_count
            get_dialogs
            get_dialogs_count
            set_chat_username
            get_nearby_chats
            archive_chats
            unarchive_chats
            add_chat_members
            create_channel
            create_group
            create_supergroup
            delete_channel
            delete_supergroup
            delete_user_history
            set_slow_mode
            set_chat_ttl
            mark_chat_unread
            get_chat_event_log
            get_chat_online_count
            get_send_as_chats
            set_send_as_chat
            set_chat_protected_content
            get_created_chats
        """,
        chat_topics="""
        Chat Forum Topics
            close_forum_topic
            create_forum_topic
            delete_forum_topic
            edit_forum_topic
            get_forum_topic_icon_stickers
            hide_forum_topic
            reopen_forum_topic
            unhide_forum_topic
            get_forum_topics
            get_forum_topic
        """,
        contacts="""
        Contacts
            add_contact
            delete_contacts
            import_contacts
            get_contacts
            get_contacts_count
        """,
        invite_links="""
        Invite Links
            get_chat_invite_link
            export_chat_invite_link
            create_chat_invite_link
            edit_chat_invite_link
            revoke_chat_invite_link
            delete_chat_invite_link
            get_chat_invite_link_joiners
            get_chat_invite_link_joiners_count
            get_chat_admin_invite_links
            get_chat_admin_invite_links_count
            get_chat_admins_with_invite_links
            get_chat_join_requests
            delete_chat_admin_invite_links
            approve_chat_join_request
            approve_all_chat_join_requests
            decline_chat_join_request
            decline_all_chat_join_requests
        """,
        messages="""
        Messages
            copy_media_group
            copy_message
            delete_messages
            download_media
            edit_cached_media
            edit_inline_caption
            edit_inline_media
            edit_inline_reply_markup
            edit_inline_text
            edit_message_caption
            edit_message_media
            edit_message_reply_markup
            edit_message_text
            forward_messages
            get_chat_history
            get_chat_history_count
            get_custom_emoji_stickers
            get_discussion_message
            get_discussion_replies
            get_discussion_replies_count
            get_media_group
            get_messages
            read_chat_history
            retract_vote
            search_global
            search_global_count
            search_messages
            search_messages_count
            search_public_hashtag_messages
            search_public_hashtag_messages_count
            send_animation
            send_audio
            send_cached_media
            send_chat_action
            send_contact
            send_dice
            send_document
            send_location
            send_media_group
            send_message
            send_photo
            send_poll
            send_sticker
            send_venue
            send_video
            send_video_note
            send_voice
            set_reaction
            stop_poll
            stream_media
            view_messages
            vote_poll
            get_chat_sponsored_messages
            translate_message_text
        """,
        password="""
        Password
            enable_cloud_password
            change_cloud_password
            remove_cloud_password
        """,
        phone="""
        Phone
            create_video_chat
            discard_group_call
            get_video_chat_rtmp_url
            invite_group_call_participants
            load_group_call_participants

        """,
        stickers="""
        Stickers
            get_message_effects
            get_stickers
        """,
        users="""
        Users
            get_me
            get_users
            get_chat_photos
            get_chat_photos_count
            set_profile_photo
            delete_profile_photos
            set_username
            update_profile
            block_user
            unblock_user
            get_common_chats
            get_default_emoji_statuses
            set_emoji_status
            set_birthdate
            set_personal_chat
        """,
        business="""
        Telegram Business & Fragment
            answer_pre_checkout_query
            answer_shipping_query
            create_invoice_link
            get_business_connection
            get_collectible_item_info
            refund_star_payment
            send_invoice
        """,   
    )

    root = PYROGRAM_API_DEST + "/methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *methods = get_title_list(v)
            fmt_keys.update({k: "\n    ".join("{0} <{0}>".format(m) for m in methods)})

            for method in methods:
                with open(root + "/{}.rst".format(method), "w") as f2:
                    title = "{}()".format(method)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: pyrogram.Client.{}()".format(method))

            functions = ["idle", "compose"]

            for func in functions:
                with open(root + "/{}.rst".format(func), "w") as f2:
                    title = "{}()".format(func)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autofunction:: pyrogram.{}()".format(func))

        f.write(template.format(**fmt_keys))

    # Types

    categories = dict(
        authorization="""
        Authorization
            SentCode
            TermsOfService
        """,
        bot_commands="""
        Bot Commands
            BotCommand
            BotCommandScope
            BotCommandScopeAllChatAdministrators
            BotCommandScopeAllGroupChats
            BotCommandScopeAllPrivateChats
            BotCommandScopeChat
            BotCommandScopeChatAdministrators
            BotCommandScopeChatMember
            BotCommandScopeDefault
        """,
        bot_keyboards="""
        Bot keyboards
            CallbackGame
            CallbackQuery
            ForceReply
            GameHighScore
            InlineKeyboardButton
            InlineKeyboardMarkup
            KeyboardButton
            KeyboardButtonPollType
            KeyboardButtonPollTypeRegular
            KeyboardButtonPollTypeQuiz
            KeyboardButtonRequestChat
            KeyboardButtonRequestUsers
            ReplyKeyboardMarkup
            ReplyKeyboardRemove
            LoginUrl
            WebAppInfo
            MenuButton
            MenuButtonCommands
            MenuButtonWebApp
            MenuButtonDefault
            SentWebAppMessage
            SwitchInlineQueryChosenChat
        """,
        chat_topics="""
        Chat Forum Topics
            ForumTopic
            ForumTopicClosed
            ForumTopicCreated
            ForumTopicEdited
            ForumTopicReopened
            GeneralForumTopicHidden
            GeneralForumTopicUnhidden
        """,
        inline_mode="""
        Inline Mode
            ChosenInlineResult
            InlineQuery
            InlineQueryResult
            InlineQueryResultCachedAnimation
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultAnimation
            InlineQueryResultAudio
            InlineQueryResultDocument
            InlineQueryResultPhoto
            InlineQueryResultVideo
            InlineQueryResultVoice
            InlineQueryResultArticle
            InlineQueryResultContact
            InlineQueryResultLocation
            InlineQueryResultVenue
        """,
        input_media="""
        Input Media
            InputMedia
            InputMediaPhoto
            InputMediaVideo
            InputMediaAudio
            InputMediaAnimation
            InputMediaDocument
            InputPhoneContact
            LinkPreviewOptions
        """,
        input_message_content="""
        InputMessageContent
            ExternalReplyInfo
            InputMessageContent
            InputPollOption
            InputTextMessageContent
            ReplyParameters
            TextQuote
        """,
        messages_media="""
        Messages & Media
            Animation
            Audio
            ChatBoostAdded
            Contact
            Dice
            Document
            Game
            GiftCode
            GiftedPremium
            Giveaway
            GiveawayCompleted
            GiveawayWinners
            Location
            Message
            MessageEffect
            MessageEntity
            MessageImportInfo
            MessageOrigin
            MessageOriginChannel
            MessageOriginChat
            MessageOriginHiddenUser
            MessageOriginUser
            MessageReactionCountUpdated
            MessageReactionUpdated
            MessageReactions
            Photo
            Reaction
            ReactionCount
            ReactionType
            ReactionTypeEmoji
            ReactionTypeCustomEmoji
            Thumbnail
            TranslatedText
            StrippedThumbnail
            Poll
            PollOption
            SponsoredMessage
            Sticker
            Story
            Venue
            Video
            VideoNote
            Voice
            WebAppData
            WebPage
        """,
        business="""
        Telegram Business
            BusinessConnection
            BusinessIntro
            BusinessLocation
            BusinessOpeningHours
            BusinessOpeningHoursInterval
            CollectibleItemInfo
            Invoice
            LabeledPrice
            OrderInfo
            PreCheckoutQuery
            ShippingAddress
            ShippingOption
            ShippingQuery
            SuccessfulPayment
        """,
        users_chats="""
        Users & Chats
            Birthdate
            Chat
            ChatAdminWithInviteLinks
            ChatColor
            ChatEvent
            ChatEventFilter
            ChatInviteLink
            ChatJoiner
            ChatJoinRequest
            ChatMember
            ChatMemberUpdated
            ChatPermissions
            ChatPhoto
            ChatPrivileges
            ChatReactions
            ChatShared
            Dialog
            EmojiStatus
            GroupCallParticipant
            InviteLinkImporter
            Restriction
            User
            Username
            UsersShared
            VideoChatEnded
            VideoChatParticipantsInvited
            VideoChatScheduled
            VideoChatStarted
            RtmpUrl
        """,
    )

    root = PYROGRAM_API_DEST + "/types"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/types.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *types = get_title_list(v)

            fmt_keys.update({k: "\n    ".join(types)})

            # noinspection PyShadowingBuiltins
            for type in types:
                with open(root + "/{}.rst".format(type), "w") as f2:
                    title = "{}".format(type)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. autoclass:: pyrogram.types.{}()\n".format(type))

        f.write(template.format(**fmt_keys))

    # Bound Methods

    categories = dict(
        message="""
        Message
            Message.click
            Message.delete
            Message.download
            Message.forward
            Message.copy
            Message.pin
            Message.unpin
            Message.edit
            Message.edit_text
            Message.edit_cached_media
            Message.edit_caption
            Message.edit_media
            Message.edit_reply_markup
            Message.reply
            Message.reply_text
            Message.reply_animation
            Message.reply_audio
            Message.reply_cached_media
            Message.reply_chat_action
            Message.reply_contact
            Message.reply_document
            Message.reply_game
            Message.reply_inline_bot_result
            Message.reply_location
            Message.reply_media_group
            Message.reply_photo
            Message.reply_poll
            Message.reply_sticker
            Message.reply_venue
            Message.reply_video
            Message.reply_video_note
            Message.reply_voice
            Message.get_media_group
            Message.react
            Message.read
            Message.view
        """,
        chat="""
        Chat
            Chat.archive
            Chat.unarchive
            Chat.set_title
            Chat.set_description
            Chat.set_photo
            Chat.ban_member
            Chat.unban_member
            Chat.restrict_member
            Chat.promote_member
            Chat.get_member
            Chat.get_members
            Chat.add_members
            Chat.join
            Chat.leave
            Chat.mark_unread
            Chat.set_protected_content
            Chat.unpin_all_messages
        """,
        user="""
        User
            User.archive
            User.unarchive
            User.block
            User.unblock
        """,
        callback_query="""
        Callback Query
            CallbackQuery.answer
            CallbackQuery.edit_message_text
            CallbackQuery.edit_message_caption
            CallbackQuery.edit_message_media
            CallbackQuery.edit_message_reply_markup
        """,
        inline_query="""
        InlineQuery
            InlineQuery.answer
        """,
        pre_checkout_query="""
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
        shipping_query="""
        ShippingQuery
            ShippingQuery.answer
        """,
        chat_join_request="""
        ChatJoinRequest
            ChatJoinRequest.approve
            ChatJoinRequest.decline
        """,
        story="""
        Story
            Story.react
            Story.download
        """,
    )

    root = PYROGRAM_API_DEST + "/bound-methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/bound-methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in categories.items():
            name, *bound_methods = get_title_list(v)

            fmt_keys.update({"{}_hlist".format(k): "\n    ".join("- :meth:`~{}`".format(bm) for bm in bound_methods)})

            fmt_keys.update(
                {"{}_toctree".format(k): "\n    ".join("{} <{}>".format(bm.split(".")[1], bm) for bm in bound_methods)})

            # noinspection PyShadowingBuiltins
            for bm in bound_methods:
                with open(root + "/{}.rst".format(bm), "w") as f2:
                    title = "{}()".format(bm)

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(".. automethod:: pyrogram.types.{}()".format(bm))

        f.write(template.format(**fmt_keys))


def start():
    global page_template
    global toctree

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with open(HOME + "/template/page.txt", encoding="utf-8") as f:
        page_template = f.read()

    with open(HOME + "/template/toctree.txt", encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    pyrogram_api()


if "__main__" == __name__:
    FUNCTIONS_PATH = "../../pyrogram/raw/functions"
    TYPES_PATH = "../../pyrogram/raw/types"
    BASE_PATH = "../../pyrogram/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    PYROGRAM_API_DEST = "../../docs/source/api"

    start()
