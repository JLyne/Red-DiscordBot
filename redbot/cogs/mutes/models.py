import enum
from typing import Optional, Dict

import discord

from dataclasses import dataclass

from redbot.core import i18n
from redbot.core.utils.chat_formatting import inline

T_ = i18n.Translator("Mutes", __file__)

_ = lambda s: s

_ = T_

class MuteIssue(enum.Enum):
    AlreadyMuted = "already_muted"
    AlreadyUnmuted = "already_unmuted"
    HierarchyProblem = "hierarchy_problem"
    AssignedRoleHierarchyProblem = "assigned_role_hierarchy_problem"
    IsAdmin = "is_admin"
    PermissionsIssueRole = "permissions_issue_role"
    PermissionsIssueGuild = "permissions_issue_guild"
    PermissionsIssueChannel = "permissions_issue_channel"
    LeftGuild = "left_guild"
    UnknownChannel = "unknown_channel"
    RoleMissing = "role_missing"
    RoleNotSet = "role_not_set"
    VoiceMutePermission = "voice_mute_permission"
    MuteIsTooLong = "mute_is_too_long"
    TimeoutsRequireTime = "timeouts_require_time"
    IsNotVoiceMute = "is_not_voice_mute"

MUTE_UNMUTE_ISSUES = {
    MuteIssue.AlreadyMuted: "That user is already muted in {location}.",
    MuteIssue.AlreadyUnmuted: "That user is not muted in {location}.",
    MuteIssue.HierarchyProblem:
        "I cannot let you do that. You are not higher than the user in the role hierarchy.",
    MuteIssue.AssignedRoleHierarchyProblem:
        "I cannot let you do that. You are not higher than the mute role in the role hierarchy.",
    MuteIssue.IsAdmin: "That user cannot be (un)muted, as they have the Administrator permission.",
    MuteIssue.PermissionsIssueRole:
        "Failed to mute or unmute user. I need the Manage Roles "
        "permission and the user I'm muting must be "
        "lower than myself in the role hierarchy.",
    MuteIssue.PermissionsIssueGuild:
        "Failed to mute or unmute user. I need the Timeout Members "
        "permission and the user I'm muting must be "
        "lower than myself in the role hierarchy.",
    MuteIssue.PermissionsIssueChannel:
        "Failed to mute or unmute user. I need the Manage Permissions permission in {location}.",
    MuteIssue.LeftGuild: "The user has left the server while applying an overwrite.",
    MuteIssue.UnknownChannel: "The channel I tried to mute or unmute the user in isn't found.",
    MuteIssue.RoleMissing: "The mute role no longer exists.",
    MuteIssue.VoiceMutePermission:
        "Because I don't have the Move Members permission, this will take into effect when the user rejoins.",
    MuteIssue.MuteIsTooLong: "Timeouts cannot be longer than 28 days.",
    MuteIssue.TimeoutsRequireTime: "You must provide a time for the timeout to end.",
    MuteIssue.IsNotVoiceMute:
        "That user is channel muted in their current voice channel, not just voice muted."
        " If you want to fully unmute this user in the channel,"
        " use {command} in their voice channel's text channel instead.",
}


@dataclass
class MuteResponse:
    success: bool
    reason: Optional[MuteIssue]
    user: discord.Member

    def get_reason_text(self):
        if self.reason is None:
            return None

        return _(MUTE_UNMUTE_ISSUES[self.reason]).format(command=inline("unmutechannel"), location=_("this server"))


@dataclass
class ChannelMuteResponse(MuteResponse):
    channel: discord.abc.GuildChannel
    old_overs: Optional[Dict[str, bool]]
    voice_mute: bool

    def get_reason_text(self):
        if self.reason is None:
            return None

        location = self.channel.mention if self.channel else _("this server")

        return _(MUTE_UNMUTE_ISSUES[self.reason]).format(command=inline("unmutechannel"), location=location)
