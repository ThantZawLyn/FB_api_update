from flask import jsonify, request
from flask_restplus import Resource, abort

from ..api.tasks_api import (subtask_response, task_keyword_patch_request,
                             task_keyword_request, task_keyword_response,
                             task_namespace, task_response,
                             task_source_patch_request, task_source_request,
                             task_source_response, task_update_request)
from ..database.mapping import (SubtaskSchema, TaskKeywordSchema, TaskSchema, UserSchema,
                                TaskSourceSchema)
from ..database.tasks_dao import (create_keyword, create_source,
                                  get_statistics, get_subtasks,
                                  get_subtasks_statistics,
                                  get_subtasks_statistics_by_task, get_task,
                                  get_task_keyword, get_task_keywords,
                                  get_task_source, get_task_sources, get_tasks,
                                  patch_keyword, patch_source, patch_task)
from ..main import api
from ..services.celery_service import send_keyword, send_source


@task_namespace.route('/keyword')
class KeywordCreate(Resource):
    def get(self):
        return TaskKeywordSchema().dump(get_task_keywords(), many=True)

    @api.marshal_with(task_keyword_response)
    @api.expect(task_keyword_request)
    def post(self):
        keyword = create_keyword(request.get_json())
        if not keyword:
            abort(405, 'Task has already exists')
        send_keyword(keyword.task_id)
        return TaskKeywordSchema().dump(keyword)


@task_namespace.route('/keyword/<int:task_id>')
class KeywordGet(Resource):
    @api.marshal_with(task_keyword_response)
    def get(self, task_id):
        task = self.get_task_keyword(task_id)
        return TaskKeywordSchema().dump(task)

    @api.marshal_with(task_keyword_response)
    @api.expect(task_keyword_patch_request)
    def patch(self, task_id):
        task = self.get_task_keyword(task_id)
        return TaskKeywordSchema().dump(
            patch_keyword(task, request.get_json())
        )

    def get_task_keyword(self, task_id):
        task = get_task_keyword(task_id)
        if task is None:
            abort(404, 'Task not found')
        return task


@task_namespace.route('/source')
class SourceCreate(Resource):
    def get(self):
        return TaskSourceSchema().dump(get_task_sources(), many=True)

    @api.marshal_with(task_source_response)
    @api.expect(task_source_request)
    def post(self):
        source = create_source(request.get_json())
        if not source:
            abort(405, 'Task already exists')

        send_source(source.task_id)
        return TaskSourceSchema().dump(source)


@task_namespace.route('/source/<int:task_id>')
class SourceGetUpdate(Resource):
    @api.marshal_with(task_source_response)
    def get(self, task_id):
        task = self.get_task_source(task_id)
        return TaskSourceSchema().dump(task)

    @api.marshal_with(task_source_response)
    @api.expect(task_source_patch_request)
    def patch(self, task_id):
        task = self.get_task_source(task_id)
        return TaskSourceSchema().dump(
            patch_source(task, request.get_json())
        )

    def get_task_source(self, task_id):
        task = get_task_source(task_id)
        if task is None:
            abort(404, 'Task not found')
        return task


@task_namespace.route('')
class GetTask(Resource):
    @api.marshal_with(task_response)
    def get(self):
        return TaskSchema().dump(get_tasks(), many=True)
        


@task_namespace.route('/<int:task_id>')
class Get(Resource):
    @api.marshal_with(task_response)
    def get(self, task_id):
        task = get_task(task_id)
        if task is None:
            abort(404, 'Task not found')
        return TaskSchema().dump(task)

    @api.marshal_with(task_response)
    @api.expect(task_update_request)
    def patch(self, task_id):
        task = get_task(task_id)
        if task is None:
            abort(404, 'Task not found')
        return TaskSchema().dump(
            patch_task(task, request.get_json())
        )


@task_namespace.route('/<int:task_id>/subtasks')
class GetSubtasks(Resource):
    @api.marshal_with(subtask_response)
    def get(self, task_id):
        subtasks = get_subtasks(task_id)
        return SubtaskSchema().dump(subtasks, many=True)


@task_namespace.route('/<int:task_id>/subtasks/stat')
class GetStatistics(Resource):
    def get(self, task_id):
        all, in_progress, failed, success, comments, shares, likes, users = get_subtasks_statistics_by_task(
            task_id)
        return jsonify(
            {"status": {
                "all": all, "in_progress": in_progress,
                "failed": failed, "success": success},
                "types": {
                    "likes": likes, "comments": comments, "shares": shares,
                    "users": users}}
        )


@task_namespace.route('/statistics')
class GetAllStatistics(Resource):
    def get(self):
        return jsonify(get_statistics())


@task_namespace.route('/subtasks/statistics')
class GetAllSubtaskStatistics(Resource):
    def get(self):
        return jsonify(get_subtasks_statistics())
