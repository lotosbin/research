
import json
P=json.load(open('personas_all.json'))
D=json.load(open('report_data.json'))
if isinstance(P,dict): P=P.get('personas',P.get('users',[]))
lines=['# 100 位模拟用户反馈（小红书卖手机壁纸）','',
 '> 基于小红书实抓 73 条评论、平台规则、竞品价格与卖家账本构造；每条反馈含身份、出价、顾虑、触发点与原话。',
 '','## 总览','',
 '- 会买：28 人｜可能买：40 人｜不买：32 人',
 '- 心理价中位数：5 元；愿付 9.9 元：23 人；一分不付：23 人',
 '- 顾虑 TOP：审美不合(17) / 生意不成立(17) / 尺寸不适配(16) / AI味(14) / 版权(13)',
 '- 触发 TOP：审美对味(44) / 机型适配(19) / 省时模板(19) / 原创可溯(18) / 商用授权(15)','',
 '## 100 条反馈','','']
cur=None
for p in P:
    b=p.get('bucket','')
    if b!=cur:
        cur=b; lines+=['### '+b,'','' ]
    lines+=['**'+p['name']+'** · '+str(p.get('age',''))+'岁 · '+p.get('gender','')+' · '+p.get('city','')+' · '+p.get('job','')+
      ' · '+p.get('intent','')+' · 心理价 '+str(p.get('price_ok',''))+' 元','',
      '> '+p.get('quote',''),'']
    if p.get('triggers'): lines+=['- 触发：'+'、'.join(p['triggers'])]
    if p.get('objections'): lines+=['- 顾虑：'+'、'.join(p['objections'])]
    if p.get('evidence'): lines+=['- 证据：'+'、'.join(p['evidence']) if isinstance(p['evidence'],list) else '- 证据：'+str(p['evidence'])]
    lines+=['','']
open('feedback_100.md','w').write('\n'.join(lines))
print('ok',len(P),'lines',len(lines))
