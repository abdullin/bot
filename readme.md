# Problems

- Problem: bot might be running on a server with a VPN connection. 
When it terminates, bot will stuck forever trying to reconnect to telegram servers

```text
Jan 23 04:28:55 dev python[1222]: telegram.error.NetworkError: urllib3 HTTPError HTTPSConnectionPool(host='api.telegram.org', port=443): Max retries exceeded with url: /bot268340955:AAH-FmjPbrMk6y2OoI_mYzoipozLiKOJ0Gg/getUpdates (Caused by NewCo
Jan 23 04:30:21 dev python[1222]: 2019-01-23 04:30:21,325 - telegram.vendor.ptb_urllib3.urllib3.connectionpool - WARNING - Retrying (Retry(total=2, connect=None, read=None, redirect=None)) after connection broken by 'NewConnectionError('<telegra
Jan 23 04:31:17 dev python[1222]: 2019-01-23 04:31:17,378 - telegram.vendor.ptb_urllib3.urllib3.connectionpool - WARNING - Retrying (Retry(total=1, connect=None, read=None, redirect=None)) after connection broken by 'NewConnectionError('<telegra
Jan 23 04:32:13 dev python[1222]: 2019-01-23 04:32:13,437 - telegram.vendor.ptb_urllib3.urllib3.connectionpool - WARNING - Retrying (Retry(total=0, connect=None, read=None, redirect=None)) after connection broken by 'NewConnectionError('<telegra
Jan 23 04:33:09 dev python[1222]: 2019-01-23 04:33:09,496 - telegram.ext.updater - ERROR - Error while getting Updates: urllib3 HTTPError HTTPSConnectionPool(host='api.telegram.org', port=443): Max retries exceeded with url: /bot268340955:AAH-Fm
Jan 23 04:33:09 dev python[1222]: 2019-01-23 04:33:09,496 - telegram.ext.dispatcher - ERROR - No error handlers are registered, logging exception.
Jan 23 04:33:09 dev python[1222]: Traceback (most recent call last):
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connection.py", line 141, in _new_conn
Jan 23 04:33:09 dev python[1222]:     (self.host, self.port), self.timeout, **extra_kw)
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/util/connection.py", line 60, in create_connection
Jan 23 04:33:09 dev python[1222]:     for res in socket.getaddrinfo(host, port, family, socket.SOCK_STREAM):
Jan 23 04:33:09 dev python[1222]:   File "/usr/lib/python3.6/socket.py", line 745, in getaddrinfo
Jan 23 04:33:09 dev python[1222]:     for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
Jan 23 04:33:09 dev python[1222]: socket.gaierror: [Errno -3] Temporary failure in name resolution
Jan 23 04:33:09 dev python[1222]: During handling of the above exception, another exception occurred:
Jan 23 04:33:09 dev python[1222]: Traceback (most recent call last):
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 617, in urlopen
Jan 23 04:33:09 dev python[1222]:     chunked=chunked)
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 360, in _make_request
Jan 23 04:33:09 dev python[1222]:     self._validate_conn(conn)
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 857, in _validate_conn
Jan 23 04:33:09 dev python[1222]:     super(HTTPSConnectionPool, self)._validate_conn(conn)
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connectionpool.py", line 289, in _validate_conn
Jan 23 04:33:09 dev python[1222]:     conn.connect()
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connection.py", line 284, in connect
Jan 23 04:33:09 dev python[1222]:     conn = self._new_conn()
Jan 23 04:33:09 dev python[1222]:   File "/root/proj/bot/venv/lib/python3.6/site-packages/telegram/vendor/ptb_urllib3/urllib3/connection.py", line 150, in _new_conn
Jan 23 04:33:09 dev python[1222]:     self, "Failed to establish a new connection: %s" % e)
```



- Problem: collaboration is tricky, different people see different sides
of a single context and may post duplicate information

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
ExecStart=/root/proj/bot/venv/bin/python app.py --key API_KEY --www WWW_ROOT
Restart=on-failure

[Install]
WantedBy=multi-user.target
```