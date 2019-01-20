from telegram import Update

import db

_contexts = {
    'maya': ['майя', 'maya'],
    'erik': ['эрик', 'erik'],
    'robot': ['robot'],
}


def _get_message_context(update: Update):
    if not update.message:
        return None

    if not update.message.text:
        return None

    text = update.message.text.lower()

    for ctx, tags in _contexts.items():
        for t in tags:
            tag = '#' + t
            if tag in text:
                return ctx
    return None


def get_active_context(update: Update):
    msg_context = _get_message_context(update)

    user_id = update.message.from_user.id
    info = db.get_user_info(user_id)
    usr_context = info.get('context', None)

    if not msg_context:
        return usr_context

    if msg_context != usr_context:
        info['context'] = msg_context
        db.save_user_info(id, info)
    return msg_context
