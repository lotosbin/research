
import json, collections, statistics as st

P = json.load(open('personas_all.json'))
S = json.load(open('stats.json'))

prices=[1,2,3,5,7,9.9,12,15,20,30]
rev=[]
for pr in prices:
    n=sum(1 for p in P if p['price_ok']>=pr)
    buyers=round(n/100*1000)
    rev.append({'price':pr,'n':n,'buyers':buyers,'revenue':round(pr*buyers)})

GORDER=['A1-学生党','A2-职场白领','A3-二次元游戏','A4-追星','A5-国风中年','A6-极简审美','B1-白嫖转付费','B2-付费踩坑维权','B3-收藏型付费','C1-小卖家试水','C2-中腰部卖家','C3-老手与退场者','D1-壁纸号博主','D2-美学号博主','D3-搬运号博主','E1-手机壳店主','E2-素材站分成方','E3-法务合规','E4-设计接单方']
GDESC={
'A1-学生党':'钱包最紧，但对“真原图+尺寸对”最买账；安卓用户被边缘化',
'A2-职场白领':'单价天花板最高，买的是“体面”和“氛围感”；最怕花哨和错英文',
'A3-二次元游戏':'愿意为角色和清晰度花钱，但一眼能认出 AI，且免费渠道极多',
'A4-追星':'愿意为“排版功夫”付钱，自己图多但不会修；最恨图文不符',
'A5-国风中年':'真正的商用付费方：汉服店/民宿/茶室，要授权书，30 元也肯',
'A6-极简审美':'审美最挑剔，买“克制”和“留白”；设计师自己会做，愿付的是思路',
'B1-白嫖转付费':'被“关注求图”和缩略图骗过，肯为“直接存原图”破例',
'B2-付费踩坑维权':'被图文不符、AI冒充手绘伤过，只信“过程可溯”',
'B3-收藏型付费':'有付费习惯、存量最多，怕的是“买完不更新”',
'C1-小卖家试水':'月入一两百的真实底色；死于回消息、没复购、被限流',
'C2-中腰部卖家':'月入两千上下，靠定制与国风；最痛是侵权和 0.01 元',
'C3-老手与退场者':'懂行、肯为原创付高价，但一致劝你别入场',
'D1-壁纸号博主':'掌握“关注换图”涨粉法，自己不买图，只肯买“排版模板”',
'D2-美学号博主':'广告主视角，最在意商用授权与 AI 标识两难',
'D3-搬运号博主':'要的是分销与批量源包，不是零售',
'E1-手机壳店主':'赠品思维，要印刷级源文件+书面授权，单价压到 4-12',
'E2-素材站分成方':'要原创声明+分层文件，AI 直出过不了审',
'E3-法务合规':'AI 图难确权、字体模板连带风险，一票否决',
'E4-设计接单方':'68 元/张的定制才是真钱，批量包只当提案资料',
}
gstat={}
for p in P:
    g=gstat.setdefault(p['bucket'],{'n':0,'buy':0,'maybe':0,'no':0,'prices':[],'ids':[]})
    g['n']+=1; g['prices'].append(p['price_ok']); g['ids'].append(p['id'])
    g['buy' if p['intent']=='买' else ('maybe' if p['intent']=='可能买' else 'no')]+=1
for g in gstat: gstat[g]['median']=st.median(gstat[g]['prices'])
rep={}
for g in GORDER:
    cand=[p for p in P if p['bucket']==g]
    if cand: rep[g]=max(cand,key=lambda x:x['price_ok'])['id']
obj=[list(x) for x in S['obj']]; trg=[list(x) for x in S['trg']]
payload={'personas':P,'obj':obj,'trg':trg,'rev':rev,'gstat':gstat,'gorder':GORDER,'gdesc':GDESC,'grep':rep,
 'median':S['median'],'avg':S['avg'],'intent':S['intent'],'price_band':S['price_band'],'wtp':S['wtp'],'total':S['total']}
json.dump(payload,open('report_data.json','w'),ensure_ascii=False)
print('ok',len(P))
for x in rev: print(x)
