# 🔍 Analysis of Women Safety in India Using Instagram Data

This project analyzes public sentiment regarding women's safety issues in India by analyzing Instagram comments using **Natural Language Processing (NLP)** techniques.  
It provides a simple **GUI using Tkinter** to:

- Visualize images
- Read Instagram comments from CSV files
- Clean the comments
- Perform sentiment analysis using **TextBlob**
- Display sentiment results using **Matplotlib charts**

---

## 📂 Project Structure
```plaintext

├── images/ 
├── Dataset/ 
├── women_safety_analysis.py
└── README.md
```
---

## 🚀 Features

- GUI interface using **Tkinter**
- Load and display category-specific images
- Read Instagram comments from CSV files
- Clean comments using basic NLP (stop words removal, punctuation removal)
- Sentiment analysis using **TextBlob** (Positive, Negative, Neutral classification)
- Visualize sentiment distribution using a **Pie Chart**
- Modular code structure for easy readability and maintenance

---

## 🛠️ Technologies Used

- **Python 3.x**
- **Tkinter** — for GUI development
- **Pandas** — for CSV data handling
- **TextBlob** — for sentiment analysis
- **NLTK** — for stop words removal
- **Pillow (PIL)** — for image processing
- **Matplotlib** — for data visualization

---
## 🔧Required libraries
```
pip install pandas textblob pillow matplotlib nltk
```
---

## Run the Python script
```
python women_safety_analysis.py
```
---

## Steps in the Application:
- Select a category (Rape, Stalking, etc.) from the dropdown.
- Load images related to the selected category.
- Read Instagram comments from the CSV file.
- Clean the comments using NLP.
- Analyze the comments' sentiment using TextBlob.
- View the sentiment distribution in a pie chart.

---

## Future Improvements
- Integrate more advanced sentiment analysis models (e.g., BERT, VADER)
- Add Instagram scraping functionality for real-time data
- Improve the user interface with modern frameworks like PyQt or Kivy
- Deploy as a web application using Flask or Django
  
---
## Author
Kavyashri Hebbar Manipal Institute of Technology, Manipal
