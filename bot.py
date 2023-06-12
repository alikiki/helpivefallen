import json
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import openai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_config():
    with open("/root/helpivefallen/config.json", "r") as f:
        config = json.load(f)
        return config

NOTE_REGEX = re.compile(r'^Nn (.+)$')
QA_REGEX = re.compile(r'^(.+)\?\?(.+)$')
REGEXES = [NOTE_REGEX, QA_REGEX]
TELEGRAM_ID = get_config()['TELEGRAM_ID']

def confirm_id(iden):
    return iden in TELEGRAM_ID
    
def write_to_file(file, args):
    with open(file, "a") as f:
        if isinstance(args, str):
            f.write('\n' + args + '\n')
        elif isinstance(args, list):
            f.write('\n')
            for arg in args:
                f.write(arg + '\n')

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.1,
        n=1
    )
    return response.choices[0].text.strip()

async def define_word(word):
    prompt = f"Define the word: {word}\n\nDefinition: "
    return ask_gpt(prompt)

async def explain_concept(concept):
    prompt = f"Explain the following concept: {concept}\n\nExplanation: "
    return ask_gpt(prompt)

def gpt_methods(fn, arg_fn):
    async def f(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if confirm_id(update.effective_user.id):
            try:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Searching...")
                definition = await fn(arg_fn(context.args))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=definition)
            except:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Something wrong 🚨")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized!")
            

    return f

define = gpt_methods(define_word, lambda x: x[0])
explain = gpt_methods(explain_concept, lambda x: ' '.join(x).strip())

async def diary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if confirm_id(update.effective_user.id):
        try:
            write_to_file("/root/helpivefallen/diary.md", ' '.join(context.args).strip())
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Committed")

        except ValueError as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Something wrong 🚨")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized!")
    
async def qa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if confirm_id(update.effective_user.id):
        try:
            q, a = QA_REGEX.search(' '.join(context.args)).groups()
            q, a = q.strip(), a.strip()
            write_to_file("/root/helpivefallen/flashcards.md", [q + "?", "?", a])
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Committed")
        except (AttributeError, SyntaxError, ValueError) as e:
            if isinstance(e, AttributeError):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Use the <QUESTION>??<ANSWER> syntax")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Something wrong 🚨")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized!")


async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if confirm_id(update.effective_user.id):
        try:
            note = ' '.join(context.args)
            write_to_file("/root/helpivefallen/notes.md", note)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Committed")
        except ValueError as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Something wrong 🚨")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized!")

async def noncommander(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if confirm_id(update.effective_user.id):
        try: 
            match = NOTE_REGEX.search(update.message.text)
            write_to_file("/root/helpivefallen/notes.md", match.group(1).strip())
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Committed")
        except:
            try:
                match = QA_REGEX.search(update.message.text)
                q, a = match.groups()
                q, a = q.strip(), a.strip()
                write_to_file("/root/helpivefallen/flashcards.md", [q + "?", "?", a])
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Committed")
            except:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="If you want a note, use \"Nn <NOTE>\". If you want a QA, use the <QUESTION>??<ANSWER>.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized!")
    

if __name__ == '__main__':
    config = get_config()
    openai.api_key = config["OPENAI_KEY"]
    application = ApplicationBuilder().token(config['TELEGRAM_KEY']).build()

    # non-commands
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), noncommander)
    application.add_handler(msg_handler)
    
    # commands
    define_handler = CommandHandler('define', define)
    expl_handler = CommandHandler('explain', explain)
    qa_handler = CommandHandler('qa', qa)
    note_handler = CommandHandler('note', note)
    diary_handler = CommandHandler('diary', diary)
    application.add_handlers([qa_handler, note_handler, define_handler, expl_handler, diary_handler])
    
    application.run_polling()

