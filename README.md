# WebScraper

## Introduction

This script uses the AWS Lambda service to automatically scrap the data from `https://stormcenter.oncor.com`

The code structure is as following:

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
