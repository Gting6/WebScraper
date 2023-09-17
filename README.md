# WebScraper

## Introduction

This script uses the AWS Lambda service to automatically scrap the data from `https://stormcenter.oncor.com`

The code structure:
![Screenshot 2023-09-17 at 5 21 14 PM](https://github.com/Gting6/WebScraper/assets/46078333/e9eae016-e4a8-4992-a061-8eeba146743a)

A concise demo:
https://youtu.be/RkZr5gFfwQ8

## Reproduce

1. Use Amazon Web Service
2. Add a new role, using S3PutPolicy and AWSLambdaBasicExecutionRole
3. Open a non public s3 bucket
4. Add a EventBridge rule
5. Integrate `chromedriver.zip` and `headless-chromium.zip` to your Amazon lambda

## Implementation Details

1. Go to https://stormcenter.oncor.com
2. Locate “View Zip Code” button and go to the report page
3. Locate data table
4. Scroll the table and record the data
5. Dump results into a JSON file
6. Upload to S3 bucket
