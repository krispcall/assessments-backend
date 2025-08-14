from django.db import models


class Book(models.Model):
    """
    Book model to store books details.
    Base classes:
        - Model
    Returns:
        None
    """
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    file = models.FileField(upload_to='books/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'book'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'