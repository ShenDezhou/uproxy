#!/usr/bin/env python
# coding=utf-8
import time
# import tools
import sys
import os
# import config
import json
import urllib
import urllib2

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.gen import coroutine, Return, Task
import tornado.web
from tornado.web import asynchronous
import tornado.httpclient

# from elasticsearch import Elasticsearch
import log_class
# import redis
import string

define("host", default="http://www.weibo.com", help="the host of the default route /")
define("port", default=8000, help="run on the given port", type=int)
#tornado.httpclient.AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

# redis_queue_host = "b.redis.sogou:2233;b.redis.sogou:2234;b.redis.sogou:2235;b.redis.sogou:2236"
# r = redis.StrictRedis(host='b.redis.sogou', port=2233, db=0, password='livenews2017')
# r_b = redis.StrictRedis(host='b.redis.sogou', port=2234, db=0, password='livenews2017')
#r_json = redis.StrictRedis(host='b.redis.sogou', port=2235, db=0, password='livenews2017')

 # es = Elasticsearch([{'host': 'es-master-ha.service.consul', 'port': 10086}])
# es_b = Elasticsearch([{'host': 'es_master_haproxy.service.consul', 'port': 90}])

param_list = ["url"]

# def create_es_request(request_params):
#     query, num, range = request_params[0], request_params[1], request_params[2]
#     tpl =  json.loads(config.use_tpl)
#     tpl["query"]["bool"]["should"][0]["bool"]["must"][1]["multi_match"]["query"] = query
#     tpl["query"]["bool"]["should"][1]["bool"]["must"][1]["multi_match"]["query"] = query
#     if num != "" and int(num) > tpl["size"]:
#         tpl["size"] = int(num)
#     if range != "":
#         pass
#     return tpl

# client = tornado.curl_httpclient.CurlAsyncHTTPClient(max_clients=11)
base_url = "http://es-master-ha.service.consul:10086/newscenter/news/_search"
baseurl_ip = "http://es_master_haproxy.service.consul:90/newscenter/news/_search"
# key:query, value:url

# def get_es(es,tpl):
    # return es.search(index="newscenter", doc_type="news", body=tpl, preference="_primary_first")

# def full2half(s):
#     n = []
#     s = s.decode('utf-8')
#     pun_list = [0x2985,0x2986] 
#     for char in s:
#         num = ord(char)
#         if num == 0x3000:
#             num = 32
#         elif 0xFF01 <= num and num <= 0xFF5E:
#             num -= 0xfee0
#         elif (0xFF5F <= num and num  <=0xFF65) or (num >= 0x3001 and num <= 0x3020) or num in pun_list:
#             continue
            
#         num = unichr(num)
#         n.append(num)
#     return ''.join(n)    

# def format_sentence(sentence):
#     sentence = full2half(sentence.encode("utf8")).encode("utf8")
#     delset = string.punctuation
#     identify = string.maketrans('', '')
#     sentence = sentence.translate(identify,delset)
#     return sentence

@coroutine
def a_get_es(url):
    client = tornado.httpclient.AsyncHTTPClient()
    request = tornado.httpclient.HTTPRequest(
        url= url,
        method="GET",
        headers = {'User-Agent': 'Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)'}
        # body= json.dumps(tpl).encode('utf8')
        )
        #print >> sys.stderr, "url:%s?%s=%s" % (base_url, 'preference', '_primary_first')
    resp = yield client.fetch(request)
    # body = json.loads(resp.body)
    raise Return(resp.body)

# def get_es_data(base_url,json_tpl):
#     jdata = json.dumps(json_tpl)
#     print jdata
#     req = urllib2.Request(base_url, jdata) 
#     response = urllib2.urlopen(req)
#     return response.read()  




# def time_format(time_str):
#     time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
#     time_stamp = int(time.mktime(time_array))
#     now_stamp = int(time.time())
#     diff = now_stamp - time_stamp
#     if diff < 60:
#         return "刚刚"
#     elif diff >= 60 and diff < 60*60:
#         return str(diff/60) + "分钟前"
#     elif diff >= 60*60 and diff < 24*60*60:
#         return str(diff/(60*60)) + "小时前"
#     elif diff >= 24*60*60 and diff < 60*60*48:
#         return "1天前"
#     elif diff >= 60*60*48 and diff < 60*60*72:
#         return "2天前"
#     else:
#         return time.strftime("%Y-%m-%d", time.localtime(time_stamp)) 

