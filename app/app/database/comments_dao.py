from ..database import db, dbro
from ..database.mapping import CommentSchema, PostSchema
from ..database.models import Comment, Content, Photo, Post, Share, User, Video
from ..main import logger


def get_post_comments(data):
    limit = data['limit']
    page = data['page']
    offset = (page - 1) * limit

    fb_post_id = data['fb_post_id']
    post = dbro.session.query(Post).filter(Post.fb_post_id == fb_post_id).first()
    if not post:
        return {"message": "post with fb_post_id: {} not found".format(fb_post_id)}

    post_id = post.id
    comments_count = Comment.query.filter(Comment.post_id == post_id).count()

    results = dbro.session.query(Comment).join(
        Post,
        Comment.post_id == Post.id
    ).join(
        Content,
        Comment.content_id == Content.id
    ).join(
        User,
        Comment.user_id == User.id
    ).join(
        Video,
        Video.content_id == Content.id, isouter=False, full=True
    ).join(
        Photo,
        Photo.content_id == Content.id, isouter=False, full=True
    ).filter(
        Comment.post_id == post_id
    ).limit(limit).offset(offset).all()

    if len(results) > 0:
        return results_data(
            comments_count,
            PostSchema().dump(post),
            CommentSchema().dump(results, many=True),
            limit,
            page,
        )
    else:
        logger.log("Комментариев к посту с id " + str(post_id) + " не найдено")

    return results_data(0, PostSchema().dump(post), [], limit, page)


def results_data(comments_count, post, comments, limit, page):
    return {'post': post, 'comments': comments,
            'paging': {
                'count': comments_count,
                'pages_count': round(comments_count / limit),
                'page_size': limit,
                'page': page
            }}
