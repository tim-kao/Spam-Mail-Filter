# Spam Detection #

## Overview ##
Spam Detection adapts machine learning models to predict whether your email is spam or not. The e-mail service [Spam-Mail-Filter](a3-tim@tim2021.de) returns a judgement showing how much the likelihood that your mail is spam with confidence level.

## Demo ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/demo.png)

## Application (Language & Tools) ##
1) Backend: AWS Serverless ([S3](https://aws.amazon.com/s3/), [Lambda](https://aws.amazon.com/lambda/), [SageMaker](https://aws.amazon.com/sagemaker/), [SES](https://aws.amazon.com/tw/ses/)

## Architecture ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/architecture.png)
1) User -> Send email to request the spam detection
2) SES -> puts the email on S3 bucket
3) S3 -> triggers lambda LF3
4) LF3 -> retrieve the text content and call prediction endpoint for analysis. Then, it returns the analysis result to the user.

## Description ##
#### 1) [SES](https://aws.amazon.com/tw/ses/) - SES
- Receive email
- Put email on S3

#### 1) [S3](https://aws.amazon.com/s3/)  - B1
- Store emails
- Trigger lambda once object is created

#### 2) [Lambda](https://aws.amazon.com/lambda/) - LF3
- Retrieve the text content
- Call prediction endpoint for analysis

*AWS Region: US-east-1 (N. Virginia)

## Contributor ##
#### [Tim Kao](https://github.com/tim-kao) (UNI: sk4920) [Yin Cheng](https://github.com/jyincheng)(UNI: cc4717)
