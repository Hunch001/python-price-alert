import os
import re
import smtplib

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


GMAIL_ADDR = os.getenv("Gmail_Addy")
GMAIL_APP_PW = os.getenv("Gmail_App_PW")
DEST_ADDR = os.getenv("Dest_email")


URL= "https://www.amazon.com/dp/B0F13B7XQB/ref=sspa_dk_detail_1?psc=1&pd_rd_i=B0F13B7XQB&pd_rd_w=KbNa0&content-id=amzn1.sym.3bc66c0a-cc61-4816-aa2d-e53327eaddb6&pf_rd_p=3bc66c0a-cc61-4816-aa2d-e53327eaddb6&pf_rd_r=WC4W8J2HQGJC5V5BD6NV&pd_rd_wg=8g4Yj&pd_rd_r=e7aae727-0fcc-4a88-8d2c-c7e62aa5e321&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWxfdGhlbWF0aWM"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
}

response = requests.get(url=URL, headers=header)
soup = BeautifulSoup(response.content, "html.parser")


price = soup.find(class_ = "a-offscreen").get_text()
# print(f"The current Instant pot price is {price.split("$")[1]}")

price_without_currency = price[3:]
price_as_float = float(price_without_currency.replace(",", ""))
print(price_as_float)

# # Get product Title
title = soup.find(id="productTitle").getText()
title_cleaned = re.sub(r'\s+', ' ', title).strip()
print(title_cleaned)

# # Set the price below which you would like to get a notification
Buy_price = 62000

if price_as_float < Buy_price:
    message = f"{title_cleaned} is on sale for {price}!"

    with smtplib.SMTP_SSL(host="smtp.gmail.com", port=465, timeout=30) as smtp_server:
        smtp_server.login(user=GMAIL_ADDR, password=GMAIL_APP_PW)
        smtp_server.sendmail(
            from_addr=GMAIL_ADDR,
            to_addrs=DEST_ADDR,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode()
        )
        print("Email successfully sent!")



