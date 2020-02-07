from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Achievement
from django.db import models
from django.forms import TextInput, ModelForm


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('avatar_url', 'email', 'password')}),
        ('Personal info', {'fields': ('display_name', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)})
    )
    add_fieldsets = [
        (None, {'fields': ('email', 'password1', 'password2')}),
    ]

    list_display = ('email', 'display_name', 'is_staff')
    search_fields = ('email', 'display_name')
    ordering = ('email',)
    filter_horizontal = ()


DEFAULT_COLORS = ['007bff', '6c757d', '28a745', 'dc3545', 'ffc107', '17a2b8', 'f8f9fa', '343a40']


def colors_suggestions():
    """Generate list of suggested colors (Based on bootstrap defaults)."""
    results = []
    for color in DEFAULT_COLORS:
        text_color = Achievement._text_color(color)
        html = f'<button class="btn btn-sm" style="background:#{color}; color: #{text_color}" type="button" onclick="document.getElementById(\'id_color\').value=\'{color}\'">#{color}</button>'
        results.append(html)
    return ' '.join(results)


class AchievementForm(ModelForm):
    class Meta:
        model = Achievement
        fields = ('title', 'icon_class', 'color')
        help_texts = {
            'color': 'Background color in format: <em>DDDDDD</em> (e.g. 00ff00). <div class="mt-3">%s</div>' % colors_suggestions(),
            'icon_class': 'Font-awesome icon css class (e.g <em>fas fa-alien-monster</em>)'
        }


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css',
                'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
            )
        }
    list_display = ('preview', 'title', 'icon_class', 'color', 'text_color')
    list_display_links = ('title',)

    form = AchievementForm

    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }

    def preview(self, instance):
        return instance.to_html()