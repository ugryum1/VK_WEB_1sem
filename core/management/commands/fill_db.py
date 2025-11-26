import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from core.models import UserProfile
from questions.models import Tag, Question, QuestionTag, Answer, AnswerTag, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'


    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения')


    def handle(self, *args, **options):
        ratio = options['ratio']

        # Всегда очищаем базу перед заполнением
        self.clear_database()

        with transaction.atomic():
            users = self.create_users(ratio)
            tags = self.create_tags(ratio)
            questions = self.create_questions(ratio * 10, users, tags)
            answers = self.create_answers(ratio * 100, users, questions)
            self.create_question_likes(ratio * 100, users, questions)
            self.create_answer_likes(ratio * 100, users, answers)


    def clear_database(self):
        """Очищает все данные из базы"""
        QuestionLike.objects.all().delete()
        AnswerLike.objects.all().delete()
        AnswerTag.objects.all().delete()
        Answer.objects.all().delete()
        QuestionTag.objects.all().delete()
        Question.objects.all().delete()
        Tag.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()


    def create_users(self, count):
        """Создает пользователей и их профили"""
        users = []

        for i in range(count):
            username = f'user_{i}'
            email = f'user_{i}@example.com'

            user = User(
                username=username,
                email=email,
                first_name=f'First_{i}',
                last_name=f'Last_{i}',
                password='testpassword123',
                is_active=True
            )
            users.append(user)

        User.objects.bulk_create(users)
        created_users = list(User.objects.all())

        user_profiles = []
        for user in created_users:
            profile = UserProfile(
                user=user,
                name=user.username,
                avatar=f'avatar_{random.randint(1, 50)}.jpg'
            )
            user_profiles.append(profile)

        UserProfile.objects.bulk_create(user_profiles)
        return created_users


    def create_tags(self, count):
        """Создает теги"""
        tags = []
        for i in range(count):
            tag = Tag(title=f'тег_{i:04d}')
            tags.append(tag)

        Tag.objects.bulk_create(tags)
        return list(Tag.objects.all())


    def create_questions(self, count, users, tags):
        """Создает вопросы и связывает их с тегами"""
        questions = []

        for i in range(count):
            user = random.choice(users)
            question = Question(
                title=f'Вопрос номер {i:06d}',
                description=f'Это подробное описание вопроса номер {i}. ' * 10,
                user=user,
                rating=random.randint(-100, 1000)
            )
            questions.append(question)

        Question.objects.bulk_create(questions)
        created_questions = list(Question.objects.all())

        question_tags = []
        for question in created_questions:
            question_tags_count = random.randint(1, min(3, len(tags)))
            selected_tags = random.sample(tags, question_tags_count)

            for tag in selected_tags:
                question_tag = QuestionTag(question=question, tag=tag)
                question_tags.append(question_tag)

        QuestionTag.objects.bulk_create(question_tags)
        return created_questions


    def create_answers(self, count, users, questions):
        """Создает ответы на вопросы"""
        answers = []

        for i in range(count):
            user = random.choice(users)
            question = random.choice(questions)

            answer = Answer(
                question=question,
                text=f'Это ответ номер {i} на вопрос. ' * 20,
                user=user,
                rating=random.randint(-50, 500),
                is_accepted=random.choice([True, False]) and i % 10 == 0
            )
            answers.append(answer)

        Answer.objects.bulk_create(answers)
        created_answers = list(Answer.objects.all())

        tags = list(Tag.objects.all())
        answer_tags = []
        for answer in created_answers:
            if random.random() < 0.3 and tags:
                answer_tags_count = random.randint(1, min(2, len(tags)))
                selected_tags = random.sample(tags, answer_tags_count)

                for tag in selected_tags:
                    answer_tag = AnswerTag(answer=answer, tag=tag)
                    answer_tags.append(answer_tag)

        if answer_tags:
            AnswerTag.objects.bulk_create(answer_tags)

        return created_answers


    def create_question_likes(self, count, users, questions):
        """Создает лайки/дизлайки для вопросов"""
        likes = []
        used_pairs = set()

        created_likes = 0
        attempts = 0
        max_attempts = count * 5

        while created_likes < count and attempts < max_attempts:
            user = random.choice(users)
            question = random.choice(questions)
            weight = random.choice([1, -1])

            pair = (user.id, question.id)

            if pair not in used_pairs:
                like = QuestionLike(user=user, question=question, weight=weight)
                likes.append(like)
                used_pairs.add(pair)
                created_likes += 1

            attempts += 1

            if len(likes) >= 500:
                QuestionLike.objects.bulk_create(likes)
                likes = []

        if likes:
            QuestionLike.objects.bulk_create(likes)


    def create_answer_likes(self, count, users, answers):
        """Создает лайки/дизлайки для ответов"""
        likes = []
        used_pairs = set()

        created_likes = 0
        attempts = 0
        max_attempts = count * 5

        while created_likes < count and attempts < max_attempts:
            user = random.choice(users)
            answer = random.choice(answers)
            weight = random.choice([1, -1])

            pair = (user.id, answer.id)

            if pair not in used_pairs:
                like = AnswerLike(user=user, answer=answer, weight=weight)
                likes.append(like)
                used_pairs.add(pair)
                created_likes += 1

            attempts += 1

            if len(likes) >= 500:
                AnswerLike.objects.bulk_create(likes)
                likes = []

        if likes:
            AnswerLike.objects.bulk_create(likes)
