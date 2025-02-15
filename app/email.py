
from fastapi import APIRouter, HTTPException, Depends, Security
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from app.config import Config
from typing import Annotated
from app import models, schemas
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1")

class EmailRequest(BaseModel):
    to_address: str
    subject: str
    body: str

# Configurez votre client SES
ses_client = boto3.client(
    'ses',
    region_name='us-east-1',
    aws_access_key_id='AKIAYPIJMGKEO2YDQAEB',
    aws_secret_access_key=Config.AWS_SES_ACCESS_KEY
)

@router.post("/send-email/")
async def send_email(emailRequests : EmailRequest):
    try:
        response = ses_client.send_email(
            Source='no_reply@tagian.ca',
            Destination={
                'ToAddresses': [
                    emailRequests.to_address,
                ],
            },
            Message={
                'Subject': {
                    'Data': emailRequests.subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': emailRequests.body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        return {"message": "Email sent successfully!", "response": response}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=400, detail=str(e))


def send_reset_password_mail(emailRequests : EmailRequest, token : str):
    try:
        response = ses_client.send_email(
        Source='no_reply@tagian.ca',
            Destination={
                'ToAddresses': [
                    emailRequests.to_address,
                ],
            },
            Message={
                'Subject': {
                    'Data': emailRequests.subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': emailRequests.body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        );
        return {"message": "Email sent successfully!", "response": response}
    except (NoCredentialsError, PartialCredentialsError) as e:
        raise HTTPException(status_code=400, detail=str(e))


