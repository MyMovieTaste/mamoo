# BackEnd

방의진



### 프로젝트 후기















### Githup 업로드 방법

1. `master` 브랜치에서 자신의 브랜치 생성 (브랜치명 mybranch라고 가정)

```bash
git branch mybranch
```

2. 자신의 브랜치로 이동

```bash
git checkout mybranch
```

3. 작업 후 브랜치에 업로드

```bash
git add .
git commit -m "..."
git push
```

4. `master` 브랜치로 이동

```bash
git checkout master
```

5. `master` 브랜치에 `newbranch` 변경사항 반영

```bash
git merge mybranch
```

### Github 받는 방법

1. 자신의 브랜치로 이동

```bash
git checkout mybranch
```

2. `master` 의 변경사항을 내 브랜치에 반영

```bash
git pull master
```

3. `conflict` 충돌 발생시 파일로 들어가서 수정
4. 수정한 완료하면 내 브랜치에 반영

```bash
git add .
git commit -m ""
#=> 이때 vim 창이 나타나면  :wq    로 종료
```

5. `master` 브랜치로 이동 후 마스터에 내 브랜치의 변경사항 반영 (위의 5번과 동일)