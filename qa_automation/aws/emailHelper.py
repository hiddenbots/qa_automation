"""

**Description**:to send reports of a test suit execution to user

**Author**: Ahmad Afraz Khan

*************************************************
Modification Log:  
********************************************************************
Date             |           Author                |                  Description
**********************************************************  
19/09/2019       |           Ahmad Afraz Khan      |     Final draft.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
---------------------------------------------------------------------------
""" 

import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication




class emailHelper:
    """
    this class handles all email notifications in frameworks.
    """

    def __init__(self):
        """
        Create a new SES resource
        """
        self.__ses_client = boto3.client('ses')

    def send_email(self,files, sender_email, recipients, subject, body_text):
        """
        this function sends email notification with attachements to recipients from QA Framework 
        containing result reports.

        :param sender_email: Default email id from QA Framework
        :type sender_email: str
        :param recipients: all email id's to which reports will be sent
        :type recipients: list
        :param files: a list containing paths all files to be attached with email.
        :type files: list
        :param subject: The subject line for the email.
        :type subject: str
        :param body_text: The email body for recipients with non-HTML email clients.
        :type body_text: str
        """

        # The HTML body of the email.
        BODY_HTML = """\
        <html>
        <head></head>
        <body>
        <h1>QA Automation</h1>
        <p>"""+ body_text+""".</p>
        </body>
        </html>
        """

        # The character encoding for the email.
        CHARSET = "utf-8"

        # Create a multipart/mixed parent container.
        msg = MIMEMultipart('mixed')
        # Add subject, from and to lines.
        msg['Subject'] = subject 
        msg['From'] = sender_email

        # Create a multipart/alternative child container.
        msg_body = MIMEMultipart('alternative')

        # Encode the text and HTML content and set the character encoding. This step is
        # necessary if you're sending a message with characters outside the ASCII range.
        htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

        # Add the text and HTML parts to the child container.
        msg_body.attach(htmlpart)

        # Attach the multipart/alternative child container to the multipart/mixed
        # parent container.
        msg.attach(msg_body)
        msg = self.__attach_files(msg, files)
        self.__send(msg, self.__ses_client, sender_email, recipients)
       
    def __attach_files(self, msg, files):
        """
        attaches all files to :class:msg to be sent

        :param msg: object containing metadata for our message
        :type msg: MIMEMultipart
        :param files: a list containing paths all files to be attached with email.
        :type files: list
        :return: returns a final Mime object after attaching files to it
        :rtype: MIMEMultipart
        """
        # Define the attachment part and encode it using MIMEApplication.
        attachments = []
        for ATTACHMENT in files:
            attachments.append(MIMEApplication(open(ATTACHMENT, 'rb').read()))

        # Add a header to tell the email client to treat this part as an attachment,
        # and to give the attachment a name.
        i = 0
        for att in attachments:
            att.add_header('Content-Disposition','attachment',filename=os.path.basename(files[i]))
            i+=1

        # Add the attachment to the parent container.
        for attachs in attachments:
            msg.attach(attachs)
        return msg
    
    def __send(self, msg, ses_client, sender, recipients):
        """
        sends msg to all recipients

        :param msg: object containing metadata for our message
        :type msg: MIMEMultipart
        :param ses_client: an AWS SES client for sending email
        :type ses_client: Client
        :param sender: emailid which will send final email
        :type sender: str
        param recipients: all email id's to which reports will be sent
        :type recipients: list
        """
        try:
            #Provide the contents of the email.
            for emailid in recipients:
                msg['To'] = emailid
                response = self.__ses_client.send_raw_email(
                Source=sender,
                Destinations=[emailid],
                RawMessage={
                    'Data':msg.as_string(),
                }
            )
        # Display an error if something goes wrong.	
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

