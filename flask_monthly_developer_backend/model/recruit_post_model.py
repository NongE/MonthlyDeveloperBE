from flask_restx import fields, Namespace, reqparse

class RecruitPostModel():
    recruit_ns = Namespace("About recruit post", description="팀 구인 관련 게시물 작성 API")

    recruit_post_model = recruit_ns.model('recruit post model', {
        'recruit_title': fields.String(description='recruit title', required=True),
        'recruit_author': fields.String(description='recruit author', required=True),
        'recruit_contents': fields.String(description='recruit contents', required=True),
        'recruit_tags': fields.List(fields.String, description='recruit tags', required=False),
        'recruit_state': fields.String(description='recruit state', required=True),
    })

    recruit_update_post_model = recruit_ns.model('recruit post model', {
        'recruit_post_id': fields.Integer(description='recruit post id', required=True),
        'recruit_title': fields.String(description='recruit title', required=True),
        'recruit_author': fields.String(description='recruit author', required=True),
        'recruit_contents': fields.String(description='recruit contents', required=True),
        'recruit_tags': fields.List(fields.String, description='recruit tags', required=False),
        'recruit_state': fields.String(description='recruit state', required=True),
    })

    search_parse = reqparse.RequestParser()
    search_parse.add_argument("recruit_search_method", type=str, help="게시글 찾는 방법")
    search_parse.add_argument("recruit_search_word", type=str, help="게시글 단어")