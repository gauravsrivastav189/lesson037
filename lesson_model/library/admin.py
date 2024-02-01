from django.contrib import admin
from .models import Profile,Author,Publisher,Book,Collection
# Register your models here.


@admin.register(Profile)
class Profile_admin(admin.ModelAdmin):
    list_display=['slug','email','username','phone','address']

admin.site.register(Author)
# class Author_admin(admin.ModelAdmin):
#     list_display=['slug','names']


admin.site.register(Publisher)



admin.site.register(Book)


admin.site.register(Collection)