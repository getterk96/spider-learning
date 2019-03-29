import json
import random
from detail_spider import load_index

movie_names = {
    "高跟鞋先生", "奔爱", "谋杀似水年华", "美人鱼", "西游记之孙悟空三打白骨精", "澳门风云3", "年兽大作战", "过年好", "功夫熊猫3", "蒸发太平洋", "致我们终将到来的爱情", "恶人报喜",
    "真相禁区", "一家老小向前冲", "熊出没之熊心归来", "最后的巫师猎人", "消失爱人", "国酒", "恋爱教父之三个“坏”家伙", "荒村怨灵", "舌尖上的新年", "小门神", "一切都好", "放飞理想",
    "赤狼蚁",
    "碟中谍5：神秘国度", "湖杀令", "落跑吧爱情", "夏洛特烦恼", "九层妖塔", "解救吾先生", "魔镜奇缘", "少年杨靖宇", "超萌特攻队-长江7号", "港囧", "第三种爱情", "遥远的拥抱", "诡打墙",
    "这里是新疆", "男左女右", "黄河", "华丽上班族", "情敌蜜月", "角逐", "人皮拼图", "墓穴迷城", "燃烧的影像", "将离草", "别有动机", "铁血残阳", "来电不善", "像素大战",
    "星语心愿之再·爱", "1980年代的爱情", "斗地主", "东莞女孩", "启功", "大变局之梦回甲午", "黑猫警长之翡翠之星", "新步步惊心", "我爸比我小四岁", "爱之初体验", "轩辕剑传奇", "情剑",
    "时间都去哪了", "小西天狄道传奇", "破风", "桂宝之爆笑闯宇宙", "一路向前", "红髅", "百团大战", "诡劫", "犹太女孩在上海2：项链密码", "烈日灼心", "刺客聂隐娘", "三城记", "心跳戈壁",
    "诱狼", "战火中的芭蕾", "双生灵", "王子与108煞", "新娘大作战", "水墨大别山", "非你勿扰", "恋爱中的城市", "鹰笛·雪莲", "我是大熊猫2之熊猫大侠", "七月半之恐怖宿舍",
    "白雪公主之神秘爸爸", "狂野飞车", "相伴库里申科", "滚蛋吧！肿瘤君", "洛克王国4：出发！巨人谷", "宅女侦探桂香", "最美的承诺", "汽车人总动员", "巴黎假期", "美人鱼之海盗来袭", "恐怖游泳馆",
    "男人制造", "谜城",
    "王朝的女人·杨贵妃", "太平轮·彼岸", "穿越硝烟的歌声", "西游新传2：真心话大冒险", "传奇状元伦文叙", "一诺千金", "等爱归来", "命中注定", "通灵之六世古宅", "守梦者",
    "赛尔号大电影5：雷神崛起", "奥拉星：进击圣殿", "道士下山", "我是路人甲", "张震讲故事之鬼迷心窍", "煎饼侠", "爱情魔发师", "捉妖记", "少女哪吒", "西游记之大圣归来", "栀子花开",
    "猪猪侠之终极决战",
    "亲，别怕之鬼宅凶灵", "为了这片土地", "不可思异", "从天儿降", "杜拉拉追婚记", "柴生芳", "唐人街探案", "一念天堂", "索命暹罗之按摩师", "探秘者", "怦然星动", "胜利大阅兵", "老炮儿",
    "恶棍天使",
    "分手再说我爱你", "寻龙诀", "万万没想到", "诡娃娃", "根据地", "没女神探", "圣诞大赢家", "咕噜咕噜美人鱼", "擦枪走火", "最美的时候遇见你", "东北偏北", "紫霞", "电商时代", "师父",
    "不能错过", "前任2：备胎反击战", "剩者为王", "雨夜惊魂", "时尚女郎之女人江湖", "火云端", "我的处女地", "消失的凶手", "坏蛋必须死", "诡影迷情", "摇滚水果", "水晶女孩", "一刻十年",
    "玩命速递：重启之战", "十月初五的月光", "一个勺子", "藏羚王", "灵臆事件", "遭遇海明威", "痞子·洛克", "桑榆街9号", "陪安东尼度过漫长岁月", "年少轻狂", "男二本色", "我的青春期",
    "我的诗篇", "天各一方", "我是证人", "山河故人", "兔子镇的火狐狸", "魔比斯环", "囧贼", "回到被爱的每一天", "既然青春留不住", "龙在哪里？", "浪漫天降", "猛龙特囧", "探灵档案",
    "家在水草丰茂的地方", "莫日根", "喜马拉雅天梯", "心迷宫", "笔仙魔咒", "魔卡行动", "零点杀机", "巴啦啦小魔仙之魔箭公主", "山海经：天眼传奇", "极地大反攻", "妈妈 让我再爱你一次",
    "家有虎妻", "幸福很囧",
    "荒村凶间", "长江图", "奇葩追梦", "为爱放手", "夜魔人", "丢羊", "看见我和你", "湄公河行动", "爵迹2", "王牌逗王牌", "幽灵医院", "新木偶奇遇记", "爱的钟声",
    "从你的全世界路过", "悍匪围城", "诡梦凶铃", "凤凰谷", "谁的青春不热血之深流不息", "三个孬家伙", "我们的十年", "夜半哭声", "小魔仙之黑魔法来袭", "玩命剧组",
    "安静的乡村女人", "击战", "我的战争", "麦兜·饭宝奇兵", "神兽金刚之青龙再现", "一条叫王子的狗", "爱的蟹逅", "大话西游3", "反贪风暴2", "七月与安生", "追凶者也",
    "丝路英雄·云镝", "咱们分手吧", "斗艳", "换个活法", "谎言西西里", "盗墓笔记", "夏有乔木 雅望天堂", "我最好朋友的婚礼", "古曼", "狼兵吼", "在世界中心呼唤爱",
    "诡新娘", "花样厨神", "白雪公主和三只小猪", "爱在星空下", "幸运是我", "喊·山", "爸爸的木房子", "疯狂的疯狂", "勿忘初心", "低碳爱情", "天使请吻我", "守灵",
    "龙拳小子", "新大头儿子和小头爸爸2一日成才", "精灵王座", "七月半2：前世今生", "终极硬汉", "Hi,高考君", "吉祥宝宝之我是食神", "一棵心中的许愿树", "怦·心跳", "筑梦人",
    "夜郎侠之一路危途", "微微一笑很倾城", "危城", "我们诞生在中国", "那件疯狂的小事叫爱情", "岛囧", "使徒行者", "再生之乐", "返乡", "人在驴途", "寒战2", "大鱼海棠",
    "致青春·原来你还在这里", "摇滚藏獒", "发条城市", "张震讲故事之合租屋", "冰雪女王2：冬日魔咒", "戊子风雪同仁堂", "封神传奇", "神秘世界历险记3", "宝贝当家", "情况不妙",
    "六弄咖啡馆", "催命符之劫后重生", "毒中毒", "天亮之前", "老阿姨", "刺猬小子之天生我刺", "魔都凶音", "少年师爷之大禹宝藏", "恐怖爱情故事之死亡公路", "绝地逃亡",
    "泡沫之夏", "丑小鸭历险记", "陆垚知马俐", "惊天大逆转", "快手枪手快枪手", "超能太阳鸭", "路边野餐", "超级保镖", "笔仙撞碟仙", "假装看不见之电影大师", "警魂之命悬一线",
    "赏金猎人", "魔轮", "古田会议", "终极胜利", "党的女儿尹灵芝", "28岁未成年", "呆呆计划", "凄灵室", "塔洛", "爱上试睡师", "牡丹仙子之皇帝诏曰", "那美",
    "试睡员48小时", "超级幼儿园", "人鱼校花", "情圣", "那年夏天你去了哪里", "你好，疯子！", "爸爸的3次婚礼", "难忘金银滩", "冒牌卧底", "初恋的滋味", "我的女神女汉子",
    "铁道飞虎", "摆渡人", "失心者", "有迹可循", "三少爷的剑", "超级快递", "食人岛", "沙漠之心", "老腔", "东宫皇子", "锅是铁", "求生者", "甜水谣", "功夫四侠",
    "长城", "罗曼蒂克消亡史", "少年", "我在故宫修文物", "五女闹京城", "生门", "飞天窑女", "我的朋友圈", "流金", "先锋之那时青春", "爱你的人", "生死96小时",
    "捉迷藏", "一句顶一万句", "非常父子档", "恐怖笔记", "笑林足球", "盛先生的花儿", "别让我走", "狱中惊魂", "诡咒", "被劫持的爱情", "我的圣途", "冲天火",
    "最萌身高差", "我是处女座", "夏威夷之恋", "怨灵地下室", "越囧", "热土悲歌", "骆驼客2：箭在弦", "我不是潘金莲", "勇士之门", "白云桥", "少年梦", "活宝",
    "红颜容", "最后证言", "比利·林恩的中场战事", "外公芳龄38", "聊斋新编之画皮新娘", "减法人生", "脱单宝典", "非常绑架", "兄弟之北漂歌手", "贫穷富爸爸", "夺路而逃",
    "那年我对你的承诺", "爱情不等式", "新东方神娃", "疯狂丑小鸭", "驴得水", "小明和他的小伙伴们", "育婴室", "枕边有张脸2", "何去何从", "大会师", "热血雷锋侠之激情营救",
    "异性合租的往事", "杠上开花", "惊天破", "铠甲勇士捕王", "太阳河", "12勇士", "黑处有什么", "爱神箭", "小熊的夏天", "四渡赤水", "T台魔王", "爱上处女座",
    "心语阳光", "遵义会议", "我是哪吒", "心灵解码", "功夫瑜伽", "西游伏妖篇", "乘风破浪", "熊出没之奇幻空间", "嫌疑人X的献身", "拆弹专家", "记忆大师", "喜欢你",
    "逆时营救", "春娇救志明", "非凡任务", "大卫贝肯之倒霉特工熊", "傲娇与偏见", "决战食神", "东北往事之破马张飞", "游戏规则", "冈仁波齐", "绑架者", "血战湘江",
    "反转人生", "欢乐喜剧人", "荡寇风云", "疯岳撬佳人", "合约男女", "猪猪侠之英雄猪少年", "毒。诫", "重返·狼群", "麻烦家族", "“吃吃”的爱", "忠爱无言", "血狼犬",
    "完美有多美", "三只小猪2", "美好的意外", "缉枪", "抢红", "健忘村", "我的爸爸是国王", "神秘家族", "提着心吊着胆", "临时演员", "碟仙诡谭2", "中国推销员",
    "异兽来袭", "美容针", "仙球大战", "夏天19岁的肖像", "以爱为名", "我是医生", "玛格丽特的春天", "二代妖精之今生有幸", "二十二", "芳华", "缝纫机乐队", "父子雄兵",
    "机器之血", "建军大业", "鲛珠传", "京城81号2", "空天猎", "七十七天", "奇门遁甲", "前任3：再见前任", "赛尔号大电影6：圣者无敌", "三生三世十里桃花", "杀破狼-贪狼",
    "十八洞村", "十万个冷笑话", "王牌保镖", "悟空传", "侠盗联盟", "心理罪", "心理罪城市之光", "羞羞的铁拳", "绣春刀之修罗战场", "妖铃铃", "妖猫传", "英伦对决",
    "战狼2", "追龙"}

new_all_index = []
all_index, index_point = load_index()
for item in all_index:
    if item['release_date'] != '' and int(item['release_date'][0:4]) < 2015:
        continue
    if item['name'] in movie_names:
        new_all_index.append(item)

with open("all_index.txt", "w") as index_file:
    random.shuffle(new_all_index)
    json.dump({'current_in': 0, 'data': new_all_index}, index_file)
