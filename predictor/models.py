from django.contrib.auth.models import User
from django.db import models

class StudentSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    coding = models.IntegerField()
    math = models.IntegerField()
    creativity = models.IntegerField()
    communication = models.IntegerField()
    academic_performance = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True)
    personality = models.CharField(max_length=100, blank=True)
    predicted_career = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} – {self.predicted_career} ({self.created_at.date()})"