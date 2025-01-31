from flask_marshmallow import Marshmallow
from marshmallow import fields
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.fields import Nested

from ..main import app
from .models import (Comment, Content, FBAccount, Photo, Post, PostStat, Proxy,
                     Subtask, Task, TaskKeyword, TaskSource, User, UserAgent,
                     UserJob, UserUniversity, Video, WorkerCredential)

ma = Marshmallow(app)


class SubtaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subtask
        include_relationships = True
        load_instance = True

    subtask_type = auto_field()
    start_time = auto_field()
    end_time = auto_field()
    status = auto_field()


class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True

    id = auto_field()
    interval = auto_field()
    retro = auto_field()
    until = auto_field()
    received_time = auto_field()
    finish_time = auto_field()
    status = auto_field()
    enabled = auto_field()


class TaskKeywordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TaskKeyword
        include_relationships = True
        load_instance = True

    id = auto_field()
    keyword = auto_field()
    task = Nested(TaskSchema)


class TaskSourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TaskSource
        include_relationships = True
        load_instance = True

    id = auto_field()
    source_id = auto_field()
    task = Nested(TaskSchema)


class UserUniversitySchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserUniversity
        include_relationships = True
        load_instance = True

    name = auto_field()
    link = auto_field()
    info = auto_field()


class UserJobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserJob
        include_relationships = True
        load_instance = True

    name = auto_field()
    link = auto_field()
    info = auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    name = auto_field()
    link = auto_field()
    sex = auto_field()
    city_of_birth = auto_field()
    current_city = auto_field()
    birthday = auto_field()
    fb_id = auto_field()

 #   universities = fields.Nested(UserUniversitySchema, many=True)
#    jobs = fields.Nested(UserJobSchema, many=True)


class StatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PostStat
        include_relationships = True
        load_instance = True

    likes = auto_field()
    comments = auto_field()
    shares = auto_field()


class VideoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Video
        include_relationships = True
        load_instance = True

    video_link = auto_field()


class PhotoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Photo
        include_relationships = True
        load_instance = True

    photo_link = auto_field()


class ContentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Content
        include_relationships = True
        load_instance = True

    text = auto_field()
    photos = fields.Pluck(PhotoSchema, "photo_link", many=True)
    videos = fields.Pluck(VideoSchema, "video_link", many=True)


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post
        include_relationships = True
        load_instance = True

    date = auto_field()
    last_time_updated = auto_field()
    fb_post_id = auto_field()
    fb_repost_id = auto_field()
    fb_repost_link = auto_field()
    content = Nested(ContentSchema)
    user = Nested(UserSchema)
    stat = Nested(StatSchema)


class WorkerCredentialSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkerCredential
        include_relationships = True
        load_instance = True

    id = auto_field()
    account_id = auto_field()
    proxy_id = auto_field()
    user_agent_id = auto_field()
    locked = auto_field()
    alive_timestamp = auto_field()


class AccountsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = FBAccount
        include_relationships = True
        load_instance = True

    login = auto_field()
    available = auto_field()


class ProxySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Proxy
        include_relationships = True
        load_instance = True

    host = auto_field()
    port = auto_field()
    login = auto_field()
    available = auto_field()
    last_time_checked = auto_field()
    expirationDate = auto_field()


class UserAgentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserAgent
        include_relationships = True
        load_instance = True

    userAgentData = auto_field()


class CommentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    date = auto_field()
    parent_comment_id = auto_field()
    content_id = auto_field()
    user_id = auto_field()
    post_id = auto_field()
    fb_comment_id = auto_field()
    likes_count = auto_field()
    content = Nested(ContentSchema)
    user = Nested(UserSchema)


class ShareSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Comment
        include_relationships = True
        load_instance = True

    post_id = auto_field()
    user_id = auto_field()
