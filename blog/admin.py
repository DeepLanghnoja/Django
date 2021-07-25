from django.contrib import admin
from blog.models import Post, Category, BlogComment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'timeStamp')
    list_filter = ('timeStamp', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author')
    radio_fields = {"category" : admin.HORIZONTAL}
    save_on_top = True
    list_per_page = 10
    exclude = ['author']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'timeStamp')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    save_on_top = True

admin.site.register(Category, CategoryAdmin)


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'post', 'timeStamp')
    search_fields = ('user',)

admin.site.register(BlogComment, BlogCommentAdmin)
