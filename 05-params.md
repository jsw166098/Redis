# Params AOF

* APPENDONLY
* APPENDFILENAME
* APPENDFSYNC
* NO-APPENDFSYNC-ON-REWRITE
* AUTO-AOF-REWRITE-PERCENTAGE
* AUTO-AOF-REWRITE-MIN-SIZE
* AUTO-AOF-REWRITE-SPEC-TIME
* AOF-LOAD-TRUNCATED
* AOF-REWRITE-INCREMENTAL-FSYNC
* AOF-USE-RDB-PREAMBLE

~~~
1. AOF Params
    1.1 APPENDONLY
    1.2 APPENDFILENAME
    1.3 AOF-USE-RDB-PREAMBLE

2. fsync 함수 관련 Params
    2.1 APPENDFSYNC
    2.2 NO-APPENDFSYNC-ON-REWRITE

3. AOF Rewrite 동작 관련 Params
    3.1 AUTO-AOF-REWRITE-PERCENTAGE
    3.2 AUTO-AOF-REWRITE-MIN-SIZE
    3.3 AUTO-AOF-REWRITE-SPEC-TIME
    3.4 AUTO-REWRITE-INCREMENTAL-FSYNC
~~~

> 지속성 기법 관련 파라미터이며 parameter turing  

모두 레디스 설정 파일(redis.conf)에 존재한다.

---

## 1. AOF parmas
### 1.1 APPENDONLY
* 데이터를 Append Only File에 쓸지 여부를 정하는 파라미터. 
* yes/no로 설정 가능하며 디폴트는 no이다. 

#### 레디스 서버 시작시 읽어들이는 파일 순서

appendonly 파일과 dump.rdb 파일이 존재한다.
이때 appendonly yes이면 레디스 서버 시작 시 appendonly 파일을 읽어 들인다. appendonly yes이지만 appendonly 파일이 없고 dump.rdb 파일만 있어도 dump.rdb를 읽지 않는다. dumb.rdb 파일은 appendonly no일때만 dumb.rdb 파일을 읽어 들인다. 

## 1.2 APPENDFILENAME
* AOF파일(AppendOnlyFile)명을 지정하는 파라미터
* 위치는 dir에 지정된 working directory이다. 
* appendonly 파라미터 값이 yes일 대 적용된다. 

~~~
appendfilename appendonly.aof
~~~

## 1.3 AOF-USE-RDB-PREAMBLE 
* AOF rewrite시 AOF 파일을 RDB format으로 작성
* 작성 시간과 로드하는 시간을 줄인다. 또한 AOF 파일 사이즈도 줄일 수 있다.
* RDB format이 binary기 때문에 편집할 수 없다. 

~~~
aof-use-rdb-preamble yes (기본값)
aof-use-rdb-preamble no
~~~

## 1.4 AOF-LOAD-TRUNCATED 
* 레디스 시작시 AOF 파일을 메모리로 로드할 때 AOF 파일 끝이 잘려있는 경우에 대한 대처이다.
* Yes: 레디스는 가능한 많은 데이터를 로드하고 해당 내용을 로그에 남긴후 정상적으로 시작한다.
* No: 레디스는 오류를 남긴 후 중단한다. -> "redis-check-aof" 유틸리티를 사용하여 AOF 파일을 수정한다!

## 2. fsync() 함수 관련 params
### 2.1 APPENDFSYNC -> fsync() 함수 관련
* 레디스 설정 파일(redis.conf)에 존재한다.
* appendonly 파일에 **데이터가 쓰여지는 시점**을 정한다.
* **fsync()를 호출하는 시점**을 정한다.

디스크에 쓰는 시점은 appendfsync 파라미터로 정해진다. 세가지 옵션 제공
* always: 레디스 명령이 실행될 때 마다 디스크에 작성한다. 성능이 떨어진다.
* everysec: 데이터를 모아서 1초마다 디스크에 작성. 따라서 1초 이내의 데이터를 잃어 버릴 수 있다/성능과 보존 양면의 적절한 값/ 기본값
* no: 디스크에 쓰는 시점을 OS(리눅스)에 맡긴다. 
~~~
appendfsync always
appendfsync everysec <기본값>
appendfsync no
~~~
#### 데이터가 클라이언트에서 디스크로 쓰여지는 과정

1. 클라이언트가 레디스 서버로 데이터를 보낸다.- 데이터는 클라이너트 메모리에 있다.
2. 레디스 서버가 데이터를 받는다. - 데이터는 서버 메모리에 있다.
3. 레디스 서버가 데이터를 디스크에 쓰는 write()시스템 콜을 호출한다. - 데이터는 커널 버퍼에 있다.
4. 운영체제는 fsync() 시스템 콜을 호출해서 버퍼에 있는 데이터를 디스크 제어기에 쓴다. - 데이터는 케시에 있다.
5. 디스크 제어기는 물리적으로 디스크에 기록한다. 

