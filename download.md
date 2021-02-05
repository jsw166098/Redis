# 레디스 설치

윈도우에서 레디스는 비공식적으로 설치가 가능하다. 일반 리눅수 서버에서 설치하는 것을 권장한다.

## 설치

~~~
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz  //압축을 푼다.
cd redis-stable  //생성된 redis-stable 디렉토리에 들어간다.
make  // 소스코드를 컴파일한다.
 
sudo make install  //redis 설치
 
redis-server  //redis  서버를 킨다.
~~~

* wget:  웹 서버로부터 콘텐츠를 가져오는 컴퓨터 프로그램
* tar, tar.gz: 리눅스 시스템에서으 압축 파일이다.

### wget 설치
* brew 를 이용한다.
~~~
brew install weget
~~~

---
## 출처
[Redis 소개와 설치 방법, 보안 설정 방법(ip 허용, 비밀번호 설정)등 빠르게 세팅하기](https://jeong-pro.tistory.com/139)
