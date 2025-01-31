from dateutil import parser

from flask import jsonify, request
from flask_restplus import Resource, abort

from ..api.posts_api import (post_keyword_request,
                             post_source_request,
                             posts_namespace)
from ..database import db
from ..database.mapping import PostSchema, UserSchema
from ..database.models import (Content, Photo, Post, Task, TaskKeyword,
                               TaskSource, User, Video)
from ..main import api, logger


@posts_namespace.route('/')
class Posts(Resource):
    def get(self):
        posts = Post.query.all()
        return jsonify(PostSchema().dump(posts, many=True))
#         users = User.query.all()
#         return jsonify(UserSchema().dump(users, many=True))


@posts_namespace.route('/<string:fb_post_id>')
class PostsById(Resource):
    def get(self, fb_post_id):
        post = Post.query.filter(Post.fb_post_id == fb_post_id).first()
        if post is None:
            abort(404, 'Post with fb_post_id={} not found'.format(fb_post_id))
        return PostSchema().dump(post)


@posts_namespace.route('/keyword')
class PostsKeyword(Resource):
    @api.expect(post_keyword_request)
    def post(self):
        data = request.get_json()
        keyword = data['keyword']

        dateTimeFrom = parser.parse(data['from'])
        limit = data['limit']
        page = data['page']
        offset = (page - 1) * limit

        count_all_posts = db.session.query(Post).join(
            TaskKeyword,
            Post.task_id == TaskKeyword.task_id
        ).filter(
            (TaskKeyword.keyword == keyword) & (Post.last_time_updated >= dateTimeFrom)
        ).count()

        results = db.session.query(
            Post,
            User,
            Task,
            Content
        ).join(
            TaskKeyword,
            Post.task_id == TaskKeyword.task_id
        ).join(
            User,
            Post.user_id == User.id
        ).join(
            Task,
            Task.id == TaskKeyword.task_id
        ).join(
            Content,
            Post.content_id == Content.id
        ).outerjoin(
            Video,
            Video.content_id == Content.id
        ).outerjoin(
            Photo,
            Photo.content_id == Content.id
        ).filter(
            (TaskKeyword.keyword == keyword) & (Post.last_time_updated >= dateTimeFrom)
        ).limit(limit).offset(offset).all()

        return post_results(count_all_posts, limit, page, results, keyword)


@posts_namespace.route('/source')
class PostsSource(Resource):
    @api.expect(post_source_request)
    def post(self):
        data = request.get_json()
        source_id = data['source_id']
        dateTimeFrom = data['from']

        limit = data['limit']
        page = data['page']
        offset = (page - 1) * limit

        count_all_posts = db.session.query(Post).join(
            TaskSource,
            Post.task_id == TaskSource.task_id
        ).filter(
            (TaskSource.source_id == source_id) &
            (Post.last_time_updated >= dateTimeFrom)
        ).count()

        results = db.session.query(
            Post,
            User,
            Task,
            Content
        ).join(
            TaskSource,
            Post.task_id == TaskSource.task_id
        ).join(
            User, Post.user_id == User.id
        ).join(
            Task,
            Task.id == TaskSource.task_id
        ).join(
            Content, Post.content_id == Content.id
        ).outerjoin(
            Video, Video.content_id == Content.id
        ).outerjoin(
            Photo, Photo.content_id == Content.id
        ).filter(
            (TaskSource.source_id == source_id) &
            (Post.last_time_updated >= dateTimeFrom)
        ).limit(limit).offset(offset).all()

        return post_results(count_all_posts, limit, page, results, source_id)


def post_results(count_all_posts, limit, page, results, search_parameter):
    json_list = []
    if len(results) > 0:
        for result in results:
            result_dict = {}
            result_dict['post'] = PostSchema().dump(result[0])
            json_list.append(result_dict)
    else:
        logger.log("There are no posts with {}".format(search_parameter))
    return jsonify(posts_results_data(count_all_posts, json_list, limit, page))


def posts_results_data(count_all_posts, json_list, limit, page):
    return {
        'items': json_list,
        'paging': {
            'count': count_all_posts,
            'pages_count': round(count_all_posts / limit),
            'page_size': limit,
            'page': page
        }}
