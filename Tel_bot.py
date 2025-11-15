

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters


# Translator Logic

def assemble_to_machine_code(assembly_code: str) -> str:
    """
    Converts assembly instructions to mock machine code (demo only).
    You can expand this dictionary for more instructions.
    """
    asm_to_machine = {
        "MOV A, B": "78",
        "MOV B, A": "79",
        "ADD A, B": "80",
        "SUB A, B": "90",
        "MUL A, B": "A0",
        "DIV A, B": "B0",
        "INC A": "3C",
        "DEC A": "3D",
        "HLT": "FF"
    }

    lines = assembly_code.strip().split('\n')
    machine_code = []

    for line in lines:
        line = line.strip().upper()
        code = asm_to_machine.get(line, "??")  
        machine_code.append(f"{line} → {code}")

    return "\n".join(machine_code)


# Bot Commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! I’m your *Assembly-to-Machine-Code Translator Bot*.\n\n"
        "Just send me assembly instructions (one or more lines), "
        "and I’ll translate them into machine code instantly!\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Get usage help\n"
        "/translate - Start translation mode"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 *How to use me:*\n"
        "1️⃣ Type or paste your assembly code (e.g., `MOV A, B`)\n"
        "2️⃣ I’ll reply with equivalent machine code.\n\n"
        "Supported Commands:\n"
        "/start - Start bot\n"
        "/help - Show this message\n"
        "/translate - Translate assembly code"
    )

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Send your assembly code now, and I’ll translate it!")


# Handle All Text Messages Dynamically

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    translation = assemble_to_machine_code(user_input)
    await update.message.reply_text(f"💡 *Translation Result:*\n\n{translation}", parse_mode="Markdown")


# Main Functio

def main():
    BOT_TOKEN = " "  # Replace with your Telegram bot token
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("translate", translate_command))

    # Message handler (dynamic input)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
