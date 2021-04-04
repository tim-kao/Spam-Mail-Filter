import json
import boto3
import os
from botocore.exceptions import ClientError
from sms_spam_classifier_utilities import one_hot_encode
from sms_spam_classifier_utilities import vectorize_sequences

vocabulary_length = 9013
RECEIVER = os.environ.get("spam_detect_email_addr")
end_point = os.environ.get("sagemaker_endpoint")
client = boto3.client('sagemaker-runtime')

fail_response = {
    'statusCode': 501,
    'body': json.dumps('Not Implemented')
}

okay_response = {
    'statusCode': 200,
    'body': json.dumps('Spam analysis result sent')
}


def lambda_handler(event, context):
    print(event)
    key = event['Records'][0]['s3']['object']['key']  # 'images/Example.jpg'
    bucket = event['Records'][0]['s3']['bucket']['name']  # 'cloud-computing-a2-b2'
    # key, bucket = 'a3-tim@tim2021.de/gbqr62bdv6l7rh0702kp4bej9aluvtbptpfcpsg1', 'a3-email'
    print(key, bucket)
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket, Key=key)

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        email_object = response['Body'].read().decode('utf-8')
        email = parser(email_object)
        print('email body:', email['body'])
        one_hot_test_messages = one_hot_encode([email['body']], vocabulary_length)
        encoded_test_messages = vectorize_sequences(one_hot_test_messages, vocabulary_length)
        payload = json.dumps(encoded_test_messages.tolist())
        res_sagemaker = client.invoke_endpoint(EndpointName=end_point, ContentType='application/json', Body=payload)
        print(res_sagemaker)
        if res_sagemaker['ResponseMetadata']['HTTPStatusCode'] == 200:
            result = json.loads(res_sagemaker['Body'].read().decode())
            email_handler(email, result)
            return okay_response

        else:
            return fail_response
    else:
        return fail_response


def parser(payload):
    email = dict()
    rows = payload.split('\r\n')
    for row in rows:
        if 'sender' not in email:
            snd = row.split('From: ')
            if len(snd) == 2:
                email['sender'] = snd[1].split('<')[1].split('>')[0]
        else:
            sub = row.split('Subject: ')
            if len(sub) == 2:
                email['subject'] = sub[1]
                break
    email['received'] = payload.split('Received: ')[1].split('for ' + RECEIVER + ';\r\n ')[1].split('\r\n')[0]
    email['body'] = payload.split('Content-Type: text/plain; charset="UTF-8"\r\n\r\n')[1].split('\r\n\r\n')[0].replace('\n', '')

    return email


def email_handler(email, result):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"

    # The subject line for the email.
    SUBJECT = "Spam filter notification"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = 'We received your email sent at [' + email['received'] + \
                '] with the subject [' + email['subject'] + '].\n\n' \
                                                            'Here is a 240 character sample of the email body:\n' + \
                email['body'][:240] + \
                '\n\nThe email was categorized as [' + str(result['predicted_label'][0][0]) + \
                '] with a [' + str(result['predicted_probability'][0][0] * 100) + ']% confidence.”'

    # The HTML body of the email.
    BODY_HTML = BODY_TEXT

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    email['sender'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=RECEIVER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])