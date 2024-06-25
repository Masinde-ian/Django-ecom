from .models import Category, Condition


# context_processors.py
def global_context(request):
    return {
        'categorys': Category.objects.all(),
        'conditions': Condition.objects.all(),
        # Add any other data you want to include globally
    }
