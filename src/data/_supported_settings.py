SUPPORTED_SETTINGS_DATA = {
    "announcement_msg_for_post": {
        "content": "any_string",
        "tips": "This setting sends an announcement when you post!\nUse {user} or {platform} to write out the user or platform in the message",
        "question": "Does this look like the message you want to send when a post OR video is sent?"
    },
    "announcement_msg_for_video": {
        "content": "any_string",
        "tips": "This setting sends a helpful message about your video since we cannot embed videos into embeded messages.",
        "question": "Does this look like the message you want to send when a video is sent?"
    },
    "send_video_as_link": {
        "content": {"Yes", "No"},
        "tips": "This setting makes sure that if there is no embedded message if you select yes. NOTE: this is not recommended as sometimes discord web embeds don't show up",
        "question": "Does this look like the correct setting you chose?"
    },
}

DEFAULT_SETTINGS_DATA = {
    "announcement_msg_for_post": "**New post from {user} on {platform}**",
    "announcement_msg_for_video": "Click to view video",
    "send_video_as_link": "No",
}
