# Spam Detection #

## Overview ##
Spam Detection adapts machine learning models to predict whether your email is spam or not. The email service [Spam Detection] a3-tim@tim2021.de returns a judgment showing how much the likelihood that your mail is spam with a confidence level.

## Demo ##
## Spam email ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/demo.png)
## Non-spam email ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/demo-2.png)
## Auto Retraining ML model and updating an endpoint ##


## Application (Language & Tools) ##
Backend: AWS Serverless ([S3](https://aws.amazon.com/s3/), [Lambda](https://aws.amazon.com/lambda/), [SageMaker](https://aws.amazon.com/sagemaker/), [SES](https://aws.amazon.com/tw/ses/), [Cloudformation](https://aws.amazon.com/cloudformation/))

## Architecture ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/architecture.png)

## Description ##
#### 1) [SES](https://aws.amazon.com/tw/ses/) - SES
- Receive email
- Put email on S3

#### 2) [S3](https://aws.amazon.com/s3/)  - B1
- Store emails
- Trigger lambda once object is created

#### 3) [Lambda](https://aws.amazon.com/lambda/) - LF3
- Retrieve the text content
- Call prediction endpoint for analysis

#### 4) [SageMaker](https://aws.amazon.com/sagemaker/)
- Build machine learning model by notebook
- Train the model with massive data
- Deploy an endpoint for access

#### 5) [Cloudformation](https://aws.amazon.com/cloudformation/)
- Deploy every resource
- Input parameter sagemaker endpoint and email address for spam detection service

*AWS Region: US-east-1 (N. Virginia)

## Contributor ##
#### [Tim Kao](https://github.com/tim-kao) (UNI: sk4920) [Yin Cheng](https://github.com/jyincheng)(UNI: cc4717)
