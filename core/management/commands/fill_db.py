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
                avatar="avatars/anon.png"
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


    def create_questions_with_realistic_likes(self, count, users, tags):
        """Создает вопросы с реалистичными лайками"""
        questions = []

        for i in range(count):
            user = random.choice(users)
            question = Question(
                title=f'Вопрос номер {i:06d}',
                description=f'Это подробное описание вопроса номер {i}. ' * 10,
                user=user,
                rating=0
            )
            questions.append(question)

        Question.objects.bulk_create(questions)
        created_questions = list(Question.objects.all())

        question_likes = []
        used_question_pairs = set()

        for question in created_questions:
            # Случайное количество пользователей, которые проголосуют за этот вопрос
            # Большинство вопросов получает мало голосов, некоторые - много
            voters_count = self.get_random_vote_count()

            # Выбираем случайных пользователей для голосования
            if voters_count > len(users):
                voters_count = len(users)

            if voters_count > 0:
                voters = random.sample(users, voters_count)

                # Каждый пользователь случайно ставит лайк или дизлайк
                for user in voters:
                    pair = (user.id, question.id)
                    if pair not in used_question_pairs:
                        # Вероятность лайка выше, чем дизлайка (как в реальности)
                        weight = 1 if random.random() < 0.8 else -1
                        like = QuestionLike(user=user, question=question, weight=weight)
                        question_likes.append(like)
                        used_question_pairs.add(pair)

                # Сохраняем пачками
                if len(question_likes) >= 500:
                    QuestionLike.objects.bulk_create(question_likes)
                    question_likes = []

        if question_likes:
            QuestionLike.objects.bulk_create(question_likes)

        # Обновляем рейтинги вопросов
        for question in created_questions:
            question.update_rating()

        # Создаем теги для вопросов
        question_tags = []
        for question in created_questions:
            question_tags_count = random.randint(1, min(3, len(tags)))
            selected_tags = random.sample(tags, question_tags_count)

            for tag in selected_tags:
                question_tag = QuestionTag(question=question, tag=tag)
                question_tags.append(question_tag)

        QuestionTag.objects.bulk_create(question_tags)
        return created_questions


    def get_random_vote_count(self):
        """Возвращает случайное количество голосов с реалистичным распределением"""
        # 50% вопросов: 0-10 голосов
        # 30% вопросов: 11-50 голосов
        # 15% вопросов: 51-200 голосов
        # 4% вопросов: 201-500 голосов
        # 1% вопросов: 501-1000 голосов

        rand = random.random()

        if rand < 0.5:
            return random.randint(0, 10)
        elif rand < 0.8:
            return random.randint(11, 50)
        elif rand < 0.95:
            return random.randint(51, 200)
        elif rand < 0.99:
            return random.randint(201, 500)
        else:
            return random.randint(501, 1000)


    def create_questions(self, count, users, tags):
        """Создает вопросы и связывает их с тегами"""
        return self.create_questions_with_realistic_likes(count, users, tags)


    def create_answers_with_realistic_likes(self, count, users, questions):
        """Создает ответы с реалистичными лайками"""
        answers = []

        for i in range(count):
            user = random.choice(users)
            question = random.choice(questions)

            answer = Answer(
                question=question,
                text=f'Это ответ номер {i} на вопрос. ' * 20,
                user=user,
                rating=0,
                is_accepted=random.choice([True, False]) and i % 10 == 0
            )
            answers.append(answer)

        Answer.objects.bulk_create(answers)
        created_answers = list(Answer.objects.all())

        answer_likes = []
        used_answer_pairs = set()

        for answer in created_answers:
            voters_count = self.get_random_answer_vote_count()

            if voters_count > len(users):
                voters_count = len(users)

            if voters_count > 0:
                voters = random.sample(users, voters_count)

                for user in voters:
                    pair = (user.id, answer.id)
                    if pair not in used_answer_pairs:
                        weight = 1 if random.random() < 0.9 else -1
                        like = AnswerLike(user=user, answer=answer, weight=weight)
                        answer_likes.append(like)
                        used_answer_pairs.add(pair)

                if len(answer_likes) >= 500:
                    AnswerLike.objects.bulk_create(answer_likes)
                    answer_likes = []

        if answer_likes:
            AnswerLike.objects.bulk_create(answer_likes)

        for answer in created_answers:
            answer.update_rating()

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


    def get_random_answer_vote_count(self):
        """Возвращает случайное количество голосов для ответов"""
        # 60% ответов: 0-5 голосов
        # 25% ответов: 6-20 голосов
        # 10% ответов: 21-100 голосов
        # 4% ответов: 101-300 голосов
        # 1% ответов: 301-500 голосов

        rand = random.random()

        if rand < 0.6:
            return random.randint(0, 5)
        elif rand < 0.85:
            return random.randint(6, 20)
        elif rand < 0.95:
            return random.randint(21, 100)
        elif rand < 0.99:
            return random.randint(101, 300)
        else:
            return random.randint(301, 500)


    def create_answers(self, count, users, questions):
        """Создает ответы на вопросы"""
        return self.create_answers_with_realistic_likes(count, users, questions)
