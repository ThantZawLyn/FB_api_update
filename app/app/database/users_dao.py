from ..database import db, dbro
from ..database.mapping import UserSchema
from ..database.models import Like, Post, Share, User


def get_users(data):
    limit = data['limit']
    page = data['page']
    offset = (page - 1) * limit

    count_all_users = dbro.session.query(User).filter(
        User.id.in_(data['source_ids'])
    ).count()

    users = dbro.session.query(User).filter(
        User.id.in_(data['source_ids'])
    ).limit(limit).offset(offset).all()

    return {'count_all_users': count_all_users,
            'users': UserSchema().dump(users, many=True)}

def get_users_keyword(data):
    limit = data['limit']
    page = data['page']
    offset = (page - 1) * limit

    count_all_users = dbro.session.query(User).filter(
        User.id.in_(data['keyword_ids'])
    ).count()

    users = dbro.session.query(User).filter(
        User.id.in_(data['keyword_ids'])
    ).limit(limit).offset(offset).all()

    return {'count_all_users': count_all_users,
            'users': UserSchema().dump(users, many=True)}


def get_users_shared_post(data):
    limit = data['limit']
    page = data['page']
    offset = (page - 1) * limit

    users_count = dbro.session.query(User).join(
        Share,
        Share.user_id == User.id
    ).join(
        Post,
        Post.id == Share.post_id
    ).filter(
        Post.fb_post_id == data['fb_post_id']
    ).count()

    results = dbro.session.query(User).join(
        Share,
        Share.user_id == User.id
    ).join(
        Post,
        Post.id == Share.post_id
    ).filter(
        Post.fb_post_id == data['fb_post_id']
    ).limit(limit).offset(offset).all()

    return user_results(users_count, limit, page, results)


def get_users_liked_post(data):
    limit = data['limit']
    page = data['page']
    offset = (page - 1) * limit

    users_count = dbro.session.query(User).join(
        Like,
        Like.user_id == User.id
    ).join(
        Post,
        Post.id == Like.post_id
    ).filter(
        Post.fb_post_id == data['fb_post_id']
    ).count()

    results = dbro.session.query(User).join(
        Like,
        Like.user_id == User.id
    ).join(
        Post,
        Post.id == Like.post_id
    ).filter(
        Post.fb_post_id == data['fb_post_id']
    ).limit(limit).offset(offset).all()

    return user_results(users_count, limit, page, results)


def user_results(users_count, limit, page, results):
    return users_results_data(
        users_count,
        UserSchema().dump(results, many=True),
        limit,
        page
    )


def users_results_data(users_count, json_list, limit, page):
    return {'users': json_list,
            'paging': {
                'count': users_count,
                'pages_count': round(users_count / limit),
                'page_size': limit,
                'page': page
            }}
