import hashlib
import sys

# Digital Watermark
WATERMARK = "Developed by Dr. Kaushik Sarkar, Director-IMACS | Forecast App 2025"
WATERMARK_HASH = hashlib.sha256(WATERMARK.encode()).hexdigest()

def verify_watermark():
    if hashlib.sha256(WATERMARK.encode()).hexdigest() != WATERMARK_HASH:
        print("Unauthorized modification detected! Exiting...")
        sys.exit(1)

verify_watermark()
