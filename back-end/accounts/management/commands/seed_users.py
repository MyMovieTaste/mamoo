from django.core.management.base import BaseCommand
from django_seed import Seed
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from movies.models import Review, Movie
from accounts.models import User
from faker import Faker
import random

# raise TypeError(
# TypeError: Direct assignment to the forward side of a many-to-many set is prohibited. Use followings.set() instead.

# class Command(BaseCommand): 
#     help = "이 커맨드를 통해 랜덤한 테스트 유저 데이터를 만듭니다."
    
#     def add_arguments(self, parser): 
#         parser.add_argument( 
#             '--number', default=2, type=int, help="몇 명의 유저를 만드나") 
            
#     def handle(self, *args, **options): 
#         number = options.get('number') 
#         seeder = Seed.seeder()
#         users = User.objects.all()

#         seeder.add_entity(User, number, {
#             "username": lambda x: seeder.faker.first_name(),
#             "is_staff": lambda x: False,
#             "is_superuser": lambda x: False,
#             "date_joined": lambda x:  seeder.faker.date(),
#             "followings": lambda x:  random.choice(users),
#             "followers": lambda x:  random.choice(users),
#         })

#         seeder.execute()

#         self.stdout.write(self.style.SUCCESS(f"{number}명의 유저가 작성되었습니다."))

