
import os
import uuid
from django.utils.text import slugify

def logo_upload_to(instance, filename):
        # Extract file extension
        ext = filename.split('.')[-1].lower()

        # Slugify the base name (removes spaces, special chars)
        base_name = slugify(os.path.splitext(filename)[0])

        # Add a short unique ID to avoid collisions
        unique_name = f"{base_name}-{uuid.uuid4().hex[:8]}.{ext}"

        # Store inside the 'logos/' directory
        return os.path.join('logos', unique_name)
