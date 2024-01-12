from django.test import TestCase
from django.utils import timezone
# Create your tests here.
import datetime
from .models import Question
from django.urls import reverse
 
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        ## If no question we should show an error
        res = self.client.get(reverse("polls:index"))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No polls are available")
        self.assertQuerySetEqual(res.context["question_list"], [])

    def test_past_question(self):
        ## Old questions are displayed
        q = create_question(text="Old question", days=-30)
        res = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(res.context["question_list"], [q])

    def test_future_question(self):
        ## Test future questions
        q = create_question(text="New qustion", days=30)
        res = self.client.get(reverse("polls:index"))
        self.assertContains(res, "No polls are available.")
        self.assertQuerySetEqual(res.context["question_list"], [])

    def test_future_question_and_past_question(self):
        #Create a new and old question
        q = create_question(text="Past question.", days=-30)
        create_question(text="Future question.", days=30)
        res = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            res.context["question_list"],
            [q],
        )

    def test_two_past_questions(self):
        ## Create two questions
        q1 = create_question(text="Past question 1.", days=-30)
        q2 = create_question(text="Past question 2.", days=-5)
        res = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            res.context["question_list"],
            [q2, q1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        ## Create a future question and verify that the detail page gives a 404
        q = create_question(text="Future question.", days=5)
        url = reverse("polls:detail", args=(q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_old_question(self):
        ## create a old question and verify that the detail page displays the question
        q = create_question(text="Old question", days=-5)
        url = reverse("polls:detail", args=(q.id,) )
        res = self.client.get(url)
        self.assertContains(res, q.question_text)
