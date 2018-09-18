from apps.question.model_status import ATTACHMENT_TYPE, answer_status
from apps.question.models import Answer, Question, AnswerOption


def get_allow_question(question, user_id, task_id):
    # 不能再做的题目id list (提交待审核的, 审核通过的)
    answered_question_ids = Answer.objects.get_answered_question_ids(user_id=user_id,
                                                                     task_id=task_id,
                                                                     question_id=question.id)
    #  访问到不能做的题目，换一道该任务下还没做的
    if question.id in answered_question_ids:
        # 可做的题目
        question = Question.objects.get_random_question(task_id=task_id, answered_question_ids=answered_question_ids)
    return question


def get_question_return_content(question,user_id, task_id, task_name):
    return_content = dict()
    return_content['question'] = question
    return_content['task_id'] = task_id
    return_content['task_name'] = task_name
    return_content['finished_count'] = Answer.objects.get_user_finished_count(user_id=user_id, task_id=task_id)

    if AnswerOption.objects.filter(task_id=task_id).exists():
        answer_option = AnswerOption.objects.filter(task_id=task_id).order_by('position')
        return_content['answer_option'] = answer_option
    return return_content


def get_answer_dict(user, task_id, question_id):
    answer_dict = dict()
    answer_dict['user_id'] = user.id
    answer_dict['task_id'] = task_id
    answer_dict['question_id'] = question_id
    answer_dict['status'] = answer_status[0][0]
    return answer_dict


def get_answer_attachment_dict(file, user, task_id, question_id):
    attach_dict = dict()
    attach_dict['detail_type'] = ATTACHMENT_TYPE['answer']
    attach_dict['file_obj'] = file
    attach_dict['created_by'] = user.id
    attach_dict['task_id'] = task_id
    attach_dict['question_id'] = question_id
    attach_dict['status'] = '待审核'
    return attach_dict
