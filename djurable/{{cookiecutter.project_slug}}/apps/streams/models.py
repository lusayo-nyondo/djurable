from django.db import models

class StreamEvent(models.Model):
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Event {self.pk} at {self.received_at}'
