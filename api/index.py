import json
import sys
import os
from pathlib import Path

# Add the root directory to Python path
sys.path.append(str(Path(__file__).parent))

from backend_api import app
from mangum import Mangum

# Wrap FastAPI app for Vercel
handler = Mangum(app)

def lambda_handler(event, context):
    """
    Vercel serverless function handler
    """
    try:
        return handler(event, context)
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': json.dumps({'error': str(e)})
        }
