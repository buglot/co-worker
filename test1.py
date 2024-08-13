from ftplib import FTP

# เชื่อมต่อกับเซิร์ฟเวอร์ FTP
ftp = FTP()
ftp.connect(('192.168.1.33', 4931))
ftp.login(user='user', passwd='12345')

# แสดงรายชื่อไฟล์และไดเรกทอรีในเซิร์ฟเวอร์
ftp.retrlines('LIST')

# ดาวน์โหลดไฟล์จากเซิร์ฟเวอร์

# ปิดการเชื่อมต่อ
ftp.quit()
