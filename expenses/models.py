from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    is_custom = models.BooleanField(default=False)  # Пользовательская категория?
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # Чья категория?
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['name', 'user']  # Уникальное имя для каждого пользователя
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name
    
    @property
    def is_main_category(self):
        return self.parent is None
    
    @property
    def is_subcategory(self):
        return self.parent is not None
    
    def save(self, *args, **kwargs):
        # Проверяем лимит пользовательских категорий
        if self.is_custom and self.user:
            custom_count = Category.objects.filter(user=self.user, is_custom=True).count()
            if not self.pk:  # Новая запись
                if custom_count >= 30:
                    raise ValueError("Достигнут лимит пользовательских категорий (30)")
        super().save(*args, **kwargs)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} - {self.description}"
