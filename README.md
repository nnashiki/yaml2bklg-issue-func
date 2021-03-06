# azfunctions-py-skelton
azure functions Python runner の skelton

## how to develop
- poetry を install する
- `poetry shell` で仮想環境に入る
- `poetry install` で必要なパッケージを install する
- `poetry run task test` で unit test を実行する
- `poetry run task fmt` で format を実行する 

## 環境変数 の指定
- export STORAGE_ACCOUNT_CONNECT_STR=<STORAGE_ACCOUNT_CONNECT_STR>

## deploy and run
- `poetry export -f requirements.txt --output requirements.txt` を実行して requirements.txt を書き出す
- VSCode から deploy する
- authLevel が function で設定してあるので、deploy された関数を実行するにはクエリパラメータ `code` を付ける必要がある

## 2022/05/10 時点で azure function に deploy して実施したテスト
- body を `` (非json形式)で request する
    - `can't parse body` が返る
- body を `{}` で request する
    - `need any body parameters` が返る
- body を `{"param_str": "hoge"}` で request する
    - `"msg": "field required" を含むエラーが返る`
- body を `{"param_str": "hoge", "param_int": 1}` で request する
    - 200 が返る

## refs
- [課題の追加 | Backlog Developer API | Nulab](https://developer.nulab.com/ja/docs/backlog/api/2/add-issue/#url)