from flask_restx import fields, Namespace, reqparse


class RecruitmentBoardModel:
    recruitment_board_ns = Namespace("Recruitment Board", description="팀 구인 관련 게시물 관련 API")

    token_parse = recruitment_board_ns.parser()
    token_parse.add_argument('header', location='headers')

    create_post_model = recruitment_board_ns.model('create post model', {
        'title': fields.String(description='Post Title', required=True),
        'author': fields.String(description='Post Author', required=True),
        'contents': fields.String(description='Post Contents', required=True),
        'tags': fields.List(fields.String, description='Post Tags', required=False),
        'state': fields.String(description='Post State', required=True),
    })

    read_post_parser = reqparse.RequestParser()
    read_post_parser.add_argument("search_method", type=str, help="게시글 찾는 방법")
    read_post_parser.add_argument("search_keyword", type=str, help="게시글 단어")
    read_post_parser.add_argument("page", type=int, default=1)

    update_post_model = recruitment_board_ns.model('update post model', {
        'post_id': fields.Integer(description='Post id', required=True),
        'title': fields.String(description='Title', required=True),
        'author': fields.String(description='Post author', required=True),
        'contents': fields.String(description='Post contents', required=True),
        'tags': fields.List(fields.String, description='Post tags', required=False),
        'state': fields.String(description='Post state', required=True),
    })

    delete_post_model = recruitment_board_ns.model('delete post model', {
        'post_id': fields.Integer(description='Post id', required=True)
    })
    