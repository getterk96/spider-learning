# coding=utf-8
import requests
import random
import json
import time
import queue
import os
from datetime import datetime
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

index_file_dir = "./"  # path-to-your-index
proxies = [{"https": "http://127.0.0.1:1081"}, {"https": "http://127.0.0.1:1082"}, {"https": "http://127.0.0.1:1083"},
           {"https": "http://127.0.0.1:1084"}, {"https": "http://127.0.0.1:1085"}, {"https": "http://127.0.0.1:1086"},
           {"https": "http://127.0.0.1:1087"}, {"https": "http://127.0.0.1:1088"}, {"https": "http://127.0.0.1:1089"},
           {"https": "http://127.0.0.1:1090"}]  # to-do
email_address = "getterk@163.com"
email_access_code = "smtp1234"


def send_alert_email(sender, pwd, receivers, msg):
    message = MIMEText(msg, "plain", "utf-8")
    message["From"] = Header("DoubanSpider", "utf-8")
    message["To"] = Header("Me", "utf-8")

    subject = "Your Spider Program Has Been Blocked, Restart It Now!"
    message["Subject"] = Header(subject, "utf-8")

    try:
        smtp_obj = smtplib.SMTP("smtp.163.com", 25)
        smtp_obj.login(sender, pwd)
        smtp_obj.sendmail(sender, receivers, message.as_string())
        print("Alert email sent!")
    except smtplib.SMTPException:
        print("Failed to send alert email, please check your network status!")


def dump_into_result_file(dump_data, index_point):
    with open("result-{}.txt".format(index_point // 50 + 1), "w") as result_file:
        json.dump(dump_data, result_file)
        result_file.close()
    if len(dump_data) >= 50:
        dump_data = []
    old_i_file = open(index_file_dir + "all_index.txt", "r")
    new_i_all = json.load(old_i_file)
    old_i_file.close()
    with open(index_file_dir + "all_index.txt", "w") as new_i_file:
        new_i_all["current_in"] = index_point
        json.dump(new_i_all, new_i_file)
        new_i_file.close()
    print("Current Data Point-{} Index Point-{} Data Saved!".format(len(dump_data), index_point))
    return dump_data


def load_index():
    main_index = []
    if os.path.isfile(index_file_dir + "all_index.txt"):
        with open(index_file_dir + "all_index.txt", "r") as i_all:
            all_index = json.load(i_all)
            index_point = all_index["current_in"]
            main_index = all_index["data"]
            i_all.close()
    else:
        with open(index_file_dir + "all_index.txt", "w") as i_all:
            names = set()
            for index_file in os.listdir(index_file_dir):
                if index_file == "all_index.txt":
                    continue
                with open(index_file_dir + index_file, "r") as f:
                    print(index_file)
                    j = json.load(f)
                    for rating in list(j):
                        for movie in j[rating]:
                            if movie["name"] not in names:
                                names.add(movie["name"])
                                new_item = movie
                                new_item["category"] = index_file.split("-")[0]
                                new_item["type"] = index_file.split("-")[1]
                                new_item["rating"] = rating
                                main_index.append(new_item)
                    f.close()
            json.dump({"current_in": 0, "data": main_index}, i_all)
            index_point = 0
            i_all.close()

    return main_index, index_point


def restore_data(main_index, index_point):
    if os.path.isfile("result-{}.txt".format(index_point // 50 + 1)):
        result = open("result-{}.txt".format(index_point // 50 + 1), "r")
        cur_data = json.load(result)
        result.close()
    else:
        cur_data = []

    index_queue = queue.Queue()
    for i in range(len(main_index)):
        if i >= index_point - 1:
            index_queue.put(main_index[i])
    if not cur_data:
        restored_data = {"short_reviews": {"P": [], "F": []}}
    elif cur_data[-1]["name"] != main_index[index_point - 1]["name"]:
        index_queue.get()
        restored_data = {"short_reviews": {"P": [], "F": []}}
    else:
        restored_data = cur_data[-1]
        cur_data = cur_data[:-1]
        index_point = index_point - 1

    print("已完成{}个电影".format(len(cur_data)))
    print("本次共计{}个电影".format(index_queue.qsize()))
    return index_queue, cur_data, restored_data, index_point


def request_for_html(url, cur_data, index_point):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/73.0.3683.75 Safari/537.36",
        "Referer": "https://accounts.douban.com/passport/login",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Cookie": "bid=0T7CuQvkg4Y; ll=\"108288\"; __yadk_uid=covotNZx9vMZFgQc6brLzRdQVbp4L9cF; "
                  "_vwo_uuid_v2=DF5DD1D49EC24D1447F98645B9179E22A|0a9f95518f9bf2f3e3334e4921da1ce0; push_noty_num=0; "
                  "push_doumail_num=0; __utmv=30149280.15862; __utmc=30149280; __utmc=223695111; ps=y; ct=y; "
                  "__utma=223695111.1140888479.1552825016.1553759441.1553959598.18; "
                  "__utmz=223695111.1553959598.18.9.utmcsr=baidu|utmccn=("
                  "organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; "
                  "__utma=30149280.1017682141.1552825016.1553959598.1553959598.20; "
                  "__utmz=30149280.1553959598.20.6.utmcsr=baidu|utmccn=("
                  "organic)|utmcmd=organic|utmctr=%E8%B1%86%E7%93%A3; "
                  "_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1554011655%2C%22https%3A%2F%2Fwww.baidu.com%2Fs%3Fie"
                  "%3Dutf-8%26f%3D8%26rsv_bp%3D1%26rsv_idx%3D1%26tn%3Dbaidu%26wd%3D%25E8%25B1%2586%25E7%2593%25A3"
                  "%26rsv_pq%3D9c16380f0004f1b7%26rsv_t%3D4d64XyGSTAB76hhLAAL4Nkgg84bznIYcKMeENuNDottsxXbbRruon9eGo2o"
                  "%26rqlang%3Dcn%26rsv_enter%3D1%26rsv_sug3%3D7%26rsv_sug1%3D7%26rsv_sug7%3D100%26rsv_sug2%3D0"
                  "%26inputT%3D1424%26rsv_sug4%3D1424%26rsv_sug%3D2%22%5D; _pk_ses.100001.4cf6=*; ap_v=0,"
                  "6.0; dbcl2=\"158620360:/CST1jorn40\"; ck=W5z3; "
                  "_pk_id.100001.4cf6=1154722f256b0bf6.1552792494.25.1554012024.1553959720.; "
                  "RT=s=1554012032941&r=https%3A%2F%2Fmovie.douban.com%2Fsubject%2F27179414%2Fcomments%3Fstart%3D1000"
                  "%26limit%3D20%26sort%3Dnew_score%26status%3DP"}
    while 1:
        try:
            r = requests.get(url, headers=headers, proxies=random.choice(proxies))
            break
        except:
            dump_into_result_file(cur_data, index_point)
            print("Url: {} blocked! Resting...".format(url))
            time.sleep(random.randint(2, 4))

    return BeautifulSoup(r.text, features="html.parser")


def run(index_queue, cur_data, restored_data, index_point):
    movies_before_rest = 1
    interval_to_rest = 10
    block_times_before_abort = 3
    rest_in = movies_before_rest
    while index_queue.qsize() > 0:
        if rest_in > 0:
            rest_in = rest_in - 1
        else:
            rest_in = movies_before_rest
            cur_data = dump_into_result_file(cur_data, index_point)
            print("resting...for {}s".format(interval_to_rest))
            time.sleep(interval_to_rest)
            continue

        begin = time.time()
        short_block_risk = 0
        movie_index = index_queue.get()
        new_item = movie_index
        soup = request_for_html(movie_index["url"], cur_data, index_point)

        try:
            if not restored_data["rating_levels"]:
                rating_levels_raw = soup.find_all(class_="rating_per")
                rating_levels = [float(item.string[0:-1]) / 100 for item in rating_levels_raw]
            else:
                rating_levels = restored_data["rating_levels"]
        except:
            rating_levels = [-1, -1, -1, -1, -1]

        try:
            if not restored_data["problem_num"]:
                problem_num = soup.find_all(class_="mod-hd")[1].find(class_="pl").a.string[2:-1]
            else:
                problem_num = restored_data["problem_num"]
        except:
            problem_num = -1

        try:
            if not restored_data["long_review_num"]:
                long_review_num = soup.find_all(class_="reviews mod")[0].find(class_="pl").a.string[3:-2]
            else:
                long_review_num = restored_data["long_review_num"]
        except:
            long_review_num = -1

        try:
            if not restored_data["discussion_num"]:
                discussion_num = soup.find_all(class_="section-discussion")[0].find_all(class_="pl")[-1].a.string[
                                 39:-23]
            else:
                discussion_num = restored_data["discussion_num"]
        except:
            discussion_num = -1

        short_blocked = False
        short_reviews = restored_data["short_reviews"]

        for status in ["P", "F"]:
            while 1:
                if short_block_risk >= block_times_before_abort:
                    short_blocked = True
                    break

                shorts_soup = request_for_html(
                    movie_index["url"] + "comments?start={}&limit=20&sort=time&status={}".format(
                        len(short_reviews[status]), status), cur_data, index_point)
                try:
                    comments = shorts_soup.find_all(class_="comment")
                except:
                    short_block_risk = short_block_risk + 1
                    continue

                for comment in comments:
                    try:
                        date = comment.find("span", class_="comment-time").attrs["title"]
                        comment_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        if comment_date > datetime.strptime(movie_index['final_date'], '%Y-%m-%d %H:%M:%S'):
                            raise Exception("Not Proper Date!")
                        short_reviews[status].append({"votes": comment.find("span", class_="votes").string,
                                                      "user": comment.find("span", class_="comment-info").a.string,
                                                      "status": status,
                                                      "rating":
                                                          comment.find("span", class_="rating").attrs["class"][0][
                                                              -2] if status == "P" else -1,
                                                      "comment-time": date,
                                                      "content": comment.find("span", class_="short").string})
                    except:
                        short_reviews[status].append({})
                    print(short_reviews[status][-1])
                if len(comments) < 20:
                    break
                time.sleep(random.randint(1, 3))

        new_item["rating_levels"] = rating_levels
        new_item["problem_num"] = problem_num
        new_item["short_reviews"] = short_reviews
        new_item["long_review_num"] = long_review_num
        new_item["discussion_num"] = discussion_num
        cur_data.append(new_item)
        index_point = index_point + 1

        if short_blocked:
            print("blocked at {} {}-{}!".format(len(cur_data), movie_index["category"], movie_index["name"]))
            dump_into_result_file(cur_data, index_point)
            send_alert_email(email_address, email_access_code, [email_address], "")
            break

        print("{}-{}: done! 共计{}条短评 duration: {}s".format(movie_index["category"], new_item["name"],
                                                          len(cur_data[-1]["short_reviews"]["P"]) +
                                                          len(cur_data[-1]["short_reviews"]["F"]), time.time() - begin))
        restored_data = {"short_reviews": {"P": [], "F": []}}

    if index_queue.qsize() == 0:
        print("All done.")
    else:
        print("Please check the cookies and restart the spider!")


if __name__ == "__main__":
    index = load_index()
    data = restore_data(index[0], index[1])
    run(data[0], data[1], data[2], data[3])
