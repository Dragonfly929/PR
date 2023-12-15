# USER (User Authentication):
#  PASS (Password Authentication):

from ftplib import FTP
ftp = FTP('ftp.example.com')
ftp.login(user='username', passwd='password')
ftp.cwd('/path/to/directory')
file_list = ftp.nlst()
print("List of files:", file_list)

# RETR (Retrieve File):
with open('local_file.txt', 'wb') as local_file:
    ftp.retrbinary('RETR remote_file.txt', local_file.write)

# STOR (Store File on Server):
with open('local_file.txt', 'rb') as local_file:
    ftp.storbinary('STOR remote_file.txt', local_file)

# DELE (Delete File on Server):
ftp.delete('file_to_delete.txt')

# CWD (Change Working Directory):
ftp.cwd('/new/directory/path')

# PWD (Print Working Directory):
current_directory = ftp.pwd()
print("Current Directory:", current_directory)

