from django.contrib import admin
from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'subscribed')
    readonly_fields = ('subscribed',)
    list_filter = ('username', 'first_name', 'last_name')

    @admin.display(description='Количество подписчиков')
    def subscribed(self, user):
        return user.subscribers.count()


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    list_filter = ('user', 'author')