# def time_sort(x, y):
#     time1 = x["_source"]["time"]
#     time2 = y["_source"]["time"]
#     time_array1 = time.strptime(time1, "%Y-%m-%d %H:%M:%S")
#     time_stamp1 = int(time.mktime(time_array1))
#     time_array2 = time.strptime(time2, "%Y-%m-%d %H:%M:%S")
#     time_stamp2 = int(time.mktime(time_array2))
#     if time_stamp1 >= time_stamp2:
#         return -1
#     else:
#         return 1

# def score_sort(x, y):
#     if x["score"] > y["score"]:
#         return -1
#     else:
#         return 1

# def normalization(max_score, min_score, score):
#     if max_score < min_score:
#         return 0
#     return (score - min_score + 1) * 1.0 / (max_score - min_score + 1)

# def get_time_score(new_time, now_time, max_time, min_time):
#     new_time = (now_time - new_time)* 1.0/ 3600;
#     max_time = (now_time - max_time) * 1.0/3600
#     min_time = (now_time - min_time) * 1.0 /3600
#     new_time = min_time - new_time + 1
#     return normalization(min_time - max_time + 1, 1, new_time)

# def score_rank(results, max_score, min_score):
#     max_time = 0
#     min_time = 0
#     for result in results:
#         timeArray = time.strptime(result["_source"]["time"], "%Y-%m-%d %H:%M:%S")
#         timeStamp = int(time.mktime(timeArray))
#         if max_time < timeStamp:
#             max_time = timeStamp
#         if min_time == 0:
#             min_time = timeStamp
#         min_time = min(min_time, timeStamp)

#     min_score = max( min_score - 2000 if min_score - 2000 > 0 else min_score - 1000, 0)
#     min_time = min_time - 5 * 24 * 3600
#     #min_time = 1483200000
#     now = int(time.time())
#     for result in results:
#         timeArray = time.strptime(result["_source"]["time"], "%Y-%m-%d %H:%M:%S")
#         timeStamp = int(time.mktime(timeArray))
#         time_score = get_time_score(timeStamp, now, max_time, min_time)
#         score = normalization(max_score + 100, min_score, result["_score"])
#         result["score"] = 3 * score + 5 * time_score
#         result["score_str"] = str(score) + ":" + str(time_score)

#     results = sorted(results, cmp = score_sort)

#     return results
    
# def filter_result(results, item):
#     for result in results:
#         if tools.get_lcs_similar(result["_source"]["title"].replace("<em>","").replace("<em/>",""), item["_source"]["title"].replace("<em>","").replace("<em/>","")) > 0.7:
#             return 0
#     results.append(item)
#     return 1

# def pic_rank1(select_result, num):
#     index = 0
#     tmp_result = []
#     result = []
#     for item in select_result:
#         if index == 0:
#             if ((item["_source"]["pic_url"] == "" or (not item["_source"]["pic_url"].startswith("https") and not item["_source"]["pic_url"].startswith("http")))\
#                and (item["_source"]["small_pic"] == "" or (not item["_source"]["small_pic"].startswith("https") and not item["_source"]["small_pic"].startswith("http"))))\
#                or ((not item["highlight"].has_key("content") or item["highlight"]["content"][0] == "")):
#                 tmp_result.append(item)
#             else:
#                 index += 1
#                 filter_result(result, item)
#         elif index == 1:
#             for tmp in tmp_result:
#                 index += filter_result(result, tmp)
#             index += filter_result(result, item)
#         else:
#             index += filter_result(result, item)
#         if index == num:
#             return result
#     return result

