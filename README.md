# 💸 Roulette Split & Tracker

An AI-powered bill splitter and gamified expense tracker designed to end the "who owes what" debate with friends. Simply snap a picture of a receipt, claim your items, and spin the wheel of destiny to see who pays the penalty!

## ✨ Features

* **📸 Live Receipt Scanning:** Snap a picture using your mobile camera or upload an image directly from your device.
* **🧠 AI-Powered Extraction:** Utilizes Google's Gemini 2.5 Flash multimodal AI to instantly extract the store name, individual line items, and prices from crumpled or faded receipts.
* **✅ Smart Item Claiming:** Dynamically generates an interactive checklist. Friends tap the items they actually consumed to calculate their exact base share (automatically distributing untracked taxes and fees evenly).
* **🎰 Bill Roulette:** A high-suspense, gamified spin wheel. Select a penalty (e.g., 2x Share, 3x Share, or Fully Pay), spin the wheel, and the app calculates the mathematical redistribution of debts based on the loser's penalty.
* **💾 The Vault:** Permanently saves all calculated debts and splits to a secure cloud PostgreSQL database.
* **📊 Squad Dashboard:** A real-time analytics page tracking total squad spending, total money owed to individuals, and a "Hall of Bad Luck" highlighting who loses at Roulette the most.

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Database:** PostgreSQL (hosted on Supabase)
* **AI Engine:** Google Generative AI (`gemini-2.5-flash`)
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
* **Environment Management:** `python-dotenv`, `dj-database-url`

## 🚀 Local Setup & Installation

To run this project locally, you will need Python installed on your machine.

**1. Clone the repository**
```bash
git clone [https://github.com/nithish-ra/roulette-split.git](https://github.com/nithish-ra/roulette-split.git)
cd roulette-split
2. Create and activate a virtual environment

Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies

Bash
pip install django psycopg2-binary google-generativeai python-dotenv pillow dj-database-url
4. Set up environment variables
Create a .env file in the root directory (next to manage.py) and add your secure keys:

Code snippet
DATABASE_URL=postgresql://[user]:[password]@[supabase-url]:6543/postgres
GEMINI_API_KEY=your_google_gemini_api_key_here
5. Apply database migrations

Bash
python manage.py makemigrations
python manage.py migrate
6. Run the development server

Bash
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser to start splitting!

🗺️ Roadmap
Phase 1 (Completed): AI Extraction, Gamified Math Logic, Database Integration.

Phase 2 (Upcoming): User Authentication & Secure Logins for distinct friend groups.

Phase 3 (Upcoming): Cloud deployment to Render for public web access.

👨‍💻 Author
Nithish Ra


***

### A Quick GitHub Pro-Tip
Before you commit this README, it is highly recommended to quickly generate a `requirements.txt` file so anyone else who downloads your code knows exactly what Python packages to install. 

Just run this single command in your terminal while your virtual environment is active:
`pip freeze > requirements.txt`

Then, you can run your `git add .`, `git commit -m "Added README and requirements"`, and `git push` to send the final polish to your live repository. You crushed this build!
