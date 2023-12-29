import os
import asyncio
from pyrogram import Client
from datetime import datetime
from pyrogram.enums import ChatType, ChatMemberStatus


if not os.path.exists("sessions"):
    os.mkdir("sessions")
    

# Telegram API Keys
API_HASH = os.getenv("API_HASH")
API_ID = os.getenv("API_ID")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


async def main():
    await app.start()
    me = await app.get_me()
    user_id = me.id
    
    chats = []
    print("Following are your joined chats... \n")
    
    async for dialog in app.get_dialogs():
        chat_id = dialog.chat.id
        username = f"@{dialog.chat.username}"
        
        # if the username is hidden or not set
        if username == "@None":
            username = dialog.chat.first_name
            
            # if the first name is also not set then it's a private chat 
            if username == None or username == "None":
                username = dialog.chat.title
        
        chats.append({
            "id": chat_id,
            "username": username,
            "type": dialog.chat.type
        })
    
    i = 0
    for chat in chats:
        print("[{}] name: {} | id: {}".format(i+1, chat["username"], chat["id"]))
        i += 1
    
    idx = input("\nChoose a chat to delete messages from (index only): ")
    target = chats[int(idx)-1]
    
    if target["type"] in [ChatType.CHANNEL, ChatType.PRIVATE, ChatType.BOT]:
        print("Cannot delete messages from this channel, private chat or bot.")
        return
    
    chat_info = await app.get_chat(target["id"])
    chat_member = await app.get_chat_member(chat_info.id, user_id)
    
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        if chat_member.privileges.can_delete_messages:
            print("You have admin access and can delete messages. Proceeding...")
        else:
            print("You have admin access but cannot delete messages, thus cannot proceed")
            return
        
    else:
        print("You do not have admin access, thus cannot proceed...")
        return

    
    year = int(input("Enter the year from which you want to delete messages (20XX): "))
    month = int(input("Enter the month from which you want to delete messages (1-12): "))
    day = int(input("Enter the day from which you want to delete messages (1-30): "))
    target_date = datetime(year, month, day)
    newest_message_id = -1
    
    # get the latest message for a starting point
    async for message in app.get_chat_history(target["id"], limit=1):
        newest_message_id = message.id
        
    print(f"\nDeleting messages from {target['username']} from date {year}-{month}-{day} \n"
          "NOTE: the older the day the more time it will took to load the messages and delete it... \n\n")
    
    current_iterating_date = datetime.now()
    older_message_id = 0
    
    async for message in app.get_chat_history(target["id"]):
        message_date = datetime(message.date.year, message.date.month, message.date.day)
        if message_date != current_iterating_date:
            print(f"Currently scanning messages of date {current_iterating_date}.")   
            current_iterating_date = message_date
        
        # We reached the target date
        if message_date < target_date:
            print(f"Reached the date {target_date}.")
            older_message_id = message.id
            break
    
    # iterate in reverse order from newer messages to newest message (newer_message_id to older_message_id)
    for i in range(newest_message_id, older_message_id, -1):
        message = await app.get_messages(target["id"], i)
        text = str(message.text)[0:20] + "..."
        text = text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        print(f'Deleting message with text "{text}"')
        await app.delete_messages(target["id"], message.id)
        


if __name__ == "__main__":
    try:
        app = Client(
            name=f"sessions/{PHONE_NUMBER}",
            api_hash=API_HASH,
            api_id=API_ID,
            phone_number=PHONE_NUMBER
        )
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("Exiting...")
