import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Khởi tạo trình duyệt
def init_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')  # Mở Chrome toàn màn hình

    # Khởi tạo ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Tải ảnh từ URL
def download_image(download_path, url, file_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(download_path, file_name), 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"Lỗi khi tải ảnh: {e}")

# Lấy URL ảnh từ pop-up
def get_image_urls_from_popup(driver, wait_time, total_images):
    image_urls = []
    images = driver.find_elements(By.CSS_SELECTOR, 'div.H8Rx8c')  # Click vào các ảnh trong kết quả tìm kiếm

    for idx, img in enumerate(images[:total_images]):
        try:
            img.click()  # Click vào ảnh để mở pop-up
            time.sleep(wait_time)  # Chờ pop-up hiện lên

            # Lấy URL ảnh từ pop-up
            popup_img = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.RfPPs.vYoxve img.sFlh5c.FyHeAf.iPVvYb'))
            )
            img_url = popup_img.get_attribute('src')
            if img_url and img_url not in image_urls:
                image_urls.append(img_url)
                print(f"Đã lấy URL ảnh {idx + 1}: {img_url}")

            # Đóng pop-up (nếu cần)
            close_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Đóng"]')
            close_button.click()
            time.sleep(0.5)  # Chờ pop-up đóng
        except Exception as e:
            print(f"Lỗi khi lấy URL ảnh {idx + 1}: {e}")

    return image_urls

# Main script
google_urls = [ 'https://www.google.com/search?q=kimono+nh%E1%BA%ADt+b%E1%BA%A3n+styles&sca_esv=b04edf4c6777ddf8&rlz=1C1GCEA_enVN1024VN1024&udm=2&biw=1536&bih=695&sxsrf=AHTn8zpcL-OpbB0PoMbgJ0Rrb4vITCpplw%3A1741191992297&ei=OHvIZ67pEabR2roPgN6WuQ0&ved=0ahUKEwiu5b7RrfOLAxWmqFYBHQCvJdcQ4dUDCBI&uact=5&oq=kimono+nh%E1%BA%ADt+b%E1%BA%A3n+styles&gs_lp=EgNpbWciGmtpbW9ubyBuaOG6rXQgYuG6o24gc3R5bGVzSI0dULkEWLkbcAd4AJABBpgBiwGgAesNqgEEMy4xNrgBA8gBAPgBAZgCAqAClwHCAggQABgTGAcYHsICBhAAGAcYHsICCBAAGAcYCBgemAMAiAYBkgcDMS4xoAf4DQ&sclient=img#vhid=KRTnEXOPliUqrM&vssid=mosaic']
labels = ['kimono']

if len(google_urls) != len(labels):
    raise ValueError('Danh sách URL không khớp với danh sách nhãn.')

download_dir = 'images/fashion_style'
os.makedirs(download_dir, exist_ok=True)

for lbl in labels:
    lbl_path = os.path.join(download_dir, lbl)
    os.makedirs(lbl_path, exist_ok=True)

TOTAL_NUMBER_OF_EXAMPLES = 50
driver = init_chrome_driver()


try:
    for url_current, lbl in zip(google_urls, labels):
        driver.get(url_current)
        time.sleep(2)  # Chờ trang tải xong

        # Lấy URL ảnh từ pop-up
        urls = get_image_urls_from_popup(driver, 1, TOTAL_NUMBER_OF_EXAMPLES)
        
        # Tải ảnh về
        for idx, url in enumerate(urls):
            download_image(
                download_path=os.path.join(download_dir, lbl),
                url=url,
                file_name=f'{idx + 1}.jpg'
            )
finally:
    driver.quit()