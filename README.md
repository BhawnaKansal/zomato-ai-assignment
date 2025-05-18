# 🍽️ Zomato RAG Chatbot

Ever wanted to ask natural questions like “What vegan dishes are available nearby?” or “Which restaurant has the spiciest starters?” and get clear answers—without digging through dozens of menus?

This project solves exactly that. It's an end-to-end AI-powered chatbot built using a **RAG (Retrieval-Augmented Generation)** setup. It scrapes real restaurant data from Swiggy, builds a searchable knowledge base, and runs a chatbot that combines search with language generation to give human-like answers.

Created as part of the **Zomato Gen AI Internship assignment**, but designed to be practical and extensible beyond the scope of the task.

---

## 🧠 Key Features

### 🔍 1. Web Scraping with Enrichment
- Scrapes restaurant metadata + detailed menu info from Swiggy’s internal APIs
- Tags each dish with dietary filters like **vegan**, **vegetarian**, and **spice level** (based on keyword analysis)
- Adds extras like closing time, cuisine type, and location
- Output is saved as a clean JSON file (`swiggy_data.json`)

### 📚 2. Knowledge Base
- Converts the scraped data into bite-sized documents
- Each restaurant and menu item becomes an individual document
- Optimized for semantic retrieval (used later in the RAG flow)

### 🤖 3. RAG Chatbot
- Uses `sentence-transformers` to find relevant info for a query
- Feeds that into `Flan-T5` (from Hugging Face) to generate natural responses

### 💬 4. Gradio UI
- Lightweight, clean interface using Gradio
- One-click deployable (no server or streamlit hassle)
- Lets users type queries and get contextual answers in a chatbot-style layout

---

## 🛠️ How to Use

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

> _(Tip: You’ll need `transformers`, `sentence-transformers`, `gradio`, `pandas`, `requests`, `tqdm`, etc.)_

### Step 2: Scrape data

```bash
python web_scraper.py --output swiggy_data.json
```

This script hits Swiggy APIs for 10 curated restaurants, processes the menus, and saves everything in a usable format.

### Step 3: Launch the chatbot

```bash
python main.py --input swiggy_data.json
```

A Gradio UI will open in your browser where you can chat with the bot.

---

## 🔍 Example Questions to Try

- _“What is the spice level of egg bhurji at Desi Tadka?”_
- _“Which restaurants serve Italian?”_
- _“What is the price of butter tawa roti at Olive”_

---

## 🎥 Demo Video

Want to see it in action before setting it up? Check out the short demo video below where we walk through scraping restaurant data, launching the chatbot, and interacting with it using real queries.

https://github.com/user-attachments/assets/dabfd610-bd3c-450c-89d2-38f7978cc8ab

---




## 📎 Notes & Limitations

- Swiggy’s API isn’t officially public, so scraping may break over time.
- Right now, everything runs in-memory—so it's not optimized for large-scale deployment yet.
- The chatbot doesn’t support follow-ups or multi-turn reasoning (yet), but that’s an area for future expansion.
- Data is localized to one region (for now) based on latitude/longitude used in the scraper config.

---

## 🧠 Behind the Scenes

**Retrieval**  
→ `SentenceTransformer` (MiniLM) finds top 5 matches for each user query  
**Generation**  
→ Prompt fed into `Flan-T5` with query + top results as context  
**UI**  
→ `Gradio` Blocks interface with input box, chat history, and output  
**Scripting**  
→ One Python script (`web_scraper.py`) handles API requests, formatting, cleaning, and tagging

---

## 🙋 About Me

**Bhawna Kansal**  
Loves building practical GenAI tools. Passionate about NLP, good UX, and making technical ideas easy to use.  
Find me on GitHub or feel free to reach out if you're working on something similar!

