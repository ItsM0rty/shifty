from django.core.management.base import BaseCommand
from myapp.models import User

class Command(BaseCommand):
    help = 'Approve and activate all existing users so they can log in.'

    def handle(self, *args, **options):
        users_to_approve = User.objects.all()
        count = 0
        for user in users_to_approve:
            if not user.approved or not user.is_active:
                user.approved = True
                user.is_active = True
                user.save()
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully approved and activated {count} user(s).')) 