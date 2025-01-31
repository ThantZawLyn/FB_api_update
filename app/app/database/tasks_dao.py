from datetime import datetime

from dateutil import parser

from sqlalchemy import false, func, or_, text, true

from ..database import db, dbro
from ..database.models import (Post, Subtask, SubtaskType, Task, TaskKeyword,
                               TaskSource, TaskStatus, User, WorkerCredential)
from ..main import TIMEOUT_BETWEEN_ACCOUNTS_WORK, logger


def create(data):
    task = Task(interval=data['interval'],
                retro=parser.parse(data['retro']),
                enabled=data['enabled'])
    if 'until' in data:
        task.until = data['until']

    db.session.add(task)
    db.session.commit()
    return task


def create_keyword(data):
    if has_task_keyword_by_keyword(data['keyword']):
        return False

    task = create(data)
    keyword = TaskKeyword(
        keyword=data['keyword'],
        task_id=task.id
    )
    db.session.add(keyword)
    db.session.commit()
    return keyword


def patch_task(task, data):
    if 'interval' in data:
        task.interval = data['interval']
    if 'retro' in data:
        task.retro = data['retro']
    if 'until' in data:
        task.until = data['until']
    if 'enabled' in data:
        task.enabled = data['enabled']


def patch_keyword(task_type, data):
    task_type = db.session.query(TaskKeyword).filter(
        TaskKeyword.id == task_type.id
    ).first()

    if 'keyword' in data:
        task_type.keyword = data['keyword']
    patch_task(task_type.task, data)
    db.session.commit()
    return task_type


def create_source(data):
    if has_task_source_by_source_id(data['source_id']):
        return False

    task = create(data)
    source = TaskSource(
        source_id=data['source_id'],
        task_id=task.id
    )
    db.session.add(source)
    db.session.commit()
    return source


def patch_source(task_type, data):
    task_type = db.session.query(TaskSource).filter(
        TaskSource.id == task_type.id
    ).first()
    if 'source_id' in data:
        task_type.source_id = data['source_id']

    patch_task(task_type.task, data)
    db.session.commit()
    return task_type


def get_tasks():
    return dbro.session.query(Task).all()
   

def get_task_sources():
    return dbro.session.query(TaskSource).all()


def get_task_keywords():
    return dbro.session.query(TaskKeyword).all()


def has_task_source_by_source_id(source_id):
    if dbro.session.query(TaskSource).filter(TaskSource.source_id == source_id).first():
        return True
    return False


def get_task_source(task_id):
    task_query = dbro.session.query(TaskSource).filter(TaskSource.id == task_id)
    return task_query.first()


def has_task_keyword_by_keyword(keyword):
    if dbro.session.query(TaskKeyword).filter(TaskKeyword.keyword == keyword).first():
        return True
    return False


def get_task_keyword(task_id):
    task_query = dbro.session.query(TaskKeyword).filter(TaskKeyword.id == task_id)
    return task_query.first()


def get_task(task_id):
    task_query = dbro.session.query(Task).filter(Task.id == task_id)
    return task_query.first()


def get_subtasks(task_id):
    subtasks = dbro.session.query(Subtask).join(
        Post,
        Post.id == Subtask.post_id
    ).join(
        Task,
        Task.id == Post.task_id
    ).filter(Task.id == task_id).all()

    return subtasks


def get_statistics():
    return dbro.session.query(
        func.count(Task.id),
        Task.status
    ).group_by(
        Task.status
    ).all()


def get_subtasks_statistics():
    return dbro.session.query(
        func.count(Subtask.id),
        Subtask.status
    ).group_by(
        Subtask.status
    ).all()


def get_subtasks_statistics_by_task(task_id):
    def get_base_query():
        return dbro.session.query(Subtask).join(
            Post,
            Post.id == Subtask.post_id
        ).filter(
            Post.task_id == task_id
        )

    all = get_base_query().count()
    in_progress = get_base_query().filter(
        Subtask.status == TaskStatus.in_progress
    ).count()
    failed = get_base_query().filter(
        Subtask.status == TaskStatus.failed
    ).count()
    success = get_base_query().filter(
        Subtask.status == TaskStatus.success
    ).count()

    comments = get_base_query().filter(
        Subtask.subtask_type == SubtaskType.comment
    ).count()
    shares = get_base_query().filter(
        Subtask.subtask_type == SubtaskType.share
    ).count()
    likes = get_base_query().filter(
        Subtask.subtask_type == SubtaskType.like
    ).count()
    users = get_base_query().filter(
        Subtask.subtask_type == SubtaskType.personal_page
    ).count()

    return all, in_progress, failed, success, comments, shares, likes, users


def change_task_status(task_id):
    task = db.session.query(Task).filter(Task.id == task_id).first()
    task.sent_time = datetime.now().isoformat()
    task.status = TaskStatus.in_queue
    db.session.commit()


def change_subtask_status(subtask):
    subtask.status = TaskStatus.in_queue
    db.session.commit()


def get_keywords_ready_to_sent():
    return dbro.session.query(TaskKeyword).join(
        Task,
        TaskKeyword.task_id == Task.id
    ).filter(
        text(
            '(tasks.received_time + (tasks.interval || \' minute\')::interval) < \'' + str(
                datetime.now()) + '\' and '
                                  'tasks.enabled = true and '
                                  '(tasks.status <> \'in_progress\' and tasks.status <> \'in_queue\' or tasks.status is Null)'
        )
    )


def get_sources_ready_to_sent():
    return dbro.session.query(TaskSource).join(
        Task,
        TaskSource.task_id == Task.id
    ).filter(
        text(
            '(tasks.received_time + (tasks.interval || \' minute\')::interval) < \'' + str(
                datetime.now()) + '\' and '
                                  'tasks.enabled = true and '
                                  '(tasks.status <> \'in_progress\' and tasks.status <> \'in_queue\' or tasks.status is Null)'
        )
    )


def get_subtasks_ready_to_sent():
    return dbro.session.query(Subtask).filter(
        text('(subtasks.status <> \'in_progress\' and subtasks.status <> \'in_queue\' '
             'or subtasks.status is Null)'
             )
    )


def get_available_wc():
    available_wc_count = dbro.session.query(WorkerCredential).filter(
        WorkerCredential.locked == false()
    ).filter(
        WorkerCredential.inProgress == false()
    ).filter(text(
        '((worker_credentials.last_time_finished + \'' + str(
            TIMEOUT_BETWEEN_ACCOUNTS_WORK) + ' minute\'::interval) < \'' + str(
            datetime.now()) + "\' or worker_credentials.last_time_finished is Null)"
    )).count()
    logger.log("Available wc count to send: {}".format(available_wc_count))
    return available_wc_count
