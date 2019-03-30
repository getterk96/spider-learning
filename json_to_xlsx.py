import json
import xlsxwriter
import pandas as pd
import time
import threading
import queue

file_name = "D:/result-1.txt"

result = open(file_name, 'r')
j = json.load(result)
result.close()


class Worker(threading.Thread):
    def __init__(self, queue, num):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num

    def run(self):
        while self.queue.qsize() > 0:
            item = self.queue.get()
            print("Thread-{} working on {}".format(self.num, item['name']))
            sheetToWrite = pd.DataFrame(columns=['电影', '评论人', '评论时间', '是否看过', '评分', '赞同数', '内容'],
                                        index=[i for i in
                                               range(len(item['short_reviews']['P'] + item['short_reviews']['F']))])

            indexs = ['user', 'comment-time', 'status', 'rating', 'votes', 'content']
            all_reviews = []
            for status in ['P', 'F']:
                for review in item['short_reviews'][status]:
                    all_reviews.append(review)
            for i in range(len(all_reviews)):
                if all_reviews[i] == {}:
                    continue
                for j in range(len(indexs)):
                    sheetToWrite.iloc[i, 0] = item['name']
                    sheetToWrite.iloc[i, j + 1] = all_reviews[i][indexs[j]]

            threadLock.acquire()
            xlsx_data_frames.append({'data': sheetToWrite, 'name': item['name']})
            threadLock.release()


xlsx_data_frames = []
movie_queue = queue.Queue()
for item in j:
    new_reviews = {'P': [], 'F': []}
    for status in ['P', 'F']:
        for review in item['short_reviews'][status]:
            if review != {}:
                new_reviews[status].append(review)
    item['short_reviews'] = new_reviews
    movie_queue.put(item)

threadLock = threading.Lock()
my_workers = []
for i in range(8):
    my_workers.append(Worker(movie_queue, i + 1))

for worker in my_workers:
    worker.start()

for worker in my_workers:
    worker.join()

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
for item in xlsx_data_frames:
    item['data'].to_excel(writer, item['name'])
writer.save()
writer.close()
print("All Done.")
