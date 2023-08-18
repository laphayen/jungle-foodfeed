# jungle-foodfeed

2023.08.08
좋아요만 구현, 댓글은 일단 보류 


<피드 생성 로직>
1. 지도 상에 가게 클릭
2. 화면 가운데에 모달창 뜸
3. 사용자가 직접 상호명을 입력하고 좋아요를 (누르거나/안누르거나 둘 다 가능) 누르고, 모달창 안의 생성하기 버튼 클릭하면 피드 생성
4. 만약 좋아요를 누르지 않았을 경우라도 좋아요 0으로 표시 된 상태로 피드 생성
   

name_give : 클라이언트 -> 서버로 보내줄때 상호명을 담은 변수

loca_give : 클라이언트 -> 서버로 보내줄때 위치를 담은 변수



name_receive : 클라가 서버로 전달한 name_give를 담은 변수

loca_receive : 클라가 서버로 전달한 loca_give 를 담은 변수



DB명 feeds
feeds = {'name', 'like', 'loca'}


2023.08.09
성태 : 클릭 이벤트
유정 : 피드 생성, 새로고침, 피드 업데이트 -> Jinja2
기찬 : 주소 찾아주기
공통 : JWT, jinja 공부, script 코드 정리, 변수명 readme에 업데이트 해주기(문서화)



시간되면 해야할 것 들
1. 피피티
2. 크롤링
3. 댓글
4. 좋아요 취소 기능
5. 아이디로 댓글 달기

   


**동작 상세
1. 검색
2. 마커 클릭
3. 주소 정보 저장
4. 좋아요 누르면 서버에 주소 정보, 상호명 전달


clickFeedLikeBtn()
-> 사이드바의 Feed의 좋아요 버튼을 눌렀을때 실행되는 함수. 모달창의 좋아요 버튼 아님!


> ### WEEK00 정글 입성 미니 프로젝트

### JWT 인증

1. 로그인

클라이언트의 로그인 요청이 서버로 들어오게 되면 서버에서는 access_token과 refresh_token을 생성하여 쿠키에 담아 클라이언트로 보낸다.


    access_token = create_access_token(identity=id)
    refresh_token = create_refresh_token(identity=id)
/

    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)

    
 클라이언트는 토큰을 받아 저장하고 있다가 요청을 보낼 때 마다 헤더에 access_token 을 포함하여 보낸다.
 
 만약에 access_token이 만료되었다면 서버는 클라이언트에게 refresh_token을 보내라고 response를 보낸다.
 
 서버는 refresh_token을 받아 그 토큰이 유효한지 체크한 후 새로운 access_token을 클라이언트에게 발급한다.
 
 2. 로그아웃

토큰의 기본 유효시간은 15분이다.
우리 조는 로그아웃 방식을 유효시간을 -1로 줘버려서 바로 토큰이 만료되게 하였다.
	 	
    response.set_cookie('refresh_token_cookie', '', expires=-1) 
    response.set_cookie('access_token_cookie', '', expires=-1) 
 
##  Jinja2
html을 넘겨줄 때 render_template을 이용.

    @app.route('/')
    def home():
       return render_template('login.html')


html을 넘겨줄 때 값을 넣어서 보내줄 수 있다.

    return render_template('index.html',id=session['id'])
    
이렇게 세션 id를 같이 넘겨주어 html에서도 id를 활용한 많을 것을 할 수 있다.

    < input id="id" hidden value="{{id}}">
    
html에서는 이렇게 {{변수 명}} 으로 변수를 넘겨받을 수 있다.
우리 조는 hidden 속성의 input 태그로 그 변수를 받게 하여 js에서도 id값을 활용하였다.


## MongoDB


1. 좋아요 누적 개수 0일 경우 피드가 삭제되며 DB에서도 삭제된다.

2.  맛집을 클릭하여 모달창을 띄워 좋아요를 클릭할 경우, DB에 해당 상호명, 도로명 주소, 좋아요 개수를 저장한다. 

3.  피드를 클릭하여 좋아요를 클릭할 경우 역시 DB에 해당 상호명, 도로명 주소, 좋아요 개수를 저장한다. 

4. 댓글을 생성하게 되면 로그인한 아이디를 가져와 DB -> comment 필드에 {id : comment} 딕셔너리 형태로 저장된다.
