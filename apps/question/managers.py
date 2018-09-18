import random
from django.db import models


class QuestionManager(models.Manager):

    def _get_allowed_question_queryset(self, task_id, answered_question_ids):
        return self.filter(task_id=task_id, status='unresolved').exclude(id__in=answered_question_ids)

    def get_random_question(self, task_id, answered_question_ids):
        if answered_question_ids:
            allowed_questions = self._get_allowed_question_queryset(task_id, answered_question_ids)
        else:
            allowed_questions = self.filter(task_id=task_id, status='unresolved')
        last = allowed_questions.count() - 1 if allowed_questions.count() else 0
        if last:
            index = random.randint(0, last)
        else:
            index = 0
        try:
            return allowed_questions[index]
        except IndexError:
            return self.all()[index]

    def get_question_by_code(self, code):
        return self.get(code=code)


class AnswerManager(models.Manager):

    def get_answered_question_ids(self, user_id,  task_id, question_id):
        # 不能再做的题目id list (提交待审核的, 审核通过的)
        return self.filter(user_id=user_id,
                           task_id=task_id,
                           question_id=question_id).exclude(status="审核未通过").values_list('question_id', flat=True)

    def get_user_finished_count(self, user_id,  task_id):
        return self.filter(user_id=user_id, task_id=task_id).count()


class AttachmentManager(models.Manager):

    def get_current_user_answered_question_ids(self, task_id, user_id):
        """获取当前用户当前任务下的已经做过的题目id list（适用于图片上传类任务）"""
        return self.filter(task_id=task_id, created_by=user_id).values_list('question_id', flat=True)
