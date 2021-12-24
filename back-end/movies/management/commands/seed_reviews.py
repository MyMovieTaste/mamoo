from re import T
from django.core.management.base import BaseCommand
from django_seed import Seed
from movies.models import Review, Movie
from accounts.models import User
# from faker import Faker
import random

from django.db.models import Q
class Command(BaseCommand): 
    help = "이 커맨드를 통해 랜덤한 테스트 리뷰 데이터를 만듭니다."
    
    def add_arguments(self, parser): 
        parser.add_argument( 
            '--number', default=100, type=int, help="몇 개의 리뷰를 만드나") 
            
    def handle(self, *args, **options): 
        number = options.get('number') 
        seeder = Seed.seeder()
        # fake = Faker('ko_KR')
        # 관리자 제외하고 리뷰 생성
        users = User.objects.exclude(Q(is_superuser=1) | Q(is_staff=1))
        movies = Movie.objects.all()

        seeder.add_entity(Review, number, {
            "content": lambda x: seeder.faker.paragraph(nb_sentences=1),
            "rank": lambda x: random.randint(1, 5),
            "created_at": lambda x:  seeder.faker.date(),
            "updated_at": lambda x:  seeder.faker.date(),
            "user": lambda x:  random.choice(users),
            "movie": lambda x:  random.choice(movies),
        })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number}개의 리뷰가 작성되었습니다."))
