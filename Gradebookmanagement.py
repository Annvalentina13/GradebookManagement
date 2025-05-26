import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import matplotlib.pyplot as plt

# Ensure data folder and CSVs exist
if not os.path.exists("data"):
    os.makedirs("data")

for file in ["students.csv", "subjects.csv", "grades.csv"]:
    if not os.path.exists(f"data/{file}"):
        if file == "students.csv":
            pd.DataFrame(columns=["student_id", "name", "email"]).to_csv(f"data/{file}", index=False)
        elif file == "subjects.csv":
            pd.DataFrame(columns=["subject_code", "subject_name"]).to_csv(f"data/{file}", index=False)
        elif file == "grades.csv":
            pd.DataFrame(columns=["student_id", "subject_code", "marks"]).to_csv(f"data/{file}", index=False)

# Load and save helpers
def load_csv(name):
    return pd.read_csv(f"data/{name}")

def save_csv(df, name):
    df.to_csv(f"data/{name}", index=False)

# GUI Class
class GradebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gradebook Management System")
        self.root.geometry("600x400")

        self.tab_control = ttk.Notebook(root)

        self.student_tab = ttk.Frame(self.tab_control)
        self.subject_tab = ttk.Frame(self.tab_control)
        self.grade_tab = ttk.Frame(self.tab_control)
        self.gpa_tab = ttk.Frame(self.tab_control)
        self.chart_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.student_tab, text="Add Student")
        self.tab_control.add(self.subject_tab, text="Add Subject")
        self.tab_control.add(self.grade_tab, text="Add Grade")
        self.tab_control.add(self.gpa_tab, text="Calculate GPA")
        self.tab_control.add(self.chart_tab, text="View Chart")

        self.tab_control.pack(expand=1, fill="both")

        self.build_student_tab()
        self.build_subject_tab()
        self.build_grade_tab()
        self.build_gpa_tab()
        self.build_chart_tab()

    def build_student_tab(self):
        tk.Label(self.student_tab, text="Student ID").pack()
        self.sid = tk.Entry(self.student_tab)
        self.sid.pack()

        tk.Label(self.student_tab, text="Name").pack()
        self.sname = tk.Entry(self.student_tab)
        self.sname.pack()

        tk.Label(self.student_tab, text="Email").pack()
        self.semail = tk.Entry(self.student_tab)
        self.semail.pack()

        tk.Button(self.student_tab, text="Add Student", command=self.add_student).pack()

    def add_student(self):
        sid, name, email = self.sid.get(), self.sname.get(), self.semail.get()
        if not sid or not name or not email:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        df = load_csv("students.csv")
        if sid in df["student_id"].values:
            messagebox.showerror("Error", "Student ID already exists.")
            return
        df.loc[len(df)] = [sid, name, email]
        save_csv(df, "students.csv")
        messagebox.showinfo("Success", "Student added successfully.")

    def build_subject_tab(self):
        tk.Label(self.subject_tab, text="Subject Code").pack()
        self.sub_code = tk.Entry(self.subject_tab)
        self.sub_code.pack()

        tk.Label(self.subject_tab, text="Subject Name").pack()
        self.sub_name = tk.Entry(self.subject_tab)
        self.sub_name.pack()

        tk.Button(self.subject_tab, text="Add Subject", command=self.add_subject).pack()

    def add_subject(self):
        code, name = self.sub_code.get(), self.sub_name.get()
        if not code or not name:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        df = load_csv("subjects.csv")
        if code in df["subject_code"].values:
            messagebox.showerror("Error", "Subject code already exists.")
            return
        df.loc[len(df)] = [code, name]
        save_csv(df, "subjects.csv")
        messagebox.showinfo("Success", "Subject added successfully.")

    def build_grade_tab(self):
        tk.Label(self.grade_tab, text="Student ID").pack()
        self.g_sid = tk.Entry(self.grade_tab)
        self.g_sid.pack()

        tk.Label(self.grade_tab, text="Subject Code").pack()
        self.g_code = tk.Entry(self.grade_tab)
        self.g_code.pack()

        tk.Label(self.grade_tab, text="Marks").pack()
        self.g_marks = tk.Entry(self.grade_tab)
        self.g_marks.pack()

        tk.Button(self.grade_tab, text="Add Grade", command=self.add_grade).pack()

    def add_grade(self):
        sid, code, marks = self.g_sid.get(), self.g_code.get(), self.g_marks.get()
        if not sid or not code or not marks:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        try:
            marks = float(marks)
        except:
            messagebox.showerror("Error", "Marks must be a number.")
            return
        df = load_csv("grades.csv")
        df.loc[len(df)] = [sid, code, marks]
        save_csv(df, "grades.csv")
        messagebox.showinfo("Success", "Grade added successfully.")

    def build_gpa_tab(self):
        tk.Label(self.gpa_tab, text="Enter Student ID").pack()
        self.gpa_sid = tk.Entry(self.gpa_tab)
        self.gpa_sid.pack()

        self.gpa_result = tk.Label(self.gpa_tab, text="")
        self.gpa_result.pack()

        tk.Button(self.gpa_tab, text="Calculate GPA", command=self.calculate_gpa).pack()

    def calculate_gpa(self):
        sid = self.gpa_sid.get()
        df = load_csv("grades.csv")
        student_grades = df[df["student_id"] == sid]
        if student_grades.empty:
            self.gpa_result.config(text="No grades found for this student.")
            return
        avg = student_grades["marks"].mean()
        self.gpa_result.config(text=f"GPA (Average Marks): {avg:.2f}")

    def build_chart_tab(self):
        tk.Label(self.chart_tab, text="Enter Student ID").pack()
        self.chart_sid = tk.Entry(self.chart_tab)
        self.chart_sid.pack()

        tk.Button(self.chart_tab, text="Show Performance Chart", command=self.show_chart).pack()

    def show_chart(self):
        sid = self.chart_sid.get()
        grades_df = load_csv("grades.csv")
        subs_df = load_csv("subjects.csv")

        student_grades = grades_df[grades_df["student_id"] == sid]
        if student_grades.empty:
            messagebox.showerror("Error", "No grades found for this student.")
            return

        merged = pd.merge(student_grades, subs_df, on="subject_code", how="left")
        plt.figure(figsize=(8, 4))
        plt.bar(merged["subject_name"], merged["marks"], color='skyblue')
        plt.title(f"Performance of {sid}")
        plt.xlabel("Subjects")
        plt.ylabel("Marks")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GradebookApp(root)
    root.mainloop()