# def pic_rank(select_result, num):
#     index = 0
#     result = []
#     for item in select_result:
#         index += filter_result(result, item)
#         if index == num:
#             break
#     if len(result) < 2:
#         return result
#     first_item = result[0] 
#     if (first_item["_source"]["pic_url"] == "" or (not first_item["_source"]["pic_url"].startswith("https") and not first_item["_source"]["pic_url"].startswith("http")))\
#         and (first_item["_source"]["small_pic"] == "" or (not first_item["_source"]["small_pic"].startswith("https") and not first_item["_source"]["small_pic"].startswith("http"))):
#         pc_url = ""
#         small_url = ""
#         for item in result:
#             if pc_url == "" and item["_source"]["pic_url"] != "":
#                 pc_url = item["_source"]["pic_url"]
#             if small_url == "" and item["_source"]["small_pic"] != "":
#                 small_url = item["_source"]["small_pic"]
#         # print >> sys.stderr, "set first pic_url %s" % pc_url
#         if first_item["_source"]["pic_url"] == "":
#             first_item["_source"]["pic_url"] = pc_url
#         if first_item["_source"]["small_pic"] == "":
#             first_item["_source"]["small_pic"] = small_url
#     return result

# def pic_qc(es_result):
#     no_result = 0
#     for item in es_result:
#         if item["_source"]["small_pic"] == "" and item["_source"]["pic_url"] == "" :
#             pass
#         else:
#             no_result = 1
#             break
#     if no_result == 0:
#         return []
#     return es_result

# def filter_rank_result(es_data, num):
#     # if not es_data.has_key("hits"):
#     #     return es_data
#     es_result = es_data["hits"]["hits"]
#     es_result = make_default(es_result)
    
#     if len(es_result) <= 1:
#         return es_result
#     time1 = time.time()
#     es_result = sorted(es_result, cmp = time_sort)
#     # print >> sys.stderr, "time1 %s" % str(time.time() - time1)
#     select_result = es_result
#     max_score = es_data["hits"]["max_score"]
#     min_score = max_score
#     time2 = time.time()
#     #for item in es_result:
#     #    is_similar = False
#     #    for sitem in select_result:
#     #        if tools.get_lcs_similar(item["_source"]["title"], sitem["_source"]["title"]) > 0.7:
#     #            is_similar = True
#     #            break
#     #    if not is_similar:
#     #        select_result.append(item)
#     #        min_score = min(item["_score"], min_score)
#     #
#     #print >> sys.stderr, "time2 %s" % str(time.time() - time2)
#     select_result = pic_qc(select_result)
#     if min_score > 1000:
#         results = pic_rank(select_result, num)
#         # print >> sys.stderr, "time4 %s" % str(time.time() - time2)
#         return results
#     time3 = time.time()
#     results = score_rank(select_result, max_score, min_score)
#     # print >> sys.stderr, "time3 %s" % str(time.time() - time3)
#     time4 = time.time()
#     results = pic_rank(results, num)
#     # print >> sys.stderr, "time4 %s" % str(time.time() - time4)
#     return results

# def lower_no_summary(es_data):
#     #print >> sys.stderr, es_data
#     if len(es_data) > 1:
#         if not es_data[0]["highlight"].has_key("summary") and not es_data[0]["highlight"].has_key("content"):
#             dest = 0
#             for x in xrange(1,len(es_data)):
#                 if es_data[x]["highlight"].has_key("summary") and es_data[x]["highlight"]["summary"] != "" :
#                     dest = x
#                     break
#                 elif es_data[x]["highlight"].has_key("content") and  es_data[x]["highlight"]["content"] != "" :
#                     dest = x
#                     break
#             if dest:
#                 # print >> sys.stderr, 'lower_no_summary swapped item 0 with item %d' % dest
#                 es_data[0], es_data[dest] = es_data[dest], es_data[0]
#     #print >> sys.stderr, es_data
#     return es_data

# def make_xml_result(es_result, params_map):
#     result_str = ""
#     es_len = len(es_result)
#     if es_len <= 1:
#         return "<!--STATUS NOVR OK-->"
#     if es_len == 2:
#         if es_result[0]["_source"]["small_pic"] == "" and es_result[1]["_source"]["small_pic"] == "" :
#             return "<!--STATUS NOVR OK-->"
#         elif es_result[0]["_source"]["small_pic"] != "":
#             es_result[1]["_source"]["pic_url"] = ""
#         else:
#             tmp = es_result[1]
#             es_result[1] = es_result[0]
#             es_result[0] = tmp


#     class_id = params_map["classid"]
#     if class_id == "11013401" and es_result[0]["_source"]["small_pic"]  == "":
#         return "<!--STATUS NOVR OK-->"
        

