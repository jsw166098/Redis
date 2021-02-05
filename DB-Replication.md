# Data Replication

하나의 서버와 하나의 데이터베이스를 가질 경우 사용자가 많아지면 query를 처리하기 힘든 상황이 닥친다. 

* 두개의 이상의 DBMS 시스템을 Master/slave로 나눠서 동일한 데이터를 자장하는 방식
* 여러 개의 DB를 권한에 따라 수직적인 구조(Master-Slave)로 구축하는 방식
* Master Node는 쓰기 작업 만을 Slave Node는 읽기 작업 만을 처리한다.

* 비동기 방식으로 노드들 간의 데이터를 동기화한다.
* 데이터를 물리적으로 다른 서버 공간에 복제하는 일이다.
* 부하 분산 및 고가용성, 버전 테스트 등의 기능을 사용할 수 있다.
* 일반적으로 Writable한 Master Node에서 Readonly인 Slave로 이루어져 있다. 



# Clustering

* 여러 개의 DB를 수평적인 구조로 구축하는 방식
* 동기 방식으로 노드들 간의 데이터를 동기화 한다. 