import os
import time
import random
import subprocess
import sys

# 检查并安装所需的库
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
except ImportError:
    install('requests')

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
except ImportError:
    install('selenium')

def jump_to_author():
    uid = uid_entry.get()
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    author_url = "https://www.pixiv.net/users/" + uid
    driver.get(author_url)

def download_all_works():
    uid = uid_entry.get()
    author_url = "https://www.pixiv.net/users/" + uid
    
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    driver.get(author_url)

    driver.implicitly_wait(10)
    works = driver.find_elements(By.CSS_SELECTOR, "a[href*='/artworks/']")
    work_links = [work.get_attribute('href') for work in works]

    os.makedirs(uid, exist_ok=True)

    max_requests = 100
    request_count = 0

    for link in work_links:
        if request_count >= max_requests:
            print("达到最大请求次数，暂停一段时间...")
            time.sleep(3600)
            request_count = 0

        try:
            driver.get(link)
            time.sleep(random.uniform(2, 5))

            img_element = driver.find_element(By.CSS_SELECTOR, "img[src*='img-master']")
            img_url = img_element.get_attribute('src')

            img_data = requests.get(img_url).content
            img_name = os.path.join(uid, img_url.split('/')[-1])

            with open(img_name, 'wb') as handler:
                handler.write(img_data)

            request_count += 1

        except Exception as e:
            print(f"请求失败: {e}")
            time.sleep(10)

    driver.quit()
    print("所有作品已下载。")

# 创建一个Tkinter窗口
window = Tk()
window.title("Pixiv作者查询")
window.geometry("400x400")
window.configure(bg="#f0f0f0")  # 设置背景颜色

# 设置字体
title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=12)

# 创建一个Frame用于组织控件
frame = Frame(window, bg="#f0f0f0")
frame.pack(pady=20)

# 创建一个标签和输入框用于输入UID
uid_label = Label(frame, text="请输入UID：", bg="#f0f0f0", font=label_font)
uid_label.pack(pady=5)
uid_entry = Entry(frame, width=30, font=label_font)
uid_entry.pack(pady=5)

# 创建两个按钮，一个用于跳转到作者界面，另一个用于下载作者所有作品
jump_button = Button(frame, text="跳转到作者界面", command=jump_to_author, bg="#4CAF50", fg="white", font=label_font)
jump_button.pack(pady=10)

download_button = Button(frame, text="下载作者所有作品", command=download_all_works, bg="#2196F3", fg="white", font=label_font)
download_button.pack(pady=10)

# 添加提示语到窗口底部
info_frame = Frame(window, bg="#f0f0f0")
info_frame.pack(side=BOTTOM, pady=20)

info_label = Label(info_frame, text="在运行后请等待片刻，请勿关闭脚本", bg="#f0f0f0", font=label_font)
info_label.pack(pady=2)

info_label2 = Label(info_frame, text="请保证您的网络可以正常访问pixiv", bg="#f0f0f0", font=label_font)
info_label2.pack(pady=2)

info_label3 = Label(info_frame, text="仅供学习交流使用，禁止用于违法用途", bg="#f0f0f0", font=label_font)
info_label3.pack(pady=2)

# 运行Tkinter窗口的主循环
window.mainloop()




