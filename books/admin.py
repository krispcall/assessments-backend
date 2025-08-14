from django.contrib import admin
from books.models import Book
from django.utils.translation import gettext_lazy as _

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    This class show the Book data into the admin panel
    Args:
        - BaseClass: ModelAdmin
    Returns:
        - None
    """
    list_display=['name','author','created_date','updated_date']
    list_display_links=['name','author','created_date','updated_date']
    list_filter = ['author',]
    search_fields = ['name',]
    readonly_fields = ('created_date', 'updated_date')

    fieldsets = (
        (_('Books Details'), {'fields': ( 'name','file')}),
        (_('Author Details'), {'fields': ( 'author',)}),
        (_('Important dates'), {'fields': ('created_date', 'updated_date')}),
    )