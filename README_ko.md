# 🏎️ F1 빗길 궤적 이탈 시뮬레이션 (스즈카 턴 7)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)

> **Polymath Developer Python | Polymath Developer Automation Tool**

본 프로젝트는 2014년 일본 스즈카 서킷 던롭 커브(Turn 7)에서 발생한 줄스 비앙키 선수의 사고 데이터를 바탕으로, **F1 차량의 수막현상(Hydroplaning) 발생 시 물리적 궤적 이탈**을 구현한 파이썬 시뮬레이션입니다. 

복잡한 물리 엔진 대신 `NumPy`와 `Matplotlib`을 활용한 직관적인 운동학적 모델(Kinetic model)을 통해, 타이어가 접지력을 잃는 순간 800kg의 머신이 어떻게 관성의 법칙을 따라 밀려 나가는지 시각화합니다.

▶️ **[유튜브 영상으로 작동 원리 및 시연 보기](유튜브 링크 삽입)**

<br>

## ⭐ 코드만 쏙 가져가시려고요?

> 💡 **잠깐!** 이 코드가 학습이나 프로젝트에 도움이 되셨나요?
> 체리피커처럼 소스코드만 날름 가져가지 마시고, 양심에 귀 기울여 우측 상단의 **Star(⭐)** 를 하나 꾹 눌러주세요! 
> 개발자의 땀과 노력에 대한 최소한의, 그리고 최고의 예의입니다.

<br>

## 🛠️ 기술 스택 및 주요 기능

| 분류 | 사용 기술 / 설명 |
| :--- | :--- |
| **언어** | Python 3.10+ |
| **핵심 라이브러리** | `NumPy` (물리 및 궤적 벡터 계산)<br>`Matplotlib` (애니메이션 렌더링 및 GIF 저장)<br>`Tkinter` (경량 UI 팝업) |
| **주요 기능** | <ul><li>시간에 따른 F1 차량의 상태(속도, 횡가속도, x/y 좌표) 계산</li><li>궤적 변화를 보여주는 애니메이션 GIF (`bianchi_trajectory_sim.gif`) 백그라운드 렌더링</li><li>렌더링 완료 직후 시스템 기본 UI를 활용한 양심 자극 팝업 출력</li><li>Supabase를 활용한 프로그램 실행 통계 데이터 전송 (트래커 연동)</li></ul> |

<br>

[📝 **Google Colab에서 설치 없이 바로 실행해보기**](https://colab.research.google.com/drive/1QEWXuyZl3Agb_VB1PZJEuO_uNDb__RiF?usp=sharing)

## 🚀 실행 방법 (로컬 환경)

**1. 저장소 클론 (Clone)**
```bash
git clone [https://github.com/gohard-lab/bianchi_trajectory.git](https://github.com/gohard-lab/bianchi_trajectory.git)
cd bianchi_trajectory
```

**2. 가상환경 생성 및 의존성 설치 (uv 활용)**

```Bash
uv venv
uv pip install numpy matplotlib python-dotenv supabase requests
```

**3. 시뮬레이션 실행**

```Bash
uv run python bianchi_trajectory_sim.py
```

*⚠️ 주의사항 (트래커 연동) > 프로그램 실행 통계 기능을 정상적으로 작동시키려면 프로젝트 루트 폴더에 SUPABASE_URL과 SUPABASE_KEY가 포함된 .env 파일이 반드시 필요합니다.*
