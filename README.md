# 📡 SHanks SHare

**SHanks SHare** is a lightweight, offline file-sharing platform designed for seamless transfers over local Wi-Fi. Whether you're sharing documents, media, or code, this tool ensures instant delivery between devices — no internet required.

---

## 🚀 Features

- ⚡ Blazing-fast file transfers over local Wi-Fi
- 🌐 Web interface for easy access from any browser
- 💬 Built-in local chat system (optional)
- 🧾 Simple terminal-based logs for debugging
- 🔐 Private sharing through unique code pairing (optional)
- 📦 Cross-platform support — works on Linux, Windows, Android (via Termux), and more

---

## 📸 Terminal Screenshot



![term-SS](https://github.com/user-attachments/assets/66a9aa0a-7956-430e-9c86-f5a561b84ced)


---

## 🌐 Web Interface Screenshot



![SS-web](https://github.com/user-attachments/assets/eef73850-1b77-4585-af6c-e67710793a63)


---

## 🛠️ How It Works

1. One device starts the host server on the local Wi-Fi network.
2. Other devices connect using the server’s IP and port in a browser.
3. Files can be uploaded, listed, downloaded, and even chatted over the local network.

---

## 📦 How to Run

### 💻 On Desktop (Linux/Windows)

```bash
git clone https://github.com/yourusername/Shanks-Share.git
cd Shanks-Share
python3 app.py
