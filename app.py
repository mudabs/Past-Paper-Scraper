import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin

# List of target URLs
urls = [
    "https://pastpapers.papacambridge.com/papers/caie/as-and-a-level-business9609-2024-oct-nov",
    "https://pastpapers.papacambridge.com/papers/caie/as-and-a-level-business9609-2024-may-june",
    "https://pastpapers.papacambridge.com/papers/caie/as-and-a-level-business9609-2024-march"
    # Add more URLs here...
]

# Setup Chrome options (headless mode)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')  # Reduce console noise

# Setup Chrome driver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Prepare download folder
download_folder = "past_papers"
os.makedirs(download_folder, exist_ok=True)

# Collect and download PDF links from each URL
headers = {"User-Agent": "Mozilla/5.0"}
for url in urls:
    print(f"\n🔗 Opening: {url}")
    driver.get(url)
    time.sleep(5)  # Wait for full page load

    print("🔍 Extracting PDF links...")
    links = driver.find_elements(By.TAG_NAME, "a")
    pdf_links = [
        urljoin(url, link.get_attribute("href"))
        for link in links
        if link.get_attribute("href") and link.get_attribute("href").endswith(".pdf")
    ]

    print(f"📄 Found {len(pdf_links)} PDFs. Downloading...")

    for pdf_url in pdf_links:
        filename = os.path.basename(pdf_url)
        file_path = os.path.join(download_folder, filename)
        print(f"⬇️  Downloading: {filename}")
        try:
            response = requests.get(pdf_url, headers=headers)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"❌ Failed to download: {pdf_url}")
        except Exception as e:
            print(f"⚠️  Error downloading {pdf_url}: {e}")

driver.quit()
print("\n✅ All downloads complete.")
