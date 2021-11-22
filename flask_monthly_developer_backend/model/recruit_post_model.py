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

    search_parse = reqparse.RequestParser()
    search_parse.add_argument("recruit_all", type=str, help="게시글 번호")
    search_parse.add_argument("recruit_author", type=str, help="게시글 작성자")
    search_parse.add_argument("recruit_tags", type=str, help="게시글 태그")
    search_parse.add_argument("recruit_state", type=str, help="게시글 상태")