from django.contrib import admin
from .models import Post,Comments

class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','body','publish','created','updated','status']
    prepopulated_fields={'slug':('title',)}
    search_fields=('title','body')
    raw_id_fields=('author',)
    ordering=['status','publish']
    list_filter=('status','author')

class CommentsAdmin(admin.ModelAdmin):
    list_display=['name','email','post','body','created','updated','active']
    
    

admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentsAdmin)