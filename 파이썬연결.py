
import redis

## 레디스 연결
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

## 데이터 저장
rd.set("string", "Hello world")

## 데이터 가져오기
data = rd.get("string")
print(data)  ### Hello world

## 데이터 삭제
rd.delete("string")
print(rd.get("string"))  ### None

## 레디스 DB 데이터 전체 삭제
rd.flushdb()


