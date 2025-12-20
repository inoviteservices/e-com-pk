from django.db import models

class CheckoutEvent(models.Model):
    session_id = models.CharField(max_length=255)
    step = models.CharField(max_length=50)
    device = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session_id} - {self.step}"
