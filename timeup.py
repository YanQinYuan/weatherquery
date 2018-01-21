# -*- coding: utf-8 -*-
# 如果在5分钟以内查询相同的数据, 不用通过 API 访问远程数据源（较难，选做）
# 任务分解：
# 定时任务
# 插入定时任务
from datetime import datetime
import time
# 输出时间
now = datetime.now()
time.sleep(300)
now2 = datetime.now()

print(now2 - now)
