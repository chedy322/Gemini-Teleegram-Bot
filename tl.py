# // Telegram with gemini response
# !pip install python-telegram-bot --upgrade
# !pip install nest_asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import getpass
# import nest_asyncio
import os
# nest_asyncio.apply()
# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def sendmsg(update: Update, context: ContextTypes.DEFAULT_TYPE, ai_msg) -> None:
    # question = update.message.text
    await update.message.reply_text(f"{ai_msg}\n{update.message.text}")
    # return question

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

# Set up Google API Key
os.environ["GOOGLE_API_KEY"] = getpass.getpass()

# Install required packages
# !pip install langchain_google_vertexai
# !pip install -qU langchain-google-genai
# !pip install --quiet --upgrade langchain langchain-community langchain-chroma langchain-google-genai pypdf

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Create the application
application = Application.builder().token("").build()

# Wrap the echo function to pass ai_msg
async def sendmsg_with_param(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    messages = [
        ("system", "You are a helpful assistant"),
        ("human", update.message.text),
    ]
    ai_msg = llm.invoke(messages)
    await sendmsg(update, context, ai_msg.content)

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT, sendmsg_with_param))

# Run the bot
# application.run_polling(allowed_updates=Update.ALL_TYPES)
application.run_polling()