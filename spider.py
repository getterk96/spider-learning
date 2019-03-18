import requests
import random
import json
import time
import threading
import queue

class Worker(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            category = self.queue.get()
            ratings = random.sample(
                ['100:90', '90:80', '80:70', '70:60', '60:50', '50:40', '40:30', '30:20', '20:10', '10:0'], 10)
            with open('{}-{}-Urls.txt'.format(category[list(category)[0]], list(category)[0]), 'w') as f:
                a = {}
                for rating in ratings:
                    begin = time.time()
                    a[rating] = []
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
                        'Referer': 'https://movie.douban.com/typerank?type_name={}&type={}&interval_id={}&action='.format(
                            category[list(category)[0]], list(category)[0], rating).encode('utf-8'),
                        'Cookie': 'your-cookie-here'}
                    start = 0
                    while (1):
                        try:
                            r = requests.get(
                                'https://movie.douban.com/j/chart/top_list?type={}&interval_id={}&action=&start={}&limit=20'.format(
                                    list(category)[0], rating, start), headers=headers)
                        except:
                            time.sleep(5)
                            continue
                        j = json.loads(r.text)
                        for item in j:
                            a[rating].append({'name': item['title'], 'url': item['url'], 'rating': item['rating'],
                                              'regions': item['regions'], 'release_date': item['release_date'],
                                              'vote_count': item['vote_count'], 'actors': item['actors']})
                        if len(j) < 20:
                            break
                        start = start + 20
                        time.sleep(random.randint(2, 10) / 1000)

                    print('{}-{}: done! duration: {}s'.format(category[list(category)[0]], rating, time.time() - begin))

                json.dump(a, f)
                f.close()
            time.sleep(1)


category_queue = queue.Queue()
for item in [{'11': '剧情'}, {'24': '喜剧'}, {'5': '动作'}, {'13': '爱情'}, {'17': '科幻'}, {'25': '动画'}, {'10': '悬疑'},
             {'19': '惊悚'}, {'20': '恐怖'}, {'1': '纪录片'}, {'23': '短片'}, {'6': '情色'}, {'26': '同性'}, {'14': '音乐'},
             {'7': '歌舞'}, {'28': '家庭'}, {'8': '儿童'}, {'2': '传记'}, {'4': '历史'}, {'22': '战争'}, {'3': '犯罪'},
             {'27': '西部'}, {'16': '奇幻'}, {'15': '冒险'}, {'12': '灾难'}, {'29': '武侠'}, {'30': '古装'}, {'18': '运动'},
             {'31': '黑色电影'}]:
    category_queue.put(item)

my_workers = []
for i in range(8):
    my_workers.append(Worker(category_queue, i + 1))

for worker in my_workers:
    worker.start()

for worker in my_workers:
    worker.join()

print("All Done.")
