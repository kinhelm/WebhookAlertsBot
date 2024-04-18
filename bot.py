from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select


import keys
from models.Base import Base
from models.User import User

TELEGRAM_BOT_TOKEN = keys.token
engine = create_engine("sqlite:///mydb.db", echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Register a user"""
    user = session.scalars(select(User).filter_by(id_telegram=update.message.from_user.id)).first()
    if user is None:
        user = User(
            id_telegram=update.message.from_user.id,
            firstname=update.message.from_user.first_name,
            chat_id=update.message.chat_id
        )
        session.add(user)
        session.commit()

    await update.message.reply_text(
        f"Hi {user.firstname}, you are now registered for the alert bot !",
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', register)
    application.add_handler(start_handler)

    application.run_polling()
