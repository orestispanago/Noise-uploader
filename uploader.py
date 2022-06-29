import glob
import os
from ftplib import FTP, error_perm

# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
os.chdir("FTP")

ftp_ip = ""
ftp_user = ""
ftp_password = ""
ftp_dir = "~/datalogger/thermi-noise"


def mkdir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def rename(old_path):
    dt = old_path.split("_")[1]
    year = dt[:2]
    month = dt[2:4]
    day = dt[4:6]
    hour_minute = dt[6:]
    return f"{year}/{month}/{day}/{hour_minute}"


def move_file(source, destination):
    mkdir_if_not_exists(os.path.dirname(destination))
    os.rename(source, destination)


def ftp_mkdir_and_enter(ftp_session, dir_name):
    if dir_name not in ftp_session.nlst():
        ftp_session.mkd(dir_name)
    ftp_session.cwd(dir_name)


def ftp_make_dirs(ftp_session, folder_path):
    for f in folder_path.split("/"):
        ftp_mkdir_and_enter(ftp_session, f)


def ftp_upload(ftp_session, local_path, remote_path):
    with open(local_path, "rb") as f:
        ftp_session.storbinary(f"STOR {remote_path}", f)


def select_non_empty(files):
    non_empty = []
    for f in files:
        if os.path.getsize(f) > 0:
            non_empty.append(f)
    return non_empty


def upload_and_archive(files):
    for local_file in files:
        new_path = rename(local_file)
        with FTP(ftp_ip, ftp_user, ftp_password) as ftp:
            ftp.cwd(ftp_dir)
            try:
                ftp_upload(ftp, local_file, new_path)
                move_file(local_file, f"uploaded/{new_path}")
            except error_perm as e:
                if "55" in str(e):
                    ftp_make_dirs(ftp, os.path.dirname(new_path))
                ftp.cwd(ftp_dir)
                ftp_upload(ftp, local_file, new_path)
                move_file(local_file, f"uploaded/{new_path}")


local_files = glob.glob("*.txt")
non_empty_files = select_non_empty(local_files)
upload_and_archive(non_empty_files)
