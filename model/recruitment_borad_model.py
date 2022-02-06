from flask_restx import fields, Namespace, reqparse


class RecruitmentBoardModel:
    recruitment_borad_ns = Namespace("Recruitment Board", description="팀 구인 관련 게시물 관련 API")

    token_parse = recruitment_borad_ns.parser()
    token_parse.add_argument('header', location='headers')

    search_parse = reqparse.RequestParser()
    search_parse.add_argument("search_method", type=str, help="게시글 찾는 방법")
    search_parse.add_argument("search_keyword", type=str, help="게시글 단어")
    search_parse.add_argument("page", type=int, default=1)

    create_post_model = recruitment_borad_ns.model('create post model', {
        'title': fields.String(description='Post Title', required=True),
        'author': fields.String(description='Post Author', required=True),
        'contents': fields.String(description='Post Contents', required=True),
        'tags': fields.List(fields.String, description='Post Tags', required=False),
        'state': fields.String(description='Post State', required=True),
    })

    recruit_update_model = recruitment_borad_ns.model('recruit update post model', {
        'recruit_post_id': fields.Integer(description='recruit post id', required=True),
        'recruit_title': fields.String(description='recruit title', required=True),
        'recruit_author': fields.String(description='recruit author', required=True),
        'recruit_contents': fields.String(description='recruit contents', required=True),
        'recruit_tags': fields.List(fields.String, description='recruit tags', required=False),
        'recruit_state': fields.String(description='recruit state', required=True),
    })

    recruit_delete_model = recruitment_borad_ns.model('recruit delete post model', {
        'recruit_post_id': fields.Integer(description='recruit post id', required=True)
    })
    