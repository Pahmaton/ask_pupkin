import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from tqdm import tqdm

from app.models import Answer, AnswerLike, Profile, Question, QuestionLike, Tag

fake = Faker()

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        num_users = ratio
        num_tags = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_likes = ratio * 200

        self.stdout.write(self.style.SUCCESS(f"Generating test data with ratio={ratio}..."))

        self.stdout.write("Creating users and profiles...")
        users = [User(username=f'user_{i}', email=f'user_{i}@example.com') for i in range(num_users)]
        User.objects.bulk_create(users, batch_size=5000)

        profiles = [Profile(user=u, rating=random.randint(0, 1000)) for u in User.objects.all()]
        Profile.objects.bulk_create(profiles, batch_size=5000)

        all_profiles = list(Profile.objects.all())

        self.stdout.write("Creating tags...")
        tags = [Tag(name=f'tag_{i}') for i in range(num_tags)]
        Tag.objects.bulk_create(tags, batch_size=5000)
        all_tags = list(Tag.objects.all())

        self.stdout.write("Creating questions...")
        questions = []
        for i in tqdm(range(num_questions)):
            author = random.choice(all_profiles)
            questions.append(
                Question(
                    title=fake.sentence(nb_words=6),
                    text=fake.text(max_nb_chars=300),
                    author=author,
                    rating=random.randint(-50, 1000),
                )
            )
        Question.objects.bulk_create(questions, batch_size=5000)
        all_questions = list(Question.objects.all())

        self.stdout.write("Assigning tags to questions...")
        for q in tqdm(all_questions):
            q.tags.add(*random.sample(all_tags, random.randint(1, 5)))

        self.stdout.write("Creating answers...")
        answers = []
        for i in tqdm(range(num_answers)):
            question = random.choice(all_questions)
            author = random.choice(all_profiles)
            answers.append(
                Answer(
                    question=question,
                    author=author,
                    text=fake.text(max_nb_chars=200),
                    rating=random.randint(-10, 200),
                )
            )
        Answer.objects.bulk_create(answers, batch_size=5000)
        all_answers = list(Answer.objects.all())

        self.stdout.write("Creating likes...")

        qlikes = []
        alikes = []

        num_qlikes = num_likes // 2
        num_alikes = num_likes - num_qlikes

        q_pairs = set()
        while len(q_pairs) < num_qlikes:
            user = random.choice(all_profiles)
            question = random.choice(all_questions)
            pair = (user.id, question.id)
            if pair not in q_pairs:
                q_pairs.add(pair)
                qlikes.append(QuestionLike(user=user, question=question, value=random.choice([-1, 1])))

        a_pairs = set()
        while len(a_pairs) < num_alikes:
            user = random.choice(all_profiles)
            answer = random.choice(all_answers)
            pair = (user.id, answer.id)
            if pair not in a_pairs:
                a_pairs.add(pair)
                alikes.append(AnswerLike(user=user, answer=answer, value=random.choice([-1, 1])))

        QuestionLike.objects.bulk_create(qlikes, batch_size=5000)
        AnswerLike.objects.bulk_create(alikes, batch_size=5000)

        self.stdout.write(self.style.SUCCESS("Database successfully filled!"))
