# About

This is a simple telegram bot that:

1. Collects all messages from the specified (in config) chats.
2. Saves all attached or forwarded files.
3. (Optionally) executes an external program after each update.

Purpose of this bot - to run on the server and collect incoming messages for further processing.

Examples:
- dedicating a chat to a project work journal that gets rendered to some HTML;
- collecting various bookmarks and files that relate to some R&D.

# Problems

No problems are left at this point

# SystemD running

copy this as bot.service to `/lib/systemd/system/bot.service`

```ini
[Unit]
Description=Telegram bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/proj/bot
ExecStart=/root/proj/bot/venv/bin/python app.py --key API_KEY --store STORAGE_FOLDER
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Where `STORAGE_FOLDER` should have a config json that looks like this:


```json
{
  "chats": {
    "CHAT_ID": {
      "folder": "robot"
    },
    "ANOTHER_CHAT_ID": {
      "folder": "test",
      "exec": [ "tail", "-1", "index.json" ]
    }
  },
  "reply_chat_id": "CHAT_ID_FOR_STATUS_REPLIES"
}
```