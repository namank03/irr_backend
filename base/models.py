from django.db import models


class File(models.Model):
    """Model definition for File."""

    file = models.FileField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        """Meta definition for File."""

        ordering = ('-created_at',)
