from django.test import TestCase
from django.urls import reverse
from .models import Presentation, Test, Question, Choice, TestAttempt
from django.contrib.auth.models import User


class CoreSmokeTests(TestCase):
    def test_home_status(self):
        res = self.client.get(reverse('core:home'))
        self.assertEqual(res.status_code, 200)

    def test_presentations_api_empty(self):
        res = self.client.get(reverse('core:api_presentations'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), [])

    def test_presentation_model_and_api(self):
        p = Presentation.objects.create(title='T1', description='d', is_published=True)
        res = self.client.get(reverse('core:api_presentations'))
        data = res.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'T1')


class TestGradingTests(TestCase):
    def setUp(self):
        # create a test with two questions
        self.test = Test.objects.create(title='Simple Test', description='Test', is_published=True)
        q1 = Question.objects.create(test=self.test, text='2+2=?', order=1, points=1, allow_multiple=False)
        c1 = Choice.objects.create(question=q1, text='3', is_correct=False)
        c2 = Choice.objects.create(question=q1, text='4', is_correct=True)

        q2 = Question.objects.create(test=self.test, text='Pick even numbers', order=2, points=2, allow_multiple=True)
        c3 = Choice.objects.create(question=q2, text='1', is_correct=False)
        c4 = Choice.objects.create(question=q2, text='2', is_correct=True)
        c5 = Choice.objects.create(question=q2, text='3', is_correct=False)
        c6 = Choice.objects.create(question=q2, text='4', is_correct=True)

    def test_full_correct_submission(self):
        # submit correct answers
        q1 = self.test.questions.first()
        q2 = self.test.questions.last()
        post = {
            f'q_{q1.id}': str(q1.choices.get(is_correct=True).id),
            f'q_{q2.id}': [str(c.id) for c in q2.choices.filter(is_correct=True)],
        }
        # start attempt via AJAX
        start = self.client.post(reverse('core:test_take', args=[self.test.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(start.status_code, 200)
        start_data = start.json()
        attempt_id = start_data['attempt_id']
        # submit answers to submit endpoint
        submit = self.client.post(reverse('core:attempt_submit', args=[attempt_id]), post)
        self.assertEqual(submit.status_code, 200)
        data = submit.json()
        attempt = TestAttempt.objects.get(pk=data['attempt_id'])
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.score, 3)

    def test_partial_incorrect_submission(self):
        q1 = self.test.questions.first()
        q2 = self.test.questions.last()
        # pick wrong answer for q1, partial for q2 (only one correct selected)
        wrong = q1.choices.filter(is_correct=False).first()
        q2_one = q2.choices.filter(is_correct=True).first()
        post = {
            f'q_{q1.id}': str(wrong.id),
            f'q_{q2.id}': [str(q2_one.id)],
        }
        start = self.client.post(reverse('core:test_take', args=[self.test.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(start.status_code, 200)
        attempt_id = start.json()['attempt_id']
        submit = self.client.post(reverse('core:attempt_submit', args=[attempt_id]), post)
        self.assertEqual(submit.status_code, 200)
        data = submit.json()
        attempt = TestAttempt.objects.get(pk=data['attempt_id'])
        # With our partial credit formula: q1=0, q2 has 1 of 2 correct selected -> credit = (1-0)/2 * 2 = 1
        # So expected score = 1
        self.assertEqual(attempt.score, 1)
