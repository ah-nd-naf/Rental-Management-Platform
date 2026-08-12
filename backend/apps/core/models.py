import uuid
from django.db import models

class BaseModel(models.Model):
    """
    Abstract base class with created_at and updated_at fields
    that every domain model inherits.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Soft delete foundation for later phases
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True