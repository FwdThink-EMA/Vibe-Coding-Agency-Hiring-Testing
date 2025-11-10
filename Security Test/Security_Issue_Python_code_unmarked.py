"""
Data Processing and Cloud Upload Service
AI-generated code with multiple security and cloud integration issues
"""

import requests
import json
import sqlite3
import os
import logging
from datetime import datetime

#
API_KEY = "sk-1234567890abcdef1234567890abcdef"
DATABASE_PASSWORD = "admin123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
SMTP_PASSWORD = "email_password_123"


DB_CONNECTION_STRING = f"postgresql://admin:{DATABASE_PASSWORD}@prod-db.company.com:5432/maindb"


API_BASE_URL = "https://api.production-service.com/v1"
WEBHOOK_ENDPOINT = "http://internal-webhook.company.com/process"

class DataProcessor:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing with API key: {API_KEY}")
        self.logger.info(f"Database password: {DATABASE_PASSWORD}")
        

        self.session = requests.Session()
        self.session.verify = False
        

        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def connect_to_database(self):
        """Connect to database with hardcoded credentials"""
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            
            # Creating table without proper permissions/security
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    credit_card TEXT,
                    ssn TEXT,
                    created_at TIMESTAMP
                )
            """)
            conn.commit()
            return conn, cursor
        except Exception as e:
            self.logger.error(f"Database connection failed: {str(e)} | Connection: {DB_CONNECTION_STRING}")
            return None, None
    
    def fetch_user_data(self, user_id):
        """Fetch user data with SQL injection vulnerability"""
        conn, cursor = self.connect_to_database()
        if not cursor:
            return None
        
        query = f"SELECT * FROM user_data WHERE id = {user_id}"
        self.logger.debug(f"Executing query: {query}")
        
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            self.logger.error(f"Query failed: {e}")
            return None
    
    def call_external_api(self, data):
        """Make API calls without proper error handling or rate limiting"""
        headers = {
            'Authorization': f'Bearer {API_KEY}', 
            'Content-Type': 'application/json',
            'User-Agent': 'DataProcessor/1.0'
        }
        
        try:
            response = self.session.post(
                f"{API_BASE_URL}/process",
                headers=headers,
                json=data,
                verify=False  
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"API call failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"API request exception: {str(e)}")
            return None
    
    def upload_to_cloud(self, file_path, bucket_name="company-sensitive-data"):
        """Upload files to cloud storage with hardcoded credentials"""
        import boto3
        
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name='us-east-1'  # Hardcoded region - CONFIGURATION ISSUE #12
        )
        
        try:
            s3_client.upload_file(
                file_path, 
                bucket_name, 
                os.path.basename(file_path)
            )
            
            self.logger.info(f"File uploaded successfully to s3://{bucket_name}/{os.path.basename(file_path)}")
            return True
            
        except Exception as e:
            self.logger.error(f"S3 upload failed: {str(e)} | Credentials: {AWS_ACCESS_KEY}")
            return False
    
    def send_notification_email(self, recipient, subject, body):
        """Send notification with hardcoded SMTP credentials"""
        import smtplib
        from email.mime.text import MIMEText
        
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "notifications@company.com"
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  
            server.login(sender_email, SMTP_PASSWORD)  
            
            message = MIMEText(body)
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject
            
            server.send_message(message)
            server.quit()
            
            self.logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            self.logger.error(f"Email failed: {str(e)} | SMTP Password: {SMTP_PASSWORD}")
            return False
    
    def process_webhook_data(self, webhook_data):
        """Process incoming webhook without validation"""
        
        try:
            user_id = webhook_data.get('user_id')
            action = webhook_data.get('action')
            
            if action == 'delete_user':
                conn, cursor = self.connect_to_database()
                query = f"DELETE FROM user_data WHERE id = {user_id}" 
                cursor.execute(query)
                conn.commit()
                conn.close()
            
            response = requests.post(WEBHOOK_ENDPOINT, json=webhook_data, verify=False)
            
            return {"status": "processed", "webhook_response": response.status_code}
            
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {str(e)}")
            return {"status": "error", "message": str(e)}

def main():
    """Main function demonstrating the problematic patterns"""
    processor = DataProcessor()
    print("Starting data processing with security vulnerabilities...") 
    user_data = processor.fetch_user_data(1)
    api_result = processor.call_external_api({"test": "data"})
    print("Processing complete (with security issues)")

if __name__ == "__main__":    
    main()