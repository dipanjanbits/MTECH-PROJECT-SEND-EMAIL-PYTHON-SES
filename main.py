import boto3
from botocore.exceptions import ClientError
from cryptography.fernet import Fernet

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Dipanjan Biswas <dipanjan.aws.2022@gmail.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "dipanjan561@gmail.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "ap-south-1"

# read encrypted pwd and convert into byte
with open('encryptedACCESS.txt') as f:
    encpwd = ''.join(f.readlines())
    encpwdbyt = bytes(encpwd, 'utf-8')
f.close()

# read key and convert into byte
with open('refKeyACCESS.txt') as f:
    refKey = ''.join(f.readlines())
    refKeybyt = bytes(refKey, 'utf-8')
f.close()

# use the key and encrypt pwd
keytouse = Fernet(refKeybyt)
myPass = (keytouse.decrypt(encpwdbyt))
#print("my password - ",myPass)
ACCESS_KEY = myPass.decode()


# read encrypted pwd and convert into byte
with open('encryptedSECRET.txt') as f:
    encpwd = ''.join(f.readlines())
    encpwdbyt = bytes(encpwd, 'utf-8')
f.close()

# read key and convert into byte
with open('refKeySECRET.txt') as f:
    refKey = ''.join(f.readlines())
    refKeybyt = bytes(refKey, 'utf-8')
f.close()

# use the key and encrypt pwd
keytouse = Fernet(refKeybyt)
myPass = (keytouse.decrypt(encpwdbyt))
#print("my password - ",myPass)
SECRET_KEY = myPass.decode()



# The subject line for the email.
SUBJECT = "Amazon SES Test (SDK for Python)"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>Amazon SES Test (SDK for Python)</h1>
  <p>This email was sent with
    <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
    <a href='https://aws.amazon.com/sdk-for-python/'>
      AWS SDK for Python (Boto)</a>.
from {AWS_REGION}</p>
</body>
</html>
            """.format(**locals())            

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
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
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        #ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.	
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])