# Spam Detection #

## Overview ##
Spam Detection adapts machine learning models to predict whether your email is spam or not. The e-mail service [Spam-Mail-Filter](a3-tim@tim2021.de) returns a judgement showing how the likelihood your mail is spam with confidence level.

## Demo ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/demo.png)

## Application (Language & Tools) ##
1) Backend: AWS Serverless ([S3](https://aws.amazon.com/s3/), [Lambda](https://aws.amazon.com/lambda/), [SageMaker](https://aws.amazon.com/sagemaker/), [SES](https://aws.amazon.com/tw/ses/)


## Architecture ##
![image](https://github.com/tim-kao/Spam-Mail-Filter/blob/main/demo/architecture.png)
1) User -> Frontend (chat.html / AWS S3): user input "hello" to initiate the conversation
2) Frontend -> API: send user's messages to API.
3) API -> LF0: LF0 receive message from API.
4) LF0 -> Lex: direct user's message to Lex and start the conversation with the Dining Chatbot.
5) Lex -> LF1: after the conversation, LF1 will be triggered to send recommendation to users via SQS.


## Description ##
#### 1) [S3](https://aws.amazon.com/s3/)
- Store the frontend files.
- Generate SDK from AWS API Gateway and store it into js folder.
- chat.js file needs modification.
- Create CORS policy.

#### 2) [Lambda](https://aws.amazon.com/lambda/) - LF0
- Receive messages from the frontend user.
- Direct messages to Dining Chatbot in Lex.

*AWS Region: US-east-1 (N. Virginia)


## Contributor ##
#### [Tim Kao](https://github.com/tim-kao) (UNI: sk4920) [Yin Cheng](https://github.com/jyincheng)(UNI: cc4717)
