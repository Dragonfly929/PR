import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ftplib import FTP
import smtplib
from email.mime.text import MIMEText


FTP_HOSTNAME = '138.68.98.108'
FTP_USERNAME = 'yourusername'
FTP_PASSWORD = 'yourusername'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
SENDER_EMAIL = 'xxx@gmail.com'
SENDER_PASSWORD = 'oozf stem psoi vyjg'


def upload_file_ftp():
    try:
        local_file_path = file_path_entry.get()
        file_name = os.path.basename(local_file_path)

        ftp = FTP(FTP_HOSTNAME)
        ftp.login(user=FTP_USERNAME, passwd=FTP_PASSWORD)

        ftp.cwd('faf-212')

        working_directory = 'Maia'
        create_directory_if_not_exists(ftp, working_directory)
        ftp.cwd(working_directory)

        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {file_name}', file)

        ftp.quit()

        file_url = f"ftp://{FTP_USERNAME}:{FTP_PASSWORD}@{FTP_HOSTNAME}/{working_directory}/{file_name}"
        send_email(file_url)
        update_status_label("File has been Uploaded!")

    except Exception as e:
        print(f"File upload failed. Error: {str(e)}")
        update_status_label("File upload failed.")


def create_directory_if_not_exists(ftp, directory):
    if directory not in ftp.nlst():
        ftp.mkd(directory)


def send_email(file_url):
    subject = subject_entry.get()
    body = body_entry.get("1.0", tk.END)
    recipient_email = recipient_entry.get()

    body_with_url = f"{body}\n\nFile URL: {file_url}"

    msg = MIMEText(body_with_url)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp_server:
            smtp_server.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            update_status_label("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Email sending failed. Error: {str(e)}")
        update_status_label("Email sending failed.")
        return False


def browse_file():
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(tk.END, filedialog.askopenfilename())


def update_status_label(message):
    status_label.config(text=message)


root = tk.Tk()
root.title("Mail client using SMTP and FTP")


style = ttk.Style()
style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 12', foreground='black', background='#153742')
style.configure("TLabel", font='Helvetica 12', background='#eaf2f4')
style.configure("TEntry", font='Helvetica 12', padding=(5, 5, 5, 5))
style.configure("TText", font='Helvetica 12', padding=(5, 5, 5, 5))


file_path_label = ttk.Label(root, text="File Path:")
file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

file_path_entry = ttk.Entry(root, width=40)
file_path_entry.grid(row=0, column=1, padx=10, pady=5)

browse_button = ttk.Button(root, text="Browse this computer", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=5)

from_label = ttk.Label(root, text="From:")
from_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

from_email_label = ttk.Label(root, text=SENDER_EMAIL, font='Helvetica 12 bold', foreground='black')
from_email_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

recipient_label = ttk.Label(root, text="To:")
recipient_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

recipient_entry = ttk.Entry(root, width=40)
recipient_entry.grid(row=2, column=1, padx=10, pady=5)

subject_label = ttk.Label(root, text="Subject:")
subject_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

subject_entry = ttk.Entry(root, width=40)
subject_entry.grid(row=3, column=1, padx=10, pady=5)

body_label = ttk.Label(root, text="Body:")
body_label.grid(row=4, column=0, padx=10, pady=5, sticky='w')

body_entry = tk.Text(root, height=5, width=40)
body_entry.grid(row=4, column=1, padx=10, pady=5)

upload_button = ttk.Button(root, text="Send Email", command=upload_file_ftp)
upload_button.grid(row=5, column=1, pady=10)

status_label = ttk.Label(root, text="", foreground='#008CBA')
status_label.grid(row=6, column=0, columnspan=2, pady=5)


root.mainloop()
