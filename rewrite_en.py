with open('app/templates/index.html', 'r') as f:
    content = f.read()

content = content.replace('スタンバイ...', 'Standby...')
content = content.replace('📝 上部エディタに反映して編集', '📝 エディタへ反映')
content = content.replace('初期化中...', 'Initializing...')
content = content.replace('キャンセルされました', 'Aborted')
content = content.replace('通信エラー', 'Connection Error')
content = content.replace('待機中', 'Standby')
content = content.replace('完了', 'Complete')
content = content.replace('エラー発生', 'Error')
content = content.replace('⚠️ ユーザーによって処理がキャンセルされました。', '[!] Process aborted by user.')
content = content.replace('通信エラーが発生しました: ', '[!] Connection error: ')

with open('app/templates/index.html', 'w') as f:
    f.write(content)
