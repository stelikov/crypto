from telethon import TelegramClient, events, Button
import logging
import asyncio
import aiohttp
from io import BytesIO
import re
import os
import deepl
import uuid
import time
import requests


# API - su default reikšmėmis jei env nėra
api_id = int(os.getenv('API_ID', '22290621'))
api_hash = os.getenv('API_HASH', '2290fc267cd636f39191a636c148ab3d')
bot_token = os.getenv('BOT_TOKEN', '7519656806:AAGIS_ijaxjI3qeXq2qPwuydLYJqhzk_-gM')
botas_tokenas_2 = os.getenv('BOTAS_TOKENAS_2', '7569012471:AAG-IttpKVFvcF0P9XBYqmeH6J-xWxREz1U')

API_KEY = os.getenv('API_KEY', 'MDUq5ee0mO24P8exbsSHG3vQZPhjRg4M1qWCShGLE35zLvpqza3DmYEGv4XMJEBO')

# PRIDĖKITE ŠIUOS ENVIRONMENT VARIABLES
PHONE_NUMBER = os.getenv('PHONE_NUMBER') # Jūsų telefono numeris su šalies kodu, pvz: +37060000000
PHONE_NUMBER = '+37067201903'
  
PASSWORD = os.getenv('PASSWORD', '')  # Jūsų Telegram passcode (jei turite)
#user_session_string = os.getenv('USER_SESSION')
user_session_string ="1BJWap1wBu7YD-jpRhhe6xirprZHTxqSY9lu2zaLJKg29kIJ5NN03ylPO8w-vrBa1fkCtG_3ino1qwt-5zoMurlPafgdZzU_q5FKjuHxvf3x-1vxSots8Q_UuONbPUSm5EftZvqIQigqnv7lMaqs6RpEK7gMX7PR4Hyc-Dpc2uK1sA1yl0NgoqLNSbBbglU3lD9S121RhFqbW8Bc5kgB9KGMekPd-8jC-rBVNBD8KFajkWgAH1oftbNMFqd4DWyFf4wE5xXUTzrjRJJvE5Avi9SlZKTcoS51xsO4JbVp5ZgFCKBRhYL2vXoaKuZzU8pJkWM1rwgDtxSDi3zW6UuKbuV1utPgLCwU="

# Grupiu ID / Topics / Kanalai
group_id = -1002521359437
second_group_id = -1002703463920
topics = {
    'crypto': 7,
    'General': 1
}

second_topics = {
    'rsialerts'       : 2,
    'liquidity'       : 4,
    'coinlisting'     : 6,
    'rsialertsmore'   : 8,
  #  'whalealerts'     : 40547,
  #  'pumpalerts'      : 40550,
  #  'openinalerts'    : 40553,
}

second_channels = {
 #   '@Binance_New_Listing_Delisting'         : ['coinlisting'],
 #   '@Bybit_New_Listings'                    : ['coinlisting'],
 #   '@binance_delisting'                     : ['coinlisting'],
 #   '@mrDRSIAlert'                           : ['rsialerts'],
 #   '@CycloneRSI'                            : ['rsialerts'],
 #   '@yoyodexrsi'                            : ['rsialertsmore'],
 #   '@cointrendz_whalehunter'               : ['whalealerts'],
 #   '@cointrendz_pumpdetector'               : ['pumpalerts'],
    '@OpenInterest_Alert'                    : ['liquidity'],
}

channels = {
    '@Insider_leak_of_theday'   : ['crypto'], 
    -1001685592361              : ['crypto'],
    '@FinancialWorldUpdates'    : ['crypto'], 
    '@Cryptocurrency_Inside'    : ['crypto'], 
    '@coingape'                 : ['crypto'],
    '@cointelegraph'            : ['crypto'],
    '@cbinsider'                : ['crypto'],
    '@forex_factory_news'       : ['forex'],
    '@ForexCalendar'            : ['forex'],
    '@CryptoKingMarketAnalysis' : ['crypto'],
    '@BlueBisonCrypto'          : ['crypto'],
    '@TokenHunters_TH'          : ['crypto'],
    '@KlondikeAI'               : ['crypto'],
    '@TradingViewAllIdeas'      : ['crypto'],
    '@worldofchartsfx'          : ['crypto'],
    '@WiseAnalyze'              : ['crypto'],
    '@CryptoHolicss'            : ['crypto'],
    '@thecryptoexpress'         : ['crypto'],
    '@BlockchainClowns'         : ['crypto'],
    '@Always_Win_Premium'       : ['signals'],
    '@BinanceKillersVipOfficial': ['signals'],
}