#     if class_id == "11012101" and es_result[0]["_source"]["pic_url"] == "":
#         return "<!--STATUS NOVR OK-->"
    
#     items_str = ""
#     for item in es_result:
#         item_str = ""
#         item_str += "<subitem><title><![CDATA[" + item["highlight"]["title"][0] + "]]></title>\n"
#         item_str += "<url><![CDATA[" + item["_source"]["url"] + "]]></url>\n"
#         item_str += "<subdisplay><site_name><![CDATA[" + item["_source"]["site_name"]+ "]]></site_name>\n"

#         if item["highlight"].has_key("summary") and item["highlight"]["summary"][0] != "":
#             item_str += "<summary><![CDATA[" + item["highlight"]["summary"][0] + "]]></summary>\n"
#         elif item["highlight"].has_key("content"):
#             item_str += "<summary><![CDATA[" + item["highlight"]["content"][0] + "]]></summary>\n"
#         item_str += "<author><![CDATA[" + item["_source"]["author"] + "]]></author>\n"
#         item_str += "<channel><![CDATA[" + item["_source"]["channel"] + "]]></channel>\n"
#         item_str += "<time><![CDATA[" + time_format(item["_source"]["time"]).decode("utf-8")+ "]]></time>\n"
#         #item_str += "<time><![CDATA[" + (item["_source"]["time"])+ "]]></time>\n"
#         item_str += "<showtime><![CDATA[" + item["_source"]["time"] + "]]></showtime>\n"
#         item_str += "<pic_url><![CDATA[" + item["_source"]["pic_url"]+ "]]></pic_url>\n"
#         item_str += "<small_pic><![CDATA[" + item["_source"]["small_pic"] + "]]></small_pic>\n"
#         item_str += "<ampurl><![CDATA[" + item["_source"]["ampurl"] + "]]></ampurl>\n"
#         item_str += "<ampcode><![CDATA[" + item["_source"]["ampcode"] + "]]></ampcode>\n"
#         item_str += "<tags><![CDATA[" + item["_source"]["tags"] + "]]></tags>\n"
#         item_str += "</subdisplay>\n</subitem>"
#         items_str += item_str
       
#     result_str += "term(0);<?xml version=\"1.0\" encoding=\"utf-16\"?>\n"
#     result_str += "<DOCUMENT><item><key ><![CDATA[" + params_map["queryString"] + "_SogouNews]]></key>\n"
#     result_str += "<display><title><![CDATA[" + params_map["queryString"] + "]]></title>\n"
#     result_str += "<url><![CDATA[http://www.sogou.com]]></url>\n"
#     result_str += items_str
#     result_str += "<count>" + str(es_len) +"</count>\n"
#     result_str += "<classid>" + class_id + "</classid>\n"
#     result_str += "<classtag>" + params_map["classtag"] +"</classtag>\n"
#     result_str += "<tplid>" + params_map["tplid"] + "</tplid>\n"
#     result_str += "<param1>50000</param1>\n<param2>100</param2> \n<param3>50000</param3>\n <param4>103</param4> \n<param5>1</param5>\n"
#     result_str += "</display>\n</item>\n</DOCUMENT>\n<!--STATUS VR OK-->"
    
#     return result_str


class MainHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self, url):
        input_time = time.time()
        request_params = []
        params_map = {}
        for param in param_list:
            value = self.get_argument(param, '')
            request_params.append(value)
            params_map[param] = value

        base_url = options.host + url
        print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, request_query: %s" % (os.getpid(), str(input_time), base_url)
        try:
            es_data =  yield a_get_es(base_url)
            self.set_header("Content-Type", "charset=UTF-8")
            send_time = time.time()

            self.write(es_data)
        except Exception as e:
            print >> sys.stderr, "Sogou-Observer: requestid:%08d, exception: %s" % (os.getpid(), str(e[:200]))

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        request_params = []
        params_map = {}
        for param in param_list:
            value = self.get_argument(param, '')
            request_params.append(value)
            params_map[param] = value

        tpl = create_es_request(request_params)
        tpl["size"] = int(params_map["num"]) if params_map["num"] != '' else 10
        es_data =  get_es(es, tpl)
        es_result = filter_rank_result(es_data, int(params_map["num"]))
        self.write({"es" : es_result})
        #result = pic_rank(es_result, params_map["num"])
        #res_data =  make_xml_result(result, params_map)
        #self.write(res_data)#.encode("gbk"))

