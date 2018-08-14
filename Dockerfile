FROM ceph-health:0.1.0
ENTRYPOINT ["/root/ceph-health/get_ceph_health.sh"]
# 아래처럼 cmd 를 넣어주면 자동으로 항상 원하는 channel에 post됨, token은 보안이 안전한 곳에서만 사용
#CMD ["<channel>", "<token>"]
