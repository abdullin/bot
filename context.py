from telegram import Update, User

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

    user:User = update.message.from_user
    if not user:
        return None

    info = db.get_user_info(user.id)
    usr_context = info.get('context', None)

    if not msg_context:
        return usr_context

    if msg_context != usr_context:
        info['context'] = msg_context
        db.save_user_info(user.id, info)
    return msg_context
