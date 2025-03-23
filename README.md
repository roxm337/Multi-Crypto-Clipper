# Multi-Crypto Clipper & C2 Server 

![GitHub](https://img.shields.io/badge/license-MIT-blue)
![GitHub](https://img.shields.io/badge/python-3.8%2B-green)

This project is a **simulation** of a multi-cryptocurrency clipper malware and a Command and Control (C2) server, designed for **educational purposes only**. It demonstrates how clipboard monitoring and C2 communication can be exploited by malicious actors, helping cybersecurity professionals understand and defend against such threats.

---

## Disclaimer
This project is intended for **educational use only**. Do not use this software for any illegal or unethical purposes. Always ensure you have explicit permission before testing any systems. The creators of this project are not responsible for any misuse of this software.

---

## Features
- **Clipboard Monitoring**: Detects cryptocurrency addresses for BTC, ETH, USDT (ERC-20 and TRC-20), and BNB.
- **Address Replacement**: Replaces detected addresses with predefined addresses.
- **C2 Communication**: Sends detected addresses to a C2 server for logging.
- **Basic Persistence**: Adds itself to the Windows registry for startup.

---

## How It Works
1. **Multi-Crypto Clipper**:
   - Monitors the clipboard for cryptocurrency addresses.
   - Replaces detected addresses with predefined addresses.
   - Sends the original addresses to the C2 server.

2. **C2 Server**:
   - Listens for incoming connections from the clipper.
   - Logs received cryptocurrency addresses to a file (`crypto_addresses.log`).

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/roxm337/Multi-Crypto-Clipper.git
   cd Multi-Crypto-Clipper
```

 ## Usage

    Start the C2 server on your machine.

    Run the Multi-Crypto Clipper on the target machine (ensure you have permission).

    The C2 server will log any detected cryptocurrency addresses.