# Logu Failas
log_file = "bot_logs.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file, encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)
# PATAISYTAS KLIENTŲ STARTUP SU SESSION STRING
# Jei turite session string, naudokite jį, kitu atveju naudokite failą
if user_session_string:
    from telethon.sessions import StringSession
    user_client = TelegramClient(StringSession(user_session_string), api_id, api_hash)
else:
    user_client = TelegramClient('user_session', api_id, api_hash)

bot_client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
botas_client_2 = TelegramClient('bot_session_2', api_id, api_hash).start(bot_token=botas_tokenas_2)

# Vertimas
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY', 'a19d53c3-b287-47a8-972a-e9e0b6105f0e:fx')
translator = deepl.Translator(DEEPL_API_KEY)

skip_translation_keywords = [
    "Bullish", "Bearish", "Coin", "Crypto Currency", "BlockChain", "Bitcoin", "Ethereum", 
    "AltCoin", "Nft", "DeFi", "AirDrop", "Token", "Mining", "Wallet", "Stablecoin", "Fork", 
    "Inverse", "Head", "Shoulders", "Pattern", "Bull Run", "Support zone", "resistance zone", 
    "flag", "Pennant", "LATOKEN", "KuCoin", "$", "K", "Breakout", "Convergence", "Falling Wedge", 
    "Pumps", "pump", "Total", "ETH", "MArket Cap", "Dominance", "Market Overview", "dump", "dumps",
    "Long", "Short",
]

blacklisted_symbols = {
    "ZEUS", "L3", "KAIA", "SNT", "1000X", "MNT", "10000LADYS", "MOCA", "MRL", "1000NEIROCTO", "S",
    "TRB"
}

def remove_formatting_tags(text):
    return re.sub(r'<.*?>|\x1B[@-_][0-?]*[ -/]*[@-~]', '', text)

async def translate_to_lithuanian(text):
    text = remove_formatting_tags(text)
    
    placeholders = {f"__PLACEHOLDER_{i}__": keyword for i, keyword in enumerate(skip_translation_keywords)}
    
    for placeholder, keyword in placeholders.items():
        text = re.sub(r'\b' + re.escape(keyword) + r'\b', placeholder, text, flags=re.IGNORECASE)
    
    translated = translator.translate_text(text, target_lang="LT")
    
    for placeholder, keyword in placeholders.items():
        translated.text = translated.text.replace(placeholder, keyword)
    
    return translated.text

