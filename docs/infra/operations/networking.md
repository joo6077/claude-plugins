---
title: 네트워킹
version: 0.1.0
last_updated: 2026-04-04
---

# 네트워킹

VPC/서브넷, CIDR, NAT, 보안 그룹/NACL, DNS, 로드 밸런서(ALB/NLB), CDN, 네트워크 디버깅을 다룬다.

---

## 원칙

### 1. VPC는 region 경계, subnet은 AZ 경계로 설계한다

VPC는 하나의 AWS 리전에 묶이며, 서브넷은 단일 가용 영역(AZ)에 배치된다. 이 경계를 기준으로 네트워크를 나누면 장애 격리와 트래픽 흐름이 명확해진다. Public subnet(인터넷 게이트웨이 연결), Private subnet(NAT 경유), Isolated subnet(외부 접근 차단) 세 유형을 AZ마다 대칭 배치하는 것이 기본 패턴이다.

> **출처:** [AWS — VPC Subnet Basics](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-subnet-basics.html)

### 2. CIDR은 비중첩, 성장 여유, 멀티리전/온프레 연동까지 고려한다

VPC CIDR 블록을 설계할 때 다른 VPC, 온프레미스 네트워크, 향후 피어링/Transit Gateway 대상과 겹치지 않아야 한다. RFC 1918 대역(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)에서 할당하되, 확장 여유를 확보한다. 서브넷은 워크로드별 IP 소모량을 예측하여 크기를 정한다.

> **출처:** [AWS — Subnet Sizing](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-sizing.html)

### 3. NAT Gateway는 가용성 우선 시 AZ별 배치한다

단일 NAT Gateway는 단일 AZ 장애 시 해당 AZ의 Private subnet뿐 아니라 다른 AZ의 아웃바운드까지 중단시킬 수 있다. 고가용성이 필요하면 각 AZ에 NAT Gateway를 배치하고, 해당 AZ의 Private subnet 라우팅 테이블이 같은 AZ의 NAT를 가리키도록 설정한다.

> **출처:** [AWS — NAT Gateway Basics](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-basics.html)

### 4. Security Group은 stateful 인스턴스 경계, NACL은 stateless 서브넷 경계로 역할을 분리한다

Security Group(SG)은 인스턴스(ENI) 수준에서 허용 규칙만 정의하며 stateful이다(응답 트래픽 자동 허용). NACL은 서브넷 수준에서 허용/거부 규칙을 모두 정의하며 stateless이다(인바운드·아웃바운드 각각 명시). 일반적으로 SG로 세밀한 접근 제어를 하고, NACL은 서브넷 단위 방어벽(특정 IP 블록 차단 등)으로 사용한다.

> **출처:** [AWS — Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)

### 5. ALB는 L7 라우팅, NLB는 L4 고성능/정적 IP에 사용한다

Application Load Balancer(ALB)는 HTTP/HTTPS 요청을 호스트명, 경로, 헤더 등으로 라우팅한다. Network Load Balancer(NLB)는 TCP/UDP/TLS를 처리하며 초저지연, 고 TPS, 정적 IP/Elastic IP가 필요한 경우에 적합하다. Classic Load Balancer(CLB)는 레거시이며 신규 설계에서 사용하지 않는다.

> **출처:** [AWS — Application Load Balancer Introduction](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html)

### 6. DNS와 LB는 멀티AZ, 헬스체크, 글로벌 엔트리포인트를 우선한다

Route 53 헬스체크 + Failover/Weighted 라우팅으로 AZ 또는 리전 장애에 자동 대응한다. LB는 반드시 2개 이상 AZ에 걸쳐 배포하며, 대상 그룹 헬스체크로 비정상 인스턴스를 자동 제외한다. CloudFront/Global Accelerator를 글로벌 엔트리포인트로 활용하면 사용자 근접 엣지에서 트래픽을 수신한다.

> **출처:** [AWS — What Is Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)

### 7. 네트워크 디버깅은 dig/traceroute/tcpdump를 계층별로 사용한다

DNS 해석 문제는 `dig`(또는 `nslookup`), 경로 문제는 `traceroute`(`mtr`), 패킷 수준 문제는 `tcpdump`/`Wireshark`로 진단한다. VPC Flow Logs는 SG/NACL 거부를 확인하는 데 유용하다. 문제 계층을 먼저 특정하고 해당 계층의 도구를 사용해야 효율적이다.

> **출처:** [man7.org — traceroute(8)](https://man7.org/linux/man-pages/man8/traceroute.8.html)

---

## 수치/기준값

- AWS VPC CIDR: /16(65,536 IP) ~ /28(16 IP) 범위로 지정 가능
- AWS는 각 서브넷에서 처음 4개 + 마지막 1개 = **5개 IP를 예약**한다 (네트워크, VPC 라우터, DNS, 예약, 브로드캐스트)
- GCP는 각 서브넷에서 **4개 IP**가 사용 불가 (네트워크, 게이트웨이, 예약 2개)
- ALB는 최소 **2개 AZ**의 서브넷에 배치해야 하며, 각 서브넷은 **/27 이상**(32 IP) + 8개 이상 free IP 권장
- NLB는 AZ당 하나의 정적 IP(또는 Elastic IP) 할당 가능
- NAT Gateway 대역폭: 기본 5 Gbps, 최대 100 Gbps까지 자동 확장

---

## 안티패턴

- **겹치는 RFC 1918 대역 무계획 사용**: VPC 피어링, Transit Gateway, VPN 연동 시 CIDR 충돌로 라우팅 불가. 사전에 IP 대역 레지스트리를 관리한다
- **단일 NAT Gateway에 여러 AZ 의존**: 해당 AZ 장애 시 모든 Private subnet의 아웃바운드 중단. AZ별 NAT 배치가 기본
- **SG와 NACL 중복 과설계**: 동일한 규칙을 양쪽에 복제하면 유지보수 부담만 증가. SG는 세밀한 허용, NACL은 서브넷 단위 거부로 역할 분리
- **ALB/NLB를 익숙함만으로 선택**: L7 기능이 필요 없는데 ALB를 쓰거나, 정적 IP가 필요한데 ALB를 고집하는 사례. 요구사항에 맞게 선택
- **DNS TTL과 장애 전파 무고려**: TTL이 길면 장애 전환(failover) 반영이 늦고, TTL이 너무 짧으면 DNS 쿼리 비용과 지연 증가

---

## Gotchas

- AWS는 서브넷의 브로드캐스트 주소(마지막 IP)도 예약한다. /28 서브넷은 16개 중 11개만 사용 가능
- ALB 서브넷의 free IP가 부족하면 ALB 노드 스케일링이 실패한다. 트래픽 급증 시 503 에러로 나타남
- NACL은 stateless이므로 아웃바운드에 ephemeral port(1024~65535) 허용 규칙이 빠지면 응답 패킷이 차단된다. SG에서 허용해도 NACL에서 막히면 통과 불가
- `traceroute`만으로 애플리케이션 계층 장애를 단정하면 안 된다. 네트워크 경로가 정상이어도 앱, DNS, TLS 계층에서 문제가 발생할 수 있다
- VPC Flow Logs는 ACCEPT/REJECT만 기록하며 패킷 내용은 포함하지 않는다. 내용 분석이 필요하면 Traffic Mirroring 또는 tcpdump를 사용한다
