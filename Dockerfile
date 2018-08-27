# FROM jawonchoo/health-report-slack
# ## ssh 접속을 위해 실행환경의 ssh info 복사
# COPY .ssh /root/.ssh
# COPY config /root/.ssh/config
# ## 아래처럼 cmd 를 넣어주면 자동으로 항상 원하는 channel에 post됨, token은 보안이 안전한 곳에서만 사용
# ENTRYPOINT ["/root/ceph-health/get_ceph_health.sh"]
# CMD ["test", "xoxp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"]

FROM ubuntu:16.04
RUN  apt update && \
     apt install python-pip -y && \
     pip install slacker && \
     mkdir -p /opt/ceph-health/data
COPY get_ceph_health.sh /opt/ceph-health/get_ceph_health.sh
COPY post.py /opt/ceph-health/post.py
