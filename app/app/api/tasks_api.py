from flask_restplus import fields

from ..main import api

task_namespace = api.namespace('task', description='Task')

task_source_request = api.model('TaskSourceRequest', {
    'source_id': fields.String(required=True, description='Source Id'),
    'interval': fields.Integer(required=True, description='interval'),
    'retro': fields.DateTime(required=True, description='retro'),
    'until': fields.DateTime(required=False, description='until'),
    'enabled': fields.Boolean(required=True, description='enabled')
})

task_keyword_request = api.model('TaskKeywordRequest', {
    'keyword': fields.String(required=True, description='Source Id'),
    'interval': fields.Integer(required=True, description='interval'),
    'retro': fields.DateTime(required=True, description='retro'),
    'enabled': fields.Boolean(required=True, description='enabled')
})

task_update_request = api.model('TaskUpdateRequest', {
    'interval': fields.Integer(required=False, description='keyword'),
    'retro': fields.DateTime(required=False, description='keyword'),
    'until': fields.DateTime(required=False, description='keyword'),
    'enabled': fields.Boolean(required=False, description='keyword'),
})

task_response = api.model('TaskResponse', {
    'id': fields.Integer(readOnly=True, description='id'),
    'interval': fields.Integer(required=True, description='interval'),
    'retro': fields.DateTime(required=True, description='retro'),
    'until': fields.DateTime(required=False, description='until'),
    'sent_time': fields.DateTime(required=True, description='sent_time'),
    'received_time': fields.DateTime(required=True, description='received_time'),
    'finish_time': fields.DateTime(required=True, description='finish_time'),
    'status': fields.String(required=True, description='status'),
    'enabled': fields.Boolean(required=True, description='enabled')
})

subtask_response = api.model('SubTaskResponse', {
    'subtask_type': fields.String(required=True, description='subtask_type'),
    'start_time': fields.DateTime(required=True, description='start_time'),
    'end_time': fields.DateTime(required=True, description='end_time'),
    'status': fields.String(required=True, description='status')
})

task_keyword_patch_request = api.model('TaskKeywordPatchRequest', {
    'keyword': fields.String(required=False, description='keyword'),
    'interval': fields.Integer(required=False, description='interval'),
    'retro': fields.DateTime(required=False, description='retro'),
    'until': fields.DateTime(required=False, description='until'),
    'enabled': fields.Boolean(required=False, description='enabled'),
})

task_source_patch_request = api.model('TaskSourcePatchRequest', {
    'source_id': fields.String(required=False, description='source_id'),
    'interval': fields.Integer(required=False, description='interval'),
    'retro': fields.DateTime(required=False, description='retro'),
    'until': fields.DateTime(required=False, description='until'),
    'enabled': fields.Boolean(required=False, description='enabled'),
})

task_keyword_response = api.model('TaskKeywordResponse', {
    'id': fields.Integer(readOnly=True, description='Task'),
    'keyword': fields.String(required=True, description='keyword'),
    'task': fields.Nested(task_response),
})

task_source_response = api.model('TaskSourceResponse', {
    'id': fields.Integer(readOnly=True, description='Task'),
    'source_id': fields.String(required=True, description='Source Id'),
    'task': fields.Nested(task_response),
})
