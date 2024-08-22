import discord

TOKEN = ''
CHANNEL_ID = 1240697291321380987

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f'Không Thể Tìm Thấy Channel ID {CHANNEL_ID}')
        await client.close()
        return

    messages = []
    last_message_id = None

    try:
        while True:
            if last_message_id:
                history = channel.history(limit=8000, before=last_message_id)
            else:
                history = channel.history(limit=8000)
            
            fetched_messages = [msg async for msg in history]
            
            if not fetched_messages:
                break

            messages.extend(fetched_messages)
            last_message_id = fetched_messages[-1].id

            print(f'Fetched {len(fetched_messages)} messages')

    except Exception as e:
        print(f'Error retrieving messages: {e}')

    try:
        with open('messages.txt', 'w', encoding='utf-8') as f:
            for msg in reversed(messages):
                # Viết tên người dùng và tin nhắn vào file
                f.write(f'**{msg.author.display_name}**\n{msg.content}\n\n')
        print(f'Successfully saved {len(messages)} messages to messages.txt')
    except Exception as e:
        print(f'Error writing to file: {e}')
    
    await client.close()

client.run(TOKEN)
