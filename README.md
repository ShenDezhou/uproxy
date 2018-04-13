#UProxy

##A micro proxy pretending to be Sogo web spider to get Weibo posts.

#Usage

##Installation

###1.Get a linux or windows server, install Python 2.7.

###2.Install facebook asynchronous lightweight web server tornado.
> pip install tornado

##Start Proxy

host: the website you want to crawl.
port: in which port the proxy listens.
> python proxy.py --port=8000 --host=https://weibo.com/ &

##Make Request

###1./route

###2.url=<some url you want to crawl>
> http://10.134.100.140:8000/route?url=http://weibo.com/rshuai&is_hot=1

##Output

The output looks like this:
> [uproxy][00018538] INFO 2018-04-13 11:49:30,505 [Starting 4 processes]
> [uproxy][00010906] ERROR 2018-04-13 11:50:27,568 [Sogou-Observer: requestid:00010914-1523591427.57, request_query: http://weibo.com/rshuai]
> [uproxy][00010906] INFO 2018-04-13 11:50:29,188 [200 GET /route?url=http://weibo.com/rshuai&is_hot=1 (10.129.152.68) 1622.82ms]
> [uproxy][00010906] ERROR 2018-04-13 11:50:30,895 [Sogou-Observer: requestid:00010914-1523591430.9, request_query: https://weibo.com/favicon.ico]
> [uproxy][00010906] INFO 2018-04-13 11:50:30,926 [200 GET /favicon.ico (10.129.152.68) 31.52ms]
> [uproxy][00010906] ERROR 2018-04-13 11:50:31,101 [Sogou-Observer: requestid:00010914-1523591431.1, request_query: https://weibo.com/p/aj/recommendlist]
> [uproxy][00010906] INFO 2018-04-13 11:50:31,137 [200 GET /p/aj/recommendlist?ajwvr=6&mid=route&location=page_100306_home&oid=1405862165&__rnd=1523591431404 (10.129.152.68) 36.86ms]
> [uproxy][00010906] ERROR 2018-04-13 11:50:33,908 [Sogou-Observer: requestid:00010914-1523591433.91, request_query: https://weibo.com/aj/guide/bubblead]
> [uproxy][00010906] INFO 2018-04-13 11:50:33,966 [200 GET /aj/guide/bubblead?ajwvr=6&pageid=&_t=0&__rnd=1523591434210 (10.129.152.68) 57.73ms]
