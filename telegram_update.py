import json, time, sys
from requests import get, post

token = str(sys.argv[1])
main = json.loads(get("https://api.github.com/repos/xtaodada/PagerMaid_Plugins/commits/master").content)
text = "#更新日志 #" + main['commit']['author']['name'].replace('_', '') + \
       ' \n\n🔨 [' + main['sha'][0:7] + '](https://github.com/Xtao-Labs/PagerMaid_Plugins/commit/' + \
       main['sha'] + '): ' + main['commit']['message']
push_content = {'chat_id': '-1001441461877', 'disable_web_page_preview': 'True', 'parse_mode': 'markdown',
                'text': text}
url = 'https://api.telegram.org/bot' + token + '/sendMessage'
try:
    main_req = post(url, data=push_content)
except:
    pass
push_content['chat_id'] = '-1001319957857'
time.sleep(1)
try:
    main_req = get(url, data=push_content)
except:
    pass
print(main['sha'] + " ok！")
