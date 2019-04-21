from django.contrib import admin

# Register your models here.

from .models import Project   
from .models import User  
from .models import Task, File, QA, Feedback, Phase
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(User) 
admin.site.register(File)
admin.site.register(QA) 
admin.site.register(Feedback)
admin.site.register(Phase)
