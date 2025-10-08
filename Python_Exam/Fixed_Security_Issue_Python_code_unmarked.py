"""
Data Processing and Cloud Upload Service
SECURE VERSION with all vulnerabilities fixed
"""

import requests
import json
import sqlite3
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import bcrypt
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Validate all required env vars are present
REQUIRED_ENV_VARS = ['API_KEY', 'DATABASE_PASSWORD', 'AWS_REGION', 'SMTP_PASSWORD', 'ENCRYPTION_KEY']
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {missing_vars}")

# Load from environment (SECURE)
API_KEY = os.getenv('API_KEY')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY').encode()

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL')
WEBHOOK_ENDPOINT = os.getenv('WEBHOOK_ENDPOINT')
REQUEST_TIMEOUT = 30


def mask_credential(credential: str, visible_chars: int = 4) -> str:
    """Mask credential for safe logging"""
    if not credential or len(credential) <= visible_chars:
        return "****"
    return "*" * (len(credential) - visible_chars) + credential[-visible_chars:]


class SecureDataProcessor:
    def __init__(self):
        # Configure logging (INFO level for production)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Safe initialization logging
        self.logger.info(f"Initializing with API key: {mask_credential(API_KEY)}")
        
        # Secure session with SSL verification ENABLED
        self.session = requests.Session()
        self.session.verify = True
        
        # Encryption setup
        self.cipher = Fernet(ENCRYPTION_KEY)
    
    def connect_to_database(self):
        """Connect to database securely"""
        try:
            # Use environment variable for connection
            db_path = os.getenv('DATABASE_PATH', 'app_data.db')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Secure table schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    credit_card_encrypted TEXT,
                    ssn_encrypted TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            return conn, cursor
        except Exception as e:
            # Don't log credentials
            self.logger.error(f"Database connection failed: {type(e).__name__}")
            return None, None
    
    def fetch_user_data(self, user_id: int) -> Optional[tuple]:
        """Fetch user data with parameterized query (SQL injection safe)"""
        # Validate input
        if not isinstance(user_id, int) or user_id <= 0:
            self.logger.warning(f"Invalid user_id: {user_id}")
            return None
        
        conn, cursor = self.connect_to_database()
        if not cursor:
            return None
        
        # Parameterized query (SECURE)
        query = "SELECT * FROM user_data WHERE id = ?"
        
        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            self.logger.error(f"Query failed: {type(e).__name__}")
            return None
    
    def call_external_api(self, data: Dict[str, Any]) -> Optional[Dict]:
        """Make API calls with proper security and error handling"""
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'User-Agent': 'DataProcessor/2.0'
        }
        
        try:
            response = self.session.post(
                f"{API_BASE_URL}/process",
                headers=headers,
                json=data,
                verify=True,  # SSL verification ENABLED
                timeout=REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            self.logger.error("API request timeout")
            return None
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e.response.status_code}")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {type(e).__name__}")
            return None
    
    def upload_to_cloud(self, file_path: str, bucket_name: str) -> bool:
        """Upload files to cloud storage using IAM roles (SECURE)"""
        import boto3
        from botocore.exceptions import ClientError
        
        # Boto3 automatically reads:
        # - AWS_ACCESS_KEY_ID
        # - AWS_SECRET_ACCESS_KEY
        s3_client = boto3.client('s3', region_name=AWS_REGION)
        
        try:
            # Validate file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Upload with server-side encryption
            s3_client.upload_file(
                file_path,
                bucket_name,
                os.path.basename(file_path),
                ExtraArgs={'ServerSideEncryption': 'AES256'}
            )
            
            # Safe logging (don't expose bucket details)
            self.logger.info("File uploaded successfully")
            return True
            
        except ClientError as e:
            self.logger.error(f"S3 upload failed: {e.response['Error']['Code']}")
            return False
        except Exception as e:
            self.logger.error(f"Upload failed: {type(e).__name__}")
            return False
    
    def send_notification_email(self, recipient: str, subject: str, body: str) -> bool:
        """Send notification with secure SMTP"""
        import smtplib
        from email.mime.text import MIMEText
        import re
        
        # Validate email address
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, recipient):
            self.logger.warning(f"Invalid email address")
            return False
        
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        sender_email = os.getenv('SENDER_EMAIL')
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=REQUEST_TIMEOUT)
            server.starttls()
            server.login(sender_email, SMTP_PASSWORD)
            
            message = MIMEText(body)
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject
            
            server.send_message(message)
            server.quit()
            
            self.logger.info("Email sent successfully")
            return True
            
        except Exception as e:
            # Don't log password!
            self.logger.error(f"Email failed: {type(e).__name__}")
            return False
    
    def validate_webhook_data(self, webhook_data: Any) -> bool:
        """Validate webhook data"""
        if not isinstance(webhook_data, dict):
            return False
        
        if 'user_id' not in webhook_data or 'action' not in webhook_data:
            return False
        
        user_id = webhook_data.get('user_id')
        if not isinstance(user_id, int) or user_id <= 0:
            return False
        
        action = webhook_data.get('action')
        allowed_actions = ['create_user', 'update_user', 'delete_user']
        if action not in allowed_actions:
            return False
        
        return True
    
    def process_webhook_data(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook with validation (SECURE)"""
        # Validate input
        if not self.validate_webhook_data(webhook_data):
            self.logger.warning("Invalid webhook data received")
            return {"status": "error", "message": "Invalid data"}
        
        try:
            user_id = webhook_data.get('user_id')
            action = webhook_data.get('action')
            
            if action == 'delete_user':
                conn, cursor = self.connect_to_database()
                if not cursor:
                    return {"status": "error", "message": "Database error"}
                
                # Parameterized query (SECURE)
                query = "DELETE FROM user_data WHERE id = ?"
                cursor.execute(query, (user_id,))
                conn.commit()
                conn.close()
            
            # HTTPS with SSL verification
            response = requests.post(
                WEBHOOK_ENDPOINT,
                json=webhook_data,
                verify=True,
                timeout=REQUEST_TIMEOUT
            )
            
            return {"status": "processed", "webhook_response": response.status_code}
            
        except Exception as e:
            self.logger.error(f"Webhook processing failed: {type(e).__name__}")
            return {"status": "error", "message": "Processing failed"}
    
    # Encryption helpers
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        return hashed.decode()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()


def main():
    """Main function with secure practices"""
    processor = SecureDataProcessor()
    print("Starting secure data processing...")
    
    user_data = processor.fetch_user_data(1)
    api_result = processor.call_external_api({"test": "data"})
    
    print("Processing complete (SECURE)")


if __name__ == "__main__":
    main()