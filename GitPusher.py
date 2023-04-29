import tkinter as tk
import os
from tkinter import messagebox, filedialog
import subprocess

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Github Repo Uploader")
        self.master.geometry("420x300")
        self.master.configure(bg='#2C2F33')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="First Create a github repo with no files inside,\nthen copy it's url", bg='#2C2F33', fg='white', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Label(self.master, text="Enter Remote Repo URL:", bg='#2C2F33', fg='white', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.repo_url = tk.Entry(self.master, width=50)
        self.repo_url.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        tk.Label(self.master, text="Choose Local Repo Path:", bg='#2C2F33', fg='white', font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.local_path = tk.Entry(self.master, width=50)
        self.local_path.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.choose_local_path_btn = tk.Button(self.master, text="Browse", bg='#7289DA', fg='white', font=('Arial', 12), command=self.choose_local_path)
        self.choose_local_path_btn.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.upload_btn = tk.Button(self.master, text="Start Operation", bg='#7289DA', fg='white', font=('Arial', 12), command=self.upload_to_github, state='disabled')
        self.upload_btn.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        self.quit_btn = tk.Button(self.master, text="Quit", bg='#7289DA', fg='white', font=('Arial', 12), command=self.master.quit)
        self.quit_btn.grid(row=5, column=1, padx=10, pady=10, sticky='w')



    def choose_local_path(self):
        self.local_path.delete(0, tk.END)
        local_path = filedialog.askdirectory()
        self.local_path.insert(0, local_path)
        self.upload_btn.config(state='normal')

    def upload_to_github(self):
        repo_url = self.repo_url.get().strip()
        local_path = self.local_path.get().strip()
        if not repo_url or not local_path:
            messagebox.showerror("Error", "Please enter both the remote repo URL and the local repo path.")
            return


        try:
                       # Check if local path is a valid git repository
            if not os.path.isdir(local_path):
                messagebox.showerror("Error", f"Invalid local repo path.{local_path}")
                return
            os.chdir(local_path)

            # Commit and push changes to Github

            subprocess.run(['git', 'init'])
            subprocess.run(['git', 'add', '.'])
            subprocess.run(['git', 'commit', '-m', 'Initial commit'])
            subprocess.run(['git', 'branch', '-M', 'master'])
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
            subprocess.run(['git', 'push', '-u', 'origin', 'master'])

            messagebox.showinfo("Success", "Repo uploaded successfully!")
            self.master.quit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading to Github: {str(e)}")
            return


if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()
