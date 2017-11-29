#boto3 api call for messaging.
import boto3

# Create an SNS client
def sendSMS(phoneNumber,message):
	client = boto3.client(
	    "sns",
	    aws_access_key_id="AKIAIZM27I7GUDMHG4BQ",
	    aws_secret_access_key="dDqiCzcwBdLDSgpsP3AJREuQojihDDNWiVm8Is0v",
	    region_name="us-east-1"
	)
	
	# Send your sms message.
	client.publish(
	    PhoneNumber="+1"+str(phoneNumber),
	    Message=message
	)