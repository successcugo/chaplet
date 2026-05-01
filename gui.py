import streamlit as st
import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

st.set_page_config(page_title="Trading Signal Generator Manager", layout="wide")

st.title("📈 Signal Generator Manager")

config = load_config()

if config:
    st.sidebar.header("General Settings")
    freq = st.sidebar.number_input("Check Frequency (Minutes)", min_value=1, value=config.get('check_frequency_minutes', 5))
    ratio = st.sidebar.number_input("TP/SL Ratio", min_value=0.1, value=config.get('tp_sl_ratio', 2.0))
    provider = st.sidebar.selectbox("Data Provider", ["tradingview-ta", "tvdatafeed"], index=0 if config.get('data_provider') == "tradingview-ta" else 1)

    config['check_frequency_minutes'] = freq
    config['tp_sl_ratio'] = ratio
    config['data_provider'] = provider

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Telegram Configuration")
        token = st.text_input("Bot Token", value=config['telegram']['token'], type="password")
        chat_id = st.text_input("Chat ID", value=config['telegram']['chat_id'])
        config['telegram']['token'] = token
        config['telegram']['chat_id'] = chat_id

    with col2:
        st.subheader("Strategies")
        for strat_name, params in config['strategies'].items():
            enabled = st.checkbox(f"Enable {strat_name.replace('_', ' ').title()}", value=params['enabled'])
            params['enabled'] = enabled
            # Simple parameter editing (could be more detailed)
            if enabled:
                st.write(f"Parameters for {strat_name}: {params}")

    st.subheader("Tickers")
    # Display as a table or text area for simplicity
    tickers_json = st.text_area("Tickers JSON (Edit with caution)", value=json.dumps(config['tickers'], indent=4), height=300)
    try:
        config['tickers'] = json.loads(tickers_json)
    except:
        st.error("Invalid JSON in Tickers field")

    if st.button("Save Configuration"):
        save_config(config)
        st.success("Configuration saved! The generator will pick up changes on its next loop.")

    if st.button("Send Test Signal to Telegram"):
        from telegram_notifier import TelegramNotifier
        tg = TelegramNotifier(config['telegram']['token'], config['telegram']['chat_id'])
        res = tg.send_test_signal()
        if res:
            st.success("Test signal sent!")
        else:
            st.error("Failed to send test signal. Check logs and token.")

    st.divider()
    st.subheader("Logs")
    if os.path.exists("generator.log"):
        with open("generator.log", "r") as f:
            logs = f.readlines()
            st.text_area("Last 50 log lines", value="".join(logs[-50:]), height=300)
    else:
        st.info("No logs found yet.")
else:
    st.error("Configuration file not found.")
