from flask_restx import fields, Namespace, reqparse


class RecruitModel():
    recruit_ns = Namespace("About recruit post", description="팀 구인 관련 게시물 작성 API")

    token_parse = recruit_ns.parser()
    token_parse.add_argument('header', location='headers')

    search_parse = reqparse.RequestParser()
    search_parse.add_argument("search_method", type=str, help="게시글 찾는 방법")
    search_parse.add_argument("search_keyword", type=str, help="게시글 단어")
    search_parse.add_argument("page", type=int, default=1)

    recruit_model = recruit_ns.model('recruit post model', {
        'recruit_title': fields.String(description='recruit title', required=True),
        'recruit_author': fields.String(description='recruit author', required=True),
        'recruit_contents': fields.String(description='recruit contents', required=True),
        'recruit_tags': fields.List(fields.String, description='recruit tags', required=False),
        'recruit_state': fields.String(description='recruit state', required=True),
    })

    recruit_update_model = recruit_ns.model('recruit update post model', {
        'recruit_post_id': fields.Integer(description='recruit post id', required=True),
        'recruit_title': fields.String(description='recruit title', required=True),
        'recruit_author': fields.String(description='recruit author', required=True),
        'recruit_contents': fields.String(description='recruit contents', required=True),
        'recruit_tags': fields.List(fields.String, description='recruit tags', required=False),
        'recruit_state': fields.String(description='recruit state', required=True),
    })

    recruit_delete_model = recruit_ns.model('recruit delete post model', {
        'recruit_post_id': fields.Integer(description='recruit post id', required=True)
    })
    