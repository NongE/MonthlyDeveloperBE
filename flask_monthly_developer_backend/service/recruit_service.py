from config import db_connector

def save_post(req_data):
    # 응답을 위한 Dict
    new_post_res = {}

    # 게시글의 고유 아이디 정보
    # 게시글 고유 아이디는 게시글의 등록 순서를 의미
    # 현재 k번 게시글까지 있다고 가정하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
    counter_db = db_connector.mongo.db.counter
    recruit_post_id = counter_db.find_one({"type": "recruit_post"}, {"_id":0})["counter"] + 1
    post_db = db_connector.mongo.db.recruit_post
    try:
        # 새 글 생성
        recruit_title = req_data.json.get("recruit_title")  # 제목
        recruit_author = req_data.json.get("recruit_author")  # 글쓴이
        recruit_contents = req_data.json.get('recruit_contents')  # 내용
        recruit_tags = req_data.json.get('recruit_tags')  # tags
        recruit_state = req_data.json.get('recruit_state')  # 상태

        newpost_recruit = {'recruit_post_id': recruit_post_id, 'recruit_title': recruit_title,
                        'recruit_author': recruit_author, 'recruit_contents': recruit_contents,
                        'recruit_tags': recruit_tags, 'recruit_state': recruit_state}
        
        for k, v in newpost_recruit.items():
            if k != "recruit_tags" and v == None:
                raise Exception("Missing Parameter")
    # 전달받은 Body 중에 누락된 내용이 있다면 Exception 발생
    # 제목, 글쓸이, 내용, 상태는 누락될 수 없음
    except:
        new_post_res = {
            "req_path": req_data.path,
            "req_result": "Missing Parameter"
        }
        return new_post_res
    
    try:
        # mongoDB에 추가
        # post = db.[colletion_name] # Collection에 접근 후
        # post.insert_one(newpost_recruit).inserted_id  #한 개 저장
        post_db.insert(newpost_recruit)
        # 현재 게시물 번호 업데이트
        counter_db.update_one({"type": "recruit_post"}, {"$set": {"counter": recruit_post_id}})
        new_post_res = {
            "req_path": req_data.path,
            "req_result": "Done"
        }
        return new_post_res
    # DB 저장 중 오류 발생 시 Exception
    except:
        new_post_res = {
            "req_path": req_data.path,
            "req_result": "Fail"
        }
        return new_post_res