def replace_group_names(text):
    replacements = {
        r'@[\w]+': '@CryptoImperija',
        "🤖 All Free Signal Bots": "@CryptoImperija",
        r'💥 Add bot to your Groups.*\n?': '',
        r'👉 Signals.*\n?': '',
        r'💥 Market Analysis*\n?': '',
        r'👉 Check live RSI.*': '@CryptoImperija',
        r'👉 RSI Pullback Signals.*': '@CryptoImperija',
        r'👉 RSI Heatmap*': '@CryptoImperija',
        r'💥 Market Analysis Bot*\n?': '',
        r'🔃 Auto fetch custom ideas 💡': '',
        r'🛍️ MevX🤑   STB🤖   BL🌸   TROJ🐎': '',
        r'Bot': '',
        r'Binance | TV': '',
        r'🛍️ AVE🌠   MevX🤑   SM☯️   MAE🥷': '',
        r'🔃 Auto-fetch ideas 💡': '',
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text

def is_promotional_message(text):
    promotional_keywords = [
        "nuolaidas", "narystė", "discounts", "membership", "nemokamas vip", "pasiūlymas", "parduoti", 
        "susisiekite", "akcija", "specialus", "priklauso", "užsakyti", "gauti", "tik šiandien", 
        "nepraleiskite", "PAID", "Group", "Quickly", "JOIN QUICKLY", "FREE VIP", "Nemokamas VIP", 
        "greitai", "paskubėkite prisijunkite", "cashback service", "#Sponsored", "VIP service",
        "VIP", "Service", "service", "signing up", "my link!", "important", "Stay safe Killers!"
    ]
    return any(keyword.lower() in text.lower() for keyword in promotional_keywords)

async def send_message_to_topics(text=None, photo=None, topic_names=None):
    topic_names = topic_names or ['main']
    for topic_name in topic_names:
        topic_id = topics.get(topic_name)
        if topic_id:
            try:
                if topic_name == "coin":
                    text = f"{text}\n\n⚠️ Nefinansinis Patarimas"
                if topic_name == "signals":
                    text = f"{text}\n\n⚠️ Nefinansinis Patarimas"
                    
                formatted_text = f"\n{text}"
                if photo:
                    await bot_client.send_file(group_id, photo, caption=formatted_text, reply_to=topic_id)
                else:
                    await bot_client.send_message(group_id, formatted_text, reply_to=topic_id)
            except Exception as e:
                error_message = f"Klaida siunčiant į temą {topic_name}: {e}"
                logger.error(error_message)
            finally:
                if photo and os.path.exists(photo):
                    os.remove(photo)

@user_client.on(events.NewMessage(chats=list(channels.keys())))
async def message_handler(event):
    try:
        message_text, media = event.message.message, event.message.media
        channel_name = f"@{event.chat.username}" if event.chat.username else event.chat.title or str(event.chat_id)
        if not message_text and not media:
            return
        message_text = replace_group_names(message_text)
        if is_promotional_message(message_text):
            return
        topic_names = channels.get(channel_name, ['main'])
        if media:
            photo = await event.message.download_media()
            await send_message_to_topics(text=message_text, photo=photo, topic_names=topic_names)
        else:
            await send_message_to_topics(text=message_text, topic_names=topic_names)
    except Exception as e:
        error_message = f"Klaida apdorojant pranešimą iš {event.chat.title or event.chat.username}: {e}"
        logger.error(error_message)

async def send_message_to_second_topics(text=None, photo=None, topic_names=None, buttons=None):
    topic_names = topic_names or ['liquidity']
    for topic_name in topic_names:
        topic_id = second_topics.get(topic_name)
        if topic_id:
            try:
                formatted_text = f"\n{text}"
                if photo:
                    await botas_client_2.send_file(second_group_id, photo, buttons=buttons, caption=formatted_text, reply_to=topic_id)
                else:
                    await botas_client_2.send_message(second_group_id, formatted_text, buttons=buttons, reply_to=topic_id)
            except Exception as e:
                error_message = f"Klaida siunčiant į temą {topic_name}: {e}"
                logger.error(error_message)
            finally:
                if photo and os.path.exists(photo):
                    os.remove(photo)

# Sentiment analysis functions (unchanged)
async def get_sentiment_percentages(symbol, session):
    intervals = ["5m", "15m", "30m", "1h"]
    sentiment_data = {}
    
    headers = {
        "X-MBX-APIKEY": API_KEY 
    }

    tasks = []
    
    symbol_mapping = {
        "1000TURBO": "TURBO",
        "SHIB1000": "1000SHIB",
        "DOGEUSD": "DOGE",
        "BTCUSD": "BTC",
        "ETHUSD": "ETH",
        "XRPUSD": "XRP",
        "10000SATS": "1000SATS",
        "LTCUSD": "LTC",
        "SOLUSD": "SOL"
    }
    
    symbol = symbol_mapping.get(symbol, symbol)
    logger.info(f"Fetching sentiment data for symbol: {symbol}")
    
    for interval in intervals:
        url = f"https://fapi.binance.com/futures/data/globalLongShortAccountRatio?symbol={symbol}USDT&period={interval}"
        tasks.append(fetch_data(url, session, interval, sentiment_data))
    
    await asyncio.gather(*tasks)
    
    logger.info(f"Sentiment data fetched: {sentiment_data}")
    return sentiment_data

async def fetch_data(url, session, interval, sentiment_data):
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data:
                long_account = float(data[0]["longAccount"])
                short_account = float(data[0]["shortAccount"])
                
                bullish_percent = long_account * 100
                bearish_percent = short_account * 100
                
                long_short_ratio = float(data[0]["longShortRatio"])
                if long_short_ratio > 1:
                    bullish_percent = (long_short_ratio / (long_short_ratio + 1)) * 100
                    bearish_percent = 100 - bullish_percent
                elif long_short_ratio < 1:
                    bearish_percent = (1 / (long_short_ratio + 1)) * 100
                    bullish_percent = 100 - bearish_percent
                
                bullish_percent = max(min(bullish_percent, 100), 0)
                bearish_percent = max(min(bearish_percent, 100), 0)
                
                sentiment_data[interval] = (round(bullish_percent, 2), round(bearish_percent, 2))
                logger.info(f"Sentiment for interval {interval}: Bullish {bullish_percent}%, Bearish {bearish_percent}%")
            else:
                sentiment_data[interval] = (0.0, 0.0)
                logger.info(f"No sentiment data for interval {interval}, setting to 0.0, 0.0")
        else:
            sentiment_data[interval] = (0.0, 0.0)  
            logger.error(f"Error fetching data for {url}: Status {response.status}")

async def get_price_change(symbol, session, interval):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}USDT&interval={interval}&limit=2"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            open_price = float(data[0][1])  
            close_price = float(data[1][4]) 
            
            price_change = ((close_price - open_price) / open_price) * 100
            logger.info(f"Price change for {symbol} over {interval}: {price_change}%")
            return price_change
        logger.error(f"Error fetching price change for {symbol}: Status {response.status}")
        return 0

async def get_trading_volume(symbol, session):
    url = f"https://fapi.binance.com/fapi/v1/ticker/24hr?symbol={symbol}USDT"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            volume = float(data["volume"]) 
            logger.info(f"Trading volume for {symbol}: {volume}")
            return volume
        logger.error(f"Error fetching trading volume for {symbol}: Status {response.status}")
        return 0

def format_sentiment_message(sentiment_data):
    intervals_order = ["5m", "15m", "30m", "1h"]
    
    sentiment_message = "\n".join(
        f"`{interval:5} : 📈 {bullish:.2f}% / 📉 {bearish:.2f}%`"
        for interval, (bullish, bearish) in ((i, sentiment_data.get(i, (0, 0))) for i in intervals_order)
    )
    logger.info(f"Formatted sentiment message: {sentiment_message}")
    return sentiment_message

@user_client.on(events.NewMessage(chats=['@BinanceLiquidations', '@BybitLiquidations']))
async def liquidation_handler(event):
    start_time = time.time()

    text, source_chat = event.message.message, event.chat.username
    symbol_prefix = "BINANCE" if source_chat == "BinanceLiquidations" else "BybitLiquidations"

    currency = re.search(r"#([A-Z0-9]+)", text)
    currency = currency.group(1) if currency else "Test"
    logger.info(f"Currency extracted: {currency}")

    if currency in blacklisted_symbols:
        logger.info(f"Symbol {currency} is blacklisted. Skipping message.")
        return 

    liq_type = re.search(r"Liquidated (Long|Short)", text)
    liq_type = liq_type.group(1) if liq_type else "Test"

    qty = re.search(r"\$(\d+(?:\.\d+)?K?)", text)
    qty = qty.group(1) if qty else "Test"

    price = re.search(r"at \$(\d+(?:\.\d+)?)", text)
    price = price.group(1) if price else "Test"

    async with aiohttp.ClientSession() as session:
        sentiment_data = await get_sentiment_percentages(currency, session)
        price_change = await get_price_change(currency, session, "5m")
        volume = await get_trading_volume(currency, session)

        sentiment_message = format_sentiment_message(sentiment_data)

        formatted_message = (
            f"🔥 Liquidation Alert! 🔥\n"
            f"{'🔴' if liq_type == 'Long' else '🟢'} Symbol: #{currency}\n"
            f"💰 Quantity: {qty}\n"
            f"💵 Price: {price}\n"
            f"⚠️ Type: {liq_type}\n\n"
            f"`📊 Sentiment:`\n{sentiment_message}"
        )

        button_bybit = Button.url("Bybit Chart", f"https://www.tradingview.com/chart/?symbol=BYBIT:{currency}USDT.P")
        button_bybit_exchange = Button.url("Bybit Exchange", f"https://www.bybit.com/trade/usdt/{currency}USDT")
        buttons = [[button_bybit, button_bybit_exchange]]
        
        await send_message_to_second_topics(formatted_message, buttons=buttons)

    end_time = time.time()
    logger.info(f"Pranešimo apdorojimas truko {end_time - start_time:.2f} sekundes.")

