# Table of contens
[🚀 Fast Install 🚀](https://github.com/AlexeyVolovinin/pinterest-bulk-upload#-fast-install)

# Pinterest Bulk Pin Uploader | Scheduler | Automated Pin Publishing Tool
⚠️ I encountered **pinterest bulk upload pins error**. I spent a long time figuring it out and getting various errors. When I finally **get success message, pins weren't published**. And in my application solved:
- ✅ Fixes **bulk upload errors** (pinterest bulk pins upload failed) 
	- Not the practicality of .csv files
	- Pins are not published, although there is a message about a successful public
- ✅ Add **free pin scheduling**. Built with **Selenium** for reliable browser automation.

---
## 🔧 Key Problems with Pinterest Bulk Uploader
1. 🛑**CSV Format Errors** and 🚨**False Success Notifications**: Pins fail to publish despite "success" status.
2. 🗓️**No Built-In Scheduler**: Lack of delayed posting functionality.

---

## ✅ Solution: Features
- **JSON/CSV Support**: Upload files from device or generate JSON pin data.
- **Selenium Authentication**: Full browser simulation for Pinterest login.
- **Free Scheduling**: Set custom dates/times for pin publication.

---

## 🚀 How to Use
### ⚡ Fast install
```bash
git clone https://github.com/maximedrn/pinterest-automatic-upload.git
cd pinterest-automatic-upload
pip install -r requirements.txt
```
### 🌐 Clone app
```bash
git clone https://github.com/maximedrn/pinterest-automatic-upload.git
cd pinterest-automatic-upload
```
### 🌐 Install requirements
```bash
pip install -r requirements.txt
```
### ⚙️ Install chrome driver
- [Driver](https://googlechromelabs.github.io/chrome-for-testing/)
- You **don't need spicify chrome executable, app do this automaticly**
### 📑 Requirements
- Python >3.7
- Chromium based browser: Brave, Chrome, Chromium is supported
### 🏁 Run
```bash
python main.py
```
or 
```bash
python3 main.py
```
#### First use
```bash
> What is your Pinterest email? ...enter {your email}
> What is your Pinterest password? ...enter {your password}
```
### 📤 How to upload
When you start app you will see:
```
Choose your file:
0 - Browse a file on PC.
1 - /home/user/pinterest/publish/list_pins.json
File number: 
```
Select 0 for finding files on PC and 1 for selecting pins from list_pins.json
### 🗃️ Using list_pins.json
```python
{
  "pin": [
    {
      "pinboard": "Coloring Pages!",
      "file_path": "/home/user/Pictures/pin.jpg",
      "title": "Wallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adults",
      "description": "Wallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adultsWallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adults. Flower",
      "alt_text": "Wallpapers and posters COLORING BOOKS",
      "link": "https://ru.pinterest.com/atomacssowtware/coloring-pages/",
      "date": ""
    },
  ]
}
```

| Field       | Limitations, symbols | Necessity | Example                                                                                                                                                                                                          |
| :---------- | :------------------: | :-------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| file_path   |          -           | required  | /home/user/Pictures/pin.jpg                                                                                                                                                                                      |
| pinboard    |          -           | required  | Coloring Pages!                                                                                                                                                                                                  |
| title       |      up to 100       | required  | Wallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adults                                                                                                             |
| description |      up to 500       | required  | Wallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adultsWallpapers and posters COLORING BOOKS for children and adults. Coloring book for children and adults. Flower |
| alt_text    |      up to 500       |     -     | Wallpapers and posters COLORING BOOKS                                                                                                                                                                            |
| link        |          -           |     -     | https://ru.pinterest.com/atomacssowtware/coloring-pages/                                                                                                                                                         |
| date        |          -           |     -     | 01/01/2025 12:00, 01/01/2025 12:00 or ""                                                                                                                                                                         |
# 💯🚀🎯 You are done
Developed by AlexeyVolovinin

[Github AlexeyVolovinin](https://github.com/AlexeyVolovinin)

[Pinterest AlexeyVolovinin](https://de.pinterest.com/atomacssowtware/)

[Support author on Pinterest](http://sites.google.com/view/color-mosaic-coloring-pages/%D1%85%D0%B0%D1%82%D0%BD%D1%8F%D1%8F-%D1%81%D1%82%D0%B0%D1%80%D0%BE%D0%BD%D0%BA%D0%B0)

# Plans
- Free AI Pins Generator
- Pins Creator tool
- WebUI
- Publishing Sheduler
