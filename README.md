# exchange_api

## 程序结构简介

程序主要分为三个线程：
* 线程1 fetchSpotPrice。 主要负责用websocket从各个交易所得到所有的现货价格。假如是3个交易所，那么就会得到3个现货价格。  
* 线程2 calculateIndex。 主要负责使用现货价格，和过去5分钟的数据，计算index。 具体计算方式见`计算方式`部分。  
* 线程3 webServer。 主要负责起一个本地的 http server，来响应 /index_price 的GET request。  

## Running
1. 请确认本地已安装 mysql, python3, websocket.
2. 数据库设置在`configs.py` 文件。只需要改动`PASSWORD`的值，保证程序能以`root@localhost`连接mysql.
3. 直接启动 `main.py`， 然后打开 `http://localhost:8080/index_price` 即可看到结果。
4. `CTRL+C` 退出程序

## Index 计算方式
1. 首先从交易所获得现货价格`spot_price`,其中`spot_price` = 所有交易所现货价格的平均值。
2. 从数据库得到过去五分钟内的所有`index_price`。 同时得到上一个`index_price` 产生时，使用的均值`last_mean`和方差`last_sigma`。
3. 假如`spot_price`在`last_mean ± 3*last_sigma`内, 则对数据集 [过去五分钟的`index_price`, `spot_price`]做正态拟合。`cur_sigma`, `cur_mean`, `spot_price`存入数据库，计算完成。
4. 假如在3sigma以外:  
    4.1. 假如大部分数据在`3*last_sigma`以内: 认为有错误数据。重新计算`spot_price` = `3*last_sigma`以内的数据平均值。 然后重复 `step 3`。   
    4.2. 否则，认为有大范围行情变动， 认可当前`spot_price`的合理性，重复 `step 3`
 
