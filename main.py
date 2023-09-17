from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import boto3


def main(event, context):
    s3 = boto3.client("s3")
    bucket = "scraperbucketgting"

    options = Options()
    options.binary_location = "/opt/headless-chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome("/opt/chromedriver", chrome_options=options)
    result = []

    try:
        driver.get("https://stormcenter.oncor.com")
        time.sleep(2)
        reportLink = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/main/section/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/div[1]/a"
        ).get_attribute("href")

        time.sleep(2)
        driver.get(reportLink)
        print(reportLink)
        time.sleep(5)

        elements = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/main/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[2]"
        )
        visited = set()
        for i in range(51):
            driver.execute_script(
                "arguments[0].scroll(0, arguments[0].scrollHeight* " + str(i) + "/50);",
                elements,
            )
            rows = driver.find_elements_by_class_name("report-row")
            time.sleep(2)
            for x in rows:
                l = x.text.split("\n")
                if len(l) < 3 or l[0] == "Zip Code" or l[0] in visited:  # invalid data
                    continue
                data = {}
                visited.add(l[0])
                data["Zip Code"] = l[0]
                data["Customers Affected"] = l[1]
                data["Customers Served"] = l[2]
                if len(l) > 3:
                    data["Latest Estimated Restoration"] = l[3]
                else:
                    data["Latest Estimated Restoration"] = ""
                result.append(data)
        driver.close()
        driver.quit()

    except Exception as e:
        print("exception!", e)
        driver.close()
        driver.quit()
        response = {"statusCode": 500, "body": ""}
        return response

    response = json.dumps(result, indent=1)
    filename = time.strftime("%Y%m%d_%H%M%S.json")

    uploadByteStream = bytes(response.encode("UTF-8"))
    s3.put_object(Bucket=bucket, Key=filename, Body=uploadByteStream)
    print("Put Completed: ", filename)
    return {"statusCode": 200, "body": ""}
