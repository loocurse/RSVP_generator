#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE_EVENT, CHOOSE_DATE, CHOOSE_TIME, CHOOSE_LOCATION, CHOOSE_VERSE = range(5)


def start(update, context):
    event_keyboard = [['JC Service', 'POLITE Service'],
                      ['Combined Arrow service', 'Care group'],
                      ['Dare Service', 'Dare Group'],
                      ['Varsity Night', 'VG'],
                      ['Cluster', 'Men\'s and women\'s meeting'],
                      ]
    with open('users.txt','w+') as f:
        now = datetime.datetime.now()
        f.write(str(update.message.from_user.first_name))
        f.write('\n')
        f.write(now.strftime("%Y-%m-%d %H:%M"))
        f.write('\n')
        f.write('=========')
        f.write('\n')

    event_markup = ReplyKeyboardMarkup(event_keyboard, one_time_keyboard=True)

    reply_text = "Hi! Thanks for serving in the Father's house. 🏘 Let's craft that RSVP " \
                 "so that we can get the sheep right in! \n\nWhat is this event called? 🤔"

    update.message.reply_text(reply_text, reply_markup=event_markup)

    return CHOOSE_EVENT


def choosing_event(update, context):
    date_keyboard = [['This Friday'], ['This Saturday'], ['This Sunday']]

    date_markup = ReplyKeyboardMarkup(date_keyboard, one_time_keyboard=True)

    text = update.message.text
    context.user_data['event'] = text
    reply_text = 'Alright, sounds exciting!! What date will it be on?'

    update.message.reply_text(reply_text, reply_markup=date_markup)

    return CHOOSE_DATE


def get_date(day):
    day = day.split()[1]
    d = datetime.date.today()
    reference = {'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    while d.weekday() != reference[day]:
        d += datetime.timedelta(1)
    return '{} {}'.format(d.day, d.strftime("%B"))


def choosing_date(update, context):
    day = update.message.text
    context.user_data['input_date'] = day
    context.user_data['date'] = get_date(day)
    update.message.reply_text('Alright! {} would fall on {}! \n\nWhat time would it be? (e.g. 3pm)'.format(context.user_data['input_date'],context.user_data['date']))

    return CHOOSE_TIME


def choosing_time(update, context):
    location_keyboard = [['Shine Auditorium'], ['Star Studio'], ['MBS']]
    location_markup = ReplyKeyboardMarkup(location_keyboard, one_time_keyboard=True)

    time = update.message.text
    context.user_data['time'] = time

    update.message.reply_text('Where would it be held at?\nYou can type in a custom location if it\'s not below', reply_markup=location_markup)

    return CHOOSE_LOCATION


def choosing_location(update, context):
    verses = [['Matthew 11:28', 'Philippians 4:13', 'Isaiah 41:10'],
              ['Exodus 15:2', '2 Corinthians 12:9', 'Joshua 1:9'],
              ['2 Timothy 1:7', 'Psalms 27:1', 'Psalms 73:26'],
              ['Nehemiah 8:10', 'Psalms 23:4', '2 Thessalonians 3:3']]

    verses_markup = ReplyKeyboardMarkup(verses, one_time_keyboard=True)
    location = update.message.text
    context.user_data['location'] = location
    update.message.reply_text('Pick an encouraging verse to wrap this message up!',reply_markup=verses_markup)

    return CHOOSE_VERSE


def choosing_verse(update, context):
    verse = update.message.text
    verse_reference = { 'Matthew 11:28': 'Come to me, all who labor and are heavy laden, and I will give you rest.',
                        'Philippians 4:13':'I can do all things through him who strengthens me.',
                        'Isaiah 41:10':'Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you, I will uphold you with my righteous right hand.',
                        'Exodus 15:2':'The Lord is my strength and my song, and he has become my salvation; this is my God, and I will praise him, my father\'s God, and I will exalt him.',
                        '2 Corinthians 12:9': 'But he said to me, My grace is sufficient for you, for my power is made perfect in weakness',
                        'Joshua 1:9':'Have I not commanded you? Be strong and courageous. Do not be frightened, and do not be dismayed, for the Lord your God is with you wherever you go.',
                        '2 Timothy 1:7':'For God gave us a spirit not of fear but of power and love and self-control.',
                        'Psalms 27:1':'Of David. The Lord is my light and my salvation; whom shall I fear? The Lord is the stronghold of my life; of whom shall I be afraid?',
                        'Psalms 73:26':'My flesh and my heart may fail, but God is the strength of my heart and my portion forever.',
                        'Nehemiah 8:10':'And do not be grieved, for the joy of the Lord is your strength.',
                        'Psalms 23:4':'Even though I walk through the valley of the shadow of death, I will fear no evil, for you are with me; your rod and your staff, they comfort me.',
                        '2 Thessalonians 3:3':'But the Lord is faithful. He will establish you and guard you against the evil one.'}
    context.user_data['input_verse'] = verse
    context.user_data['verse'] = verse_reference[verse]

    update.message.reply_text('Here\'s the RSVP:')
    update.message.reply_text(craft_RSVP(context.user_data))
    update.message.reply_text('For any feedback/enquires, please DM me!! @loocurse')

    return ConversationHandler.END



def craft_RSVP(user_data):
    RSVP = '☀️*{}*☀️ \n\n{}\n📖 {} 📖\n\n' \
           'Welcome to the Father\'s house!! 🌈⛈🎉 It has been a draining week for all of us but let\'s be expectant that we ' \
           'will be filled as we seek after that one thing that is needful today!🌹🐧😊 \n\n📅 Date: {}, {}\n⌚ Time: {}\n📍 Location: ' \
           '{}\n\nI\'m coming!🙋‍🙋\n1.\n2.\n3.'''.format(user_data['event'], user_data['verse'],user_data['input_verse'],user_data['date'],user_data['input_date'].split()[1], user_data['time'],
                                                  user_data['location'])

    return RSVP


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("API KEY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE_EVENT: [MessageHandler(Filters.all,
                                          choosing_event),
                           ],

            CHOOSE_DATE: [MessageHandler(Filters.all,
                                         choosing_date),
                          ],

            CHOOSE_TIME: [MessageHandler(Filters.all,
                                         choosing_time),
                          ],

            CHOOSE_LOCATION: [MessageHandler(Filters.all,
                                             choosing_location),
                              ],

            CHOOSE_VERSE: [MessageHandler(Filters.all,
                                             choosing_verse),
                              ],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