@user_client.on(events.NewMessage(chats=list(second_channels.keys())))
async def second_handler(event):
    try:
        message_text, media = event.message.message, event.message.media
        channel_name = f"@{event.chat.username}" if event.chat.username else event.chat.title or str(event.chat_id)
        if not message_text and not media:
            return

        message_text = replace_group_names(message_text)
        if is_promotional_message(message_text):
            return

        topic_names = second_channels.get(channel_name, ['liquidity'])

        if 'rsialerts' in topic_names:
            translated_message = message_text  
        else:
             translated_message = message_text

        if media:
            photo = await event.message.download_media()
            await send_message_to_second_topics(text=translated_message, photo=photo, topic_names=topic_names)
        else:
            await send_message_to_second_topics(text=translated_message, topic_names=topic_names)
    except Exception as e:
        error_message = f"Klaida apdorojant pranešimą iš {event.chat.title or event.chat.username}: {e}"
        logger.error(error_message)

async def keep_alive():
    while True:
        try:
            await user_client.send_message('me', '🔄 Laikau botą aktyvų...')
            await asyncio.sleep(900)  
        except Exception as e:
            logger.error(f"Klaida bandant išlaikyti aktyvumą: {e}")
            try:
                await user_client.connect()
                if not await user_client.is_user_authorized():
                    # PROGRAMINIS AUTENTIFIKAVIMAS
                    if PHONE_NUMBER:
                        await user_client.start(phone=PHONE_NUMBER, password=PASSWORD)
                    else:
                        logger.error("PHONE_NUMBER environment variable not set!")
                        return
                logger.info("Sėkmingai iš naujo prisijungta prie Telegram.")
            except Exception as e:
                logger.error(f"Nepavyko prisijungti iš naujo: {e}")




# PATAISYTA MAIN FUNKCIJA SU SESSION STRING PALAIKYMU
async def main():
    try:
        # Prisijungiame prie user_client
        await user_client.connect()
        
        # Jei naudojame session string, jis jau turėtų būti autentifikuotas
        if user_session_string:
            logger.info("Using session string for authentication")
            # Tikriname ar sesija veikia
            if not await user_client.is_user_authorized():
                logger.error("Session string is invalid or expired!")
                return
        else:
            # Senas metodas - reikalingas tik jei nėra session string
            if not await user_client.is_user_authorized():
                if not PHONE_NUMBER:
                    logger.error("PHONE_NUMBER environment variable not set! Please set it to your phone number with country code (e.g., +37060000000)")
                    return
                
                try:
                    # Siunčiame autentifikavimo kodą
                    logger.info(f"Sending authentication code to {PHONE_NUMBER}")
                    await user_client.send_code_request(PHONE_NUMBER)
                    
                    # Čia reikės interaktyviai įvesti kodą arba naudoti iš anksto žinomą kodą
                    # Deployment aplinkoje geriau naudoti jau sukurtą session string
                    logger.error("Authentication code required. Please authenticate locally first to create session string, then set USER_SESSION environment variable.")
                    return
                    
                except Exception as e:
                    logger.error(f"Authentication failed: {e}")
                    return
        
        # Paleidžiame visus klientus
        await asyncio.gather(
            bot_client.start(), 
            botas_client_2.start(),
        )
        print("sadsa")
        asyncio.create_task(keep_alive())
        logger.info("Visi bot'ai paleisti ir veikia.")
        await user_client.run_until_disconnected()
        
    except Exception as e:
        error_message = f"Klaida paleidžiant bot'us: {e}"
        logger.error(error_message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())