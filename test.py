import jinja2 as jinja
import datetime
import asyncio
import time
# t = jinja.Template('{% for t in test1 %}{% if loop.index == 2 %}aaa{% else %}bbb{% endif %}{% endfor %}')
# output = t.render(test1 = [5,5,5,5])
# print(output)

# print(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

import threading

# 子執行緒的工作函數
def job():
  for i in range(5):
    print(i)
    time.sleep(5)

# 建立一個子執行緒
t = threading.Thread(target = job)

# 執行該子執行緒
t.start()

# 主執行緒繼續執行自己的工作
for i in range(10):
  print("Main thread:")
  time.sleep(1)

# 等待 t 這個子執行緒結束
# t.join()

print("Done.")
