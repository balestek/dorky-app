# Dorky

<p align="center">
  <img src="https://raw.githubusercontent.com/balestek/dorky-app/master/dorky/assets/images/dorky-logo.png">
</p>

[![PyPI version](https://badge.fury.io/py/dorky-app.svg)](https://badge.fury.io/py/dorky-app)
![Python minimum version](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/balestek/dorky-app.svg)](https://github.com/balestek/dorky/blob/master/LICENSE)

## 📝Intro
__Dorky__ is a lightweight OSINT companion tool that helps you run search engine "dorks" — those advanced queries — across a range of popular search engines. It’s not magic, but it does make your life easier by handling the dirty work of reformatting and opening light to medium dorks for you.

Try it online at: __[dorky.uk](https://dorky.uk)__.

<p align="center">
  <img src="https://raw.githubusercontent.com/balestek/dorky-app/master/dorky/assets/images/dorky-screenshot.png">
</p>

## ✨ Highlights

Here’s what __Dorky__ can do:

- ✅ Automatically convert Google and custom dorks for use with Google, Bing, Yandex, DuckDuckGo, Brave, and Baidu — all in one click.  
- ✅ Instantly open the results in your browser for any selected engine.  
- ✅ Firefox extension for easier access and quicker usage.

Under the hood, __Dorky__ maps or approximates compatible search operators using URL tweaking.

### ☰ Supported Operators
#### Google style
- " "
- ( )
- OR, |
- \-
- site:
- inurl:
- intitle:
- intext:
- filetype:, ext:
- \*
- after:
- before:
#### Custom
- lang:
- country:
- sub:
- last:
- !IP

The full list of supported operators and their compatibility can be found at __[dorky.uk](https://dorky.uk)__.

## 🛠️ Installation

### 🔹 pipx  (recommended)

Install with pipx:

```bash
pipx install dorky-app
```

Run __Dorky__ with pipx without installing it:

```bash
pipx run dorky-app [arguments]
```

### 🔹 uv (also recommended)

Install with uv:

```bash

uv tool install dorky-app
```

Run __Dorky__ with uv without installing it:

```bash
uvx dorky-app [arguments]
```

### 🔹 pip

```bash
pip install dorky-app
```

## 🚀 Getting Started

### ▶️ Start the Web App

By default, __Dorky__ runs on port 8080. Launch it like this:

```bash
dorky-app start
```

### ⚙️ Change the Port if needed

Use --port or -p to pick a different port:

```bash
dorky-app start --port 8083
# or shorthand
dorky-app start -p 8083
```

### 🔐 Set the Secret Key

To store user preferences securely (like selected engines and view states), set a `DORKY_SECRET` environment variable. If this isn’t set, your preferences reset every time you restart.

### 🐳 Using Docker?

Fire up __Dorky__ with Docker like so:

```bash 
docker run -p 8080:8080 -e DORKY_SECRET="your secret" balestek/dorky-app # start dorky on port 8080
docker run -p 8083:8080 -e DORKY_SECRET="your secret" balestek/dorky-app # start dorky on port 8083
```

## ⚡ Using Dorky

Visit your local __Dorky__ instance:

- http://127.0.0.1:8080
- http://localhost:8080

#### Step-by-step

1. Allow pop-ups for __Dorky__ domain in your browser settings.
2. Click to enable the search engines you want to use.
3. Type your query or paste in your dork.
4. Hit Enter or click the search button.

### 🧩 Firefox Add on

<p align="center">
  <img src="https://raw.githubusercontent.com/balestek/dorky-app/master/dorky/assets/images/dorky-addon-popup.png">
</p>

Want to use __Dorky__ directly in your browser?

🔗 [Get the Add-on](https://addons.mozilla.org/en-US/firefox/addon/dorky/)

🔗 [Source on GitHub](https://github.com/balestek/dorky-addon)

It aims to provide a seamless experience, allowing you to run __Dorky__ directly from your browser without needing to open the web app separately.

It’s already configured to work out of the box with the [dorky.uk](https://dorky.uk) instance, but you can also point it to your own self-hosted instance of __Dorky__ if needed.

#### Step-by-step

1. Install the add on.
2. Click on the add on icon and select the search engines you need.
3. (Optional) Set the __Dorky__ URL in _Advanced settings_ if you are using a self-hosted instance.
4. In the firefox omnibox (the address bar), type `!d` followed by your query or dork. For example: `!d osint site:github.com`.
5. Click on _Search_.

## ✔️ Requirements

Python version 3.9 or higher is required.
```
nicegui
```

## 📄 License
GPLv3
