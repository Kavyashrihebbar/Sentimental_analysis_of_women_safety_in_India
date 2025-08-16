import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import pandas as pd
from textblob import TextBlob
from string import punctuation
from nltk.corpus import stopwords
import threading
import matplotlib
matplotlib.use('TkAgg')                  # Initialize Matplotlib for use with Tkinter
import matplotlib.pyplot as plt

class LandingPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analysis of Women Safety in India Using Instagram Data")
        self.geometry("1000x300")  # Set window size
        self.configure(bg="#f0f0f0")  # Set background color

        # Title label
        self.label_title = tk.Label(self, text="Analysis of Women Safety in India Using Instagram Data", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.label_title.pack(pady=5)

        # Combobox for selecting analysis option
        self.label_choose_option = tk.Label(self, text="Select an option:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_choose_option.pack()
        
        self.combobox = ttk.Combobox(self, values=["Rape", "Stalking", "Sexual abuse", "Gender discrimination"], font=("Helvetica", 12))
        self.combobox.pack(pady=5)

        # Upload button
        self.upload_button = tk.Button(self, text="Load Image", command=self.display_images, font=("Helvetica", 12))
        self.upload_button.pack(pady=5)

        # Frame for displaying images
        self.grid_frame = tk.Frame(self, bg="#f0f0f0")
        self.grid_frame.pack(pady=5)

        # Analyze button
        self.upload_comment_button = tk.Button(self, text="Analyze Comments", command=self.open_analysis_program, font=("Helvetica", 12))
        self.upload_comment_button.pack(pady=5)

    def display_images(self):
        selected_value = self.combobox.get()
        if not selected_value:
            messagebox.showwarning("Warning", "Please select a value from the combobox.")
            return

        # Load images based on the selected value
        images = None  # Initialize images variable
        if selected_value == "Rape":
            images = [r"D:\project\image\Rape1.jpeg",r"D:\project\image\Rape5.jpg",r"D:\project\image\Rape3.jpeg",r"D:\project\image\Rape4.jpeg"]
        elif selected_value == "Stalking":
            images = [r"D:\project\image\stk1.jpg",r"D:\project\image\stk2.png",r"D:/project/image/stk3.jpg",r"D:\project\image\stk4.jpg"]
        elif selected_value == "Sexual abuse":
            images = [r"D:\project\image\sexual5.jpg",r"D:\project\image\sexual6.jpg",r"D:\project\image\sexual3.jpg",r"D:\project\image\sexual2.webp"]
        elif selected_value == "Gender discrimination":
            images = [r"D:\project\image\gender1.jpg",r"D:\project\image\gender2.jpg",r"D:\project\image\gender3.jpg",r"D:\project\image\gender4.jpg"]

        # Check if images were found
        if images is None:
            messagebox.showwarning("Warning", "No images found for the selected option.")
            return

        # Display loading circle icon
        loading_label = tk.Label(self.grid_frame, text="Loading...", font=("Helvetica", 12), bg="#f0f0f0")
        loading_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # After 10 seconds, hide the loading label and display images
        self.after(1000, lambda: self._display_images(images, loading_label))

    def _display_images(self, images, loading_label):
        # Clear previous images and loading label
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Display images in a 2x2 grid
        row = 0
        col = 0
        for img_path in images:
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.grid_frame, image=photo)
            label.image = photo
            label.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Destroy loading label
        loading_label.destroy()

    def open_analysis_program(self):
        selected_value = self.combobox.get()
        if not selected_value:
            messagebox.showwarning("Warning", "Please select a value from the combobox.")
            return

        # Associate combobox values with CSV files
        csv_files = {
            "Rape": "D:\project\Dataset\Rape.csv",
            "Stalking": "D:\project\Dataset\stalking.csv",
            "Sexual abuse": "D:\project\Dataset\sexual_abusee(1).csv",
            "Gender discrimination":"D:\project\Dataset\genderdiscrimination(1).csv"
        }

        # Check if the selected value is in the dictionary
        if selected_value in csv_files:
            # Run analysis
            self.run_analysis(selected_value, csv_files[selected_value])
        else:
            messagebox.showwarning("Warning", "Invalid selection")

    def run_analysis(self, selected_value, csv_file):
        # Create an instance of AnalysisProgram
        AnalysisProgram(selected_value, csv_file, self)
        
    def bring_to_front(self):
        self.lift()

class AnalysisProgram:
    def __init__(self, selected_value, csv_file, landing_page_instance):
        self.main = tk.Toplevel()  # Changed from tk.Tk() to tk.Toplevel()
        self.landing_page_instance = landing_page_instance
        self.main.title("Analysis of Women Safety in India Using Instagram Data")
        self.main.geometry("1000x1000")

        self.selected_value = selected_value
        self.filename = csv_file
        self.insta_list = []
        self.clean_list = []
        self.pos = 0
        self.neu = 0
        self.neg = 0

        self.font = ('times', 14, 'bold')
        self.title = tk.Label(self.main, text='Analysis of Women Safety in India Using Instagram Data')
        self.title.config(bg='antiquewhite', fg='black')
        self.title.config(font=self.font)
        self.title.config(height=3, width=130)
        self.title.place(x=0, y=5)

        self.home_button = tk.Button(self.main, text="Home", command=self.go_to_landing_page)
        self.home_button.place(x=30, y=150)
        self.home_button.config(font=self.font)

        self.read_button = tk.Button(self.main, text="Read Instagram Comments", command=self.read)
        self.read_button.place(x=135, y=150)  # Adjusted x-coordinate
        self.read_button.config(font=self.font)

        self.clean_button = tk.Button(self.main, text="Clean Instagram Comments", command=self.clean)
        self.clean_button.place(x=420, y=150)
        self.clean_button.config(font=self.font)

        self.ml_button = tk.Button(self.main, text="Run Machine Learning Algorithm", command=self.machine_learning)
        self.ml_button.place(x=710, y=150)  # Adjusted x-coordinate
        self.ml_button.config(font=self.font)

        self.graph_button = tk.Button(self.main, text="Women Safety Graph", command=self.graph)
        self.graph_button.place(x=1050, y=150)  # Adjusted x-coordinate
        self.graph_button.config(font=self.font)


        self.font1 = ('times', 12, 'bold')
        self.text = tk.Text(self.main, height=25, width=167)
        self.scroll = tk.Scrollbar(self.text)
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.place(x=10, y=200)
        self.text.config(font=self.font1)

        self.main.config(bg='darkgrey')
        self.main.mainloop()
        
    def go_to_landing_page(self):
        self.main.destroy()  # Close the current window
        self.landing_page_instance.update()  # Update the existing LandingPage instance
        self.landing_page_instance.deiconify()

    def read(self):
        self.text.delete('1.0', tk.END)
        self.insta_list.clear()
        if self.filename:
            train = pd.read_csv(self.filename, encoding='iso-8859-1')
            for i in range(len(train)):
                insta = train.at[i, 'Comments']
                self.insta_list.append(insta)
                self.text.insert(tk.END, insta + "\n")                       # Fix here: changed self.insta to self.text
        else:
            messagebox.showwarning("Warning", "Please select a CSV file first.")

    def clean(self):
        self.text.delete('1.0', tk.END)
        self.clean_list.clear()
        if self.insta_list:
            for i in range(len(self.insta_list)):
                insta = self.insta_list[i]
                insta = insta.strip("\n")                                           # This line might be causing the error
                insta = insta.strip()
                insta = self.insta_cleaning(insta.lower())
                self.clean_list.append(insta)
                self.text.insert(tk.END, insta + "\n")
        else:
            messagebox.showwarning("Warning", "Please read comments first.")


    def machine_learning(self):
        self.text.delete('1.0', tk.END)
        self.pos = 0
        self.neu = 0
        self.neg = 0
        if self.clean_list:
            for i in range(len(self.clean_list)):
                insta = self.clean_list[i]
                blob = TextBlob(insta)
                if blob.polarity <= 0.2:
                    self.neg += 1
                    self.text.insert(tk.END, insta + "\n")
                    self.text.insert(tk.END, "Predicted Sentiment : NEGATIVE\n")
                    self.text.insert(tk.END, "Polarity Score      : " + str(blob.polarity) + "\n")
                    self.text.insert(tk.END, '==============================================================================================================================\n')
                if 0.2 < blob.polarity <= 0.5:
                    self.neu += 1
                    self.text.insert(tk.END, insta + "\n")
                    self.text.insert(tk.END, "Predicted Sentiment : NEUTRAL\n")
                    self.text.insert(tk.END, "Polarity Score      : " + str(blob.polarity) + "\n")
                    self.text.insert(tk.END, '==============================================================================================================================\n')
                if blob.polarity > 0.5:
                    self.pos += 1
                    self.text.insert(tk.END, insta + "\n")
                    self.text.insert(tk.END, "Predicted Sentiment : POSITIVE\n")
                    self.text.insert(tk.END, "Polarity Score      : " + str(blob.polarity) + "\n")
                    self.text.insert(tk.END, '==============================================================================================================================\n')
        else:
            messagebox.showwarning("Warning", "Please clean comments first.")

    def graph(self):
        if self.clean_list and (self.pos or self.neg or self.neu):
            label_X = ['Positive', 'Negative', 'Neutral']
            category_X = [self.pos, self.neg, self.neu]
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, "Safety Factor\n\n")
            self.text.insert(tk.END, 'Positive : ' + str(self.pos) + "\n")
            self.text.insert(tk.END, 'Negative : ' + str(self.neg) + "\n")
            self.text.insert(tk.END, 'Neutral  : ' + str(self.neu) + "\n\n")
            self.text.insert(tk.END, 'Length of comments : ' + str(len(self.clean_list)) + "\n")
            self.text.insert(tk.END, 'Positive : ' + str(self.pos) + ' / ' + str(len(self.clean_list)) + ' = ' + str(
                (self.pos / len(self.clean_list)) * 100) + '%\n')
            self.text.insert(tk.END, 'Negative : ' + str(self.neg) + ' / ' + str(len(self.clean_list)) + ' = ' + str(
                (self.neg / len(self.clean_list)) * 100) + '%\n')
            self.text.insert(tk.END, 'Neutral  : ' + str(self.neu) + ' / ' + str(len(self.clean_list)) + ' = ' + str(
                (self.neu / len(self.clean_list)) * 100) + '%\n')

            plt.pie(category_X, labels=label_X, autopct='%1.1f%%')
            plt.title('Women Safety & Sentiment Graph')
            plt.axis('equal')
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please run the machine learning analysis first.")

    def insta_cleaning(self, doc):
        tokens = doc.split()
        table = str.maketrans('', '', punctuation)
        tokens = [w.translate(table) for w in tokens]
        tokens = [word for word in tokens if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stop_words]
        tokens = [word for word in tokens if len(word) > 1]
        tokens = ' '.join(tokens)
        return tokens

if __name__ == "__main__":
    landing_page = LandingPage()
    landing_page.mainloop()