### 2.2 NO-APPENDFSYNC-ON-REWRITE 
* 대량의 데이터를 디스크에 작성할 때 fsync() 수행 여부를 결정한다. 
* No-> 대량 쓰기 동안 설정한 대로 fsync()를 수행한다.
* Yes -> 대량 쓰기 동안 레디스 서버에서 fsync()를 수행하지 않고 운영체제에게 맡긴다. 30초 마다 한 번씩 fsync()가 수행된다. 이는 appendfsync를 No로 설정한 것과 같다. 
* 배경: 레디스 서버가 대량의 데이터를 작성할 때 이러한 메모리에 있는 데이터 크기와 디스크 성능에 따라 성능에 문제가 생길 수 있다. 따라서 디스크에 작성과 관련된 함수 fsync()를 관리하는 파라미터이다. 
~~~
no-appendfsync-on-rewrite no   (기본값)
no-appendfsync-on-rewrite yes
~~~

> 질문1 파라미터 값이 yes이면 fsync()를 수행하지 않고 운영체제에게 맡긴다.

## 3. AOF Rewrite 동작 관련 params
###  3.1 AUTO-AOF-REWRITE-PERCENTAGE  
* AOF Rewrite 동작 시점을 정한다.
* 이전에 다시쓰기한 AOF 파일 크기를 기준으로 100% 증가할 경우 다시쓰기를 한다.
* 만약 처음 다시쓰기를 하는 경우 레디스 서버 시작시 AOF 파일 크기를 기준으로 한다. 
~~~
auto-aof-rewrite-percentage 100 (기본값)
auto-aof-rewrite-percentage 0 (AOF 파일 다시쓰기를 하지 않음)
~~~

### 3.2 AUTO-AOF-REWRITE-MIN-SIZE
> 레디스 서버 시작시 파일 크기가 0일 경우만 적용된다. 
* **AOF Rewrite 동작을 하기 위한 AOF 파일의 최소 파라미터 값**을 알려준다.
* AOF 파일 크기가 설정값 이상이 되면 AOF Rewrite가 동작한다. 
* 레디스 서버 시작시 AOF 파일 크기가 0이었다면 64mb가 되어야 다시쓰기를 진행한다. 이후 부터는 auto-aof-rewrite-percentage값이 적용된다.
~~~
auto-aof-rewrite-min-size 64mb   (기본값)
auto-aof-rewrite-min-size 1gb
~~~

### 3.3 AUTO-AOF-REWRITE-SPEC-TIME 
> 서버 부하가 적은 시점을 지정해 AOF Rewrite 동작을 시점을 지정한다. 
* AOF Rewrite 동작을 하기 위한 시간을 지정한다.
* 퍼센트 지정 방법은 이미 서버 부하가 심한 지점에 rewrite가 실행되는 경우가 많아 서버 부하를 가중시키고 메모리 사용량이 많아지며 처리 성능이 저하된다. 
* 서버 부하가 적은 시점을 지정해서 동작을 관리할 수 있다. 
~~~
auto-aof-rewrite-percentage 03:00 (기본값)
~~~

### 3.4 AOF-REWRITE-INCREMENTAL-FSYNC 
> 디스크에 파일을 나눠서 작성한다. 
* AOF 파일을 Rewrite 할 때 디스크에 쓰는 fync를 32mb씩 나누어서 한다. 
* 대량 디스크 쓰기로 발생할 수 있는 문제를 피한다. 

---

# Params RDB

* SAVE
* STOP-WRITES-ON-BGSAVE-ERROR
* RDBCOMPRESSION
* RDBCHECKSUM
* DBFILENAME
* RDB-SAVE-INCREMENTAL-FSYNC

## 1. SAVE
* RDB 방식으로 디스크에 데이터를 저장할 때 저장 주기를 결정하는 파라미터
* 메인 메모리에 있는 데이터를 스냅샷을 통해 디스크에 저장하는 주기를 설정하는 파라미터
* 저장 주기는 시간과 변경된 데이터 개수로 설정
~~~
save 60 10000  -> 60초 안에 만개 이상 데이터가 변경되는 경우
save 300 10 -> 300초 안에 10개 이상 데이터가 변경되는 경우
save 900 1 900초 안에 1개 이상 데이터가 변경되는 경우
~~~ 

## 2. STOP-WRITES-ON-BGSAVE-ERROR
* **RDB 파일 저장이 실패했을 경우**(디렉토리에 쓰기 권한 없거나 여유 디스크 공간이 모자라서) 데이터를 받아 들일지 말지 정하는 파라미터
* 데이터를 받아들이지 않게 되어 RDB 파일 저장이 되지 않으면 관리자에게 문제 상황을 알리게 된다. 따라서 기본 값은 데이터를 받아들이지 않는 것이다.

## 3. RDBCOMPRESSION
* RDB 파일을 저장할 때 LZF 방식으로 압출할지 정한다. 
* 기본값은 yes이며 압축할 때 cpu를 사용하는데 이를 막고 압축 자체를 하지 않게 하려면 no로 설정하면 된다. 

## 4. RDBCHECKSUM
* RDB 파일이 정확히 저장되었는지 확인하는 방법이며 checksum을 파일 끝에 추가할지 말지를 정하는 파라미터 -> `checksum 추가 여부 결정`
* 파일의 무결성, 정확성을 높일 수 있으며 대신 로딩할때 10% 정도성능 저하될 수 있다.
* 기본 값은 yes이다. 

## 5. DBFILENAME
* RDB의 파일명을 지정한다.
* 디렉토리는 dir 파라미터에서 지정하는 곳에 저장된다.

## 6. RDB-SAVE-INCREMENTAL-FSYNC
* RDB 파일을 쓸 때 디스크에 쓰는 fsync를 32mb씩 나누어서 한다. 