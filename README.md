# TechBites

> 매주 한입씩 나누는 기술 이야기

TechBites는 각자 관심 있는 기술을 공부하고, 기록한 내용을 짧게 공유하는 미니 세미나 스타일의 스터디입니다.

탐구할 주제 또는 프로젝트 진행 중 생긴 문제 해결 과정 등, 공유하고자 하는 주제에 대해 블로그 포스트 또는 Notion web publish 글을 작성 후 공유합니다.
포스트 공유는 워크플로우 폼을 작성하거나, 수동으로 [템플릿](TEMPLATE.md)에 맞춰 본인의 디렉토리에 업로드합니다.

## Topics

주제에는 제한이 없습니다.

- Backend
- Cloud/Infra
- Cloud Native
- Troubleshooting
- Certification
- Development Tools
- Project Experience

## Members

| Name | GitHub                                     | Talks                | Blog                                                              |
| ---- | ------------------------------------------ | -------------------- | ----------------------------------------------------------------- |
| 김도현  | [@hyn128](https://github.com/hyn128) | [모아보기](./talks/hyn128/) | [hyn128.site](https://hyn128.site/?series=TechNotes)              |
| 이태경  | [@xoruddl](https://github.com/xoruddl)     | [모아보기](./talks/xoruddl/)   | [etakyung.com](https://etakyung.com)                              |
| 박성아  | [@sungahbak](https://github.com/sungahbak) | [모아보기](./talks/sungahbak/) | [haveagooddaysa.tistory.com](https://haveagooddaysa.tistory.com/category/Techbites) |


## How We Share

1. 자유롭게 주제를 선택합니다.
2. 공부한 내용을 개인 블로그 또는 Notion에 작성합니다.
3. Notion의 경우 `Web Publish`를 활성화해 링크로 공유가 가능하도록 합니다.
4. 워크플로우 입력 폼으로 포스트 정보를 등록합니다.
	-  또는 자신의 디렉터리에 포스트 정보를 담은 Markdown 파일을 추가합니다.
5. 변경사항이 기본 브랜치에 반영되면 포스트 기록이 자동으로 갱신됩니다.

## Register a Talk

아래 사진과 같이 GitHub Actions 입력 폼으로 포스트 정보를 등록할 수 있습니다.

<img width="1665" height="681" alt="image" src="https://github.com/user-attachments/assets/ec52d8b3-95fd-4bc1-8be1-929eb89b6f58" />


1. 주제에 대한 포스트를 개인 블로그 또는 Notion에 작성합니다.
2. 저장소의 **Actions** 탭에서 `Update talks`를 선택합니다.
3. `Run workflow`를 누르고 폼을 작성합니다.
4. 회차, 날짜, 주제, 글 URL을 입력합니다.
5. `Run workflow`를 눌러 실행합니다.
6. 완료되면 `talks/본인의 GitHub ID/` 디렉토리에 파일이 생성되고 아래의 Talks 표가 갱신됩니다.
7. 추가 자료가 있을 경우 `talks/본인의 Github Id/` 디렉토리에 `TechBites-MMDD-이름-주제.pdf`로 업로드 합니다.

발표자는 폼을 실행한 GitHub 계정으로 식별합니다. 
폼은 신규 포스트 등록 전용이며, 같은 작성자의 같은 회차는 중복 등록할 수 없습니다.
기존 내용을 수정하거나 삭제하려면 해당 Markdown 파일을 변경한 뒤 브랜치에 반영합니다.
이후 Talks 표도 자동으로 다시 생성됩니다.

Markdown 파일을 직접 추가하는 방식도 사용 가능합니다. [TEMPLATE.md](TEMPLATE.md)를 복사하여 `talks/본인의 GitHub ID/` 디렉토리에 저장한 뒤 `main` 브랜치에 반영합니다.

## Talks

<!-- TALKS:START -->

| 회차 | 날짜 | 발표자 | 주제 | 포스트 |
| --- | --- | --- | --- | --- |
| 1 | 2026-09-15 | 김도현 | 홈 서버로 이해하는 VPN | [글 보기](<https://hyn128.site/notes-09-techbites-vpn/>) |
| 1 | 2026-09-15 | 이태경 | 낙관적 락과 비관적 락 | [글 보기](<https://etakyung.com/posts/Backend-1-%EB%82%99%EA%B4%80%EC%A0%81-%EB%9D%BD%EA%B3%BC-%EB%B9%84%EA%B4%80%EC%A0%81-%EB%9D%BD/>) |
| 1 | 2026-09-15 | 박성아 | 연결이 비공개로 설정되어 있지 않습니다. - 인증서 검증 실패가 TLS handshake를 중단시키는 이유 | [글 보기](<https://haveagooddaysa.tistory.com/154>) |
| 2 | 2026-09-22 | 김도현 | Kubernetes Ingress의 한계와 Gateway API | [글 보기](<https://hyn128.site/notes-10-techbites-gateway-api/>) |

<!-- TALKS:END -->
