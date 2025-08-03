"""
Video Profanity Replacer - Main Entry Point
Created by: Sriharsha Chittipothu
GitHub: https://github.com/sriharsha-2005
Email: sriharshachittipothu@gmail.com
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app import app
    logger.info("Flask app imported successfully")
except ImportError as e:
    logger.error(f"Failed to import Flask app: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"Unexpected error importing app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        logger.info(f"Starting Flask app on port {port}, debug={debug}")
        app.run(debug=debug, host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start Flask app: {e}")
        sys.exit(1)