# char_list = [u'\u0387', u'\u2022', u'\xa0', u'\u200b']
# def filter_char(data):
#     for char in char_list:
#         data = data.replace(char, "")
#     return data.encode("gbk")

# fields = ["author","channel","pic_url","small_pic","tags","ampurl","ampcode"]
# def make_default(data):
#     for item in data:
#         for field in fields:
#             if not item["_source"].has_key(field):
#                 item["_source"][field] = ""
#                 continue
#             if not item["_source"][field]:
#                 item["_source"][field] = ""
#     return data

class IndexHandler(tornado.web.RequestHandler):
    @coroutine
    def get(self):
        input_time = time.time()
        request_params = []
        params_map = {}
        for param in param_list:
            value = self.get_argument(param, '')
            request_params.append(value)
            params_map[param] = value
        print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, request_query: %s" % (os.getpid(), str(input_time), self.get_argument("url", '').encode('utf8'))
        # url = format_sentence(params_map["url"])
        base_url = urllib.unquote(params_map["url"])
        try:
            # class_id = params_map["classid"]
            # if class_id == "11013401":
            #     redis_cache = r.get(key)
            # else:
            #     redis_cache = r_b.get(key)
            # if redis_cache:
            #     self.set_header("Content-Type", "charset=UTF-16")
            #     # print >> sys.stderr, "rank time1 %s" % str(send_time - make_time)
            #     self.write(redis_cache)
            #     #r.expire(key,30)
            #     #redis_cache = redis_cache.decode("utf-16")
            #     if redis_cache != "<!--STATUS NOVR OK-->".encode("utf-16"):
            #         print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, query: %s, cost: %d, RESOK ret: 0, CACHE" % (os.getpid(), str(input_time), params_map["queryString"].encode('utf8'), int(( time.time()-input_time)*1000))
            #     else:
            #         print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, query: %s, cost: %d, NORES ret: 0, CACHE" % (os.getpid(), str(input_time), params_map["queryString"].encode('utf8'), int(( time.time()-input_time)*1000))
            #     return
            # tpl = create_es_request(request_params)
            # preference=_primary_first
            # es_data =  get_es(es, tpl)
            es_data =  yield a_get_es(base_url)
            # es_data = es.search(index="newscenter", doc_type="news", body=tpl, request_cache="true", terminate_after=5)
            # rank_time = time.time()
            # print >> sys.stderr, "get_es time %s" % str(rank_time - input_time)
            # es_result = filter_rank_result(es_data, int(params_map["num"]))
            # print >> sys.stderr, "rank time %s" % str(time.time() - rank_time)
            # es_result = lower_no_summary(es_result)
            # make_time = time.time()
            # res_data =  make_xml_result(es_result, params_map)
            self.set_header("Content-Type", "charset=UTF-8")
            send_time = time.time()
            # print >> sys.stderr, "rank time1 %s" % str(send_time - make_time)

            self.write(es_data)
            # if len(es_result):
            #     print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, query: %s, cost: %d, RESOK ret: %d, get_es time %s, rank time %s, rank time1 %s" % (os.getpid(), str(input_time), params_map["queryString"].encode('utf8'), int((send_time-input_time)*1000), len(es_result), str(rank_time - input_time), str(time.time() - rank_time),str(send_time - make_time))
            # else:
            #     print >> sys.stderr, "Sogou-Observer: requestid:%08d-%s, query: %s, cost: %d, NORES ret: 0, get_es time %s, rank time %s, rank time1 %s" % (os.getpid(), str(input_time), params_map["queryString"].encode('utf8'), int((send_time-input_time)*1000), str(rank_time - input_time), str(time.time() - rank_time),str(send_time - make_time))
        except Exception as e:
            print >> sys.stderr, "Sogou-Observer: requestid:%08d, exception: %s" % (os.getpid(), str(e[:200]))

            

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/route", IndexHandler),
                                            (r"/test", TestHandler),
                                            (r"/(.*)", MainHandler)], debug=False)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(0)
    tornado.ioloop.IOLoop.instance().start()

