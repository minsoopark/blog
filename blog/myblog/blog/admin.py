from django.contrib import admin
from blog.models import Entries, Categories, TagModel, Comments


class EntriesAdmin(admin.ModelAdmin):
	list_display = ('id', 'Name', 'created', 'Title',)

class CategoriesAdmin(admin.ModelAdmin):
	list_display = ('id', 'Title',)

class TagModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'Title',)

class CommentsAdmin(admin.ModelAdmin):
	list_display = ('id', 'Entry', 'Name', 'Content',)

class UsersAdmin(admin.ModelAdmin):
	list_display = ('id', 'Name', 'Password',)

admin.site.register(Entries, EntriesAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(TagModel, TagModelAdmin)
admin.site.register(Comments, CommentsAdmin)