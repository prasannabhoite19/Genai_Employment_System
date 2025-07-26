**GenAI Employment System**  
An end-to-end AI-powered platform designed to assist job seekers by leveraging generative AI technologies like GPT, web scraping tools, and NLP models. The system can extract job-related data from LinkedIn, recommend courses, and provide overview about hiring company.

🚀 Features
  🔍 LinkedIn Job Scraper: Automatically gathers job postings from LinkedIn.
  
  🧹 Data Cleaner: Processes and structures scraped data for optimal use.
  
  💬 GPT Summarizer: Provides information about hiring company using GPT and NLP.
  
  📚 Course Recommendation Engine: Recommends courses to upgrade your skill using scraped course data.
  
  🔗 Integration with GPT APIs: For Summary generation and content assistance.

🧱 Project Structure
  Genai_Employment_System/
  │
  ├── app.py                   # Main application entry point
  ├── chatbot_main.py          # To understand how it work without gpt
  ├── .env                     # Environment variables (e.g., API keys)
  ├── requirements.txt         # Python dependencies
  ├── README.md                # Documentation file
  │
  ├── src/
  │   ├── chatbot_nlp.py       # NLP logic for chatbot interactions
  │   ├── course_scraper.py    # Web scraper for courses
  │   ├── gpt_helper.py        # GPT API helper functions
  │   ├── gpt_nlp.py           # GPT-based NLP logic
  │   ├── linkedin_cleaner.py  # Cleans and preprocesses LinkedIn data
  │   ├── linkedin_scraper.py  # Scrapes job listings from LinkedIn
  │   └── __init__.py
  │
  └── data/                    # Folder for storing scraped and processed data

🛠️ Installation

  1. Clone the Repository
     git clone https://github.com/prasannabhoite19/Genai_Employment_System.git
     cd Genai_Employment_System

  2. Create and Activate Virtual Environment (Optional but recommended)
     python -m venv venv
     source venv/bin/activate  # For Windows: venv\Scripts\activate

  3. Install Dependencies
     pip install -r requirements.txt

  4. Download spaCy Language Model
     python -m spacy download en_core_web_sm
     
  5. Set Up Environment Variables
     Create a .env file in the root directory with required API keys, e.g.:
     OPENAI_API_KEY=your_openai_key

▶️ Running the Project
  1. Run Main App
     streamlit run app.py

🤖 Usage
  Input your query about job title job location.

  GPT gives overview about the company.
  
  The scraper pulls recent jobs from LinkedIn based on user input.
  
  Course recommendations are made based on skills required for job.

📦 Dependencies
Key libraries used:

  spaCy
  
  openai
  
  requests
  
  beautifulsoup4
  
  selenium
  
  python-dotenv

See requirements.txt for full list.

🤝 Contributing
Feel free to fork the repo and submit pull requests. For major changes, please open an issue first to discuss what you’d like to change.

📄 License
This project is open source and available under the MIT License.
