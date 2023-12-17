## React_vercelBE_practiceV3
本版有兩大處理目標：
1. 把它變成應用docker做虛擬環境、套件、版本管理
2. 處理id歸零的議題（非必要），相關代碼實踐在db_worlist.py
3. 處理Skill格式化以及篩選的議題，但目前卡住在JSONB，後續要請教老師。主要是本地搭建的postgresql可以運轉，但雲端versel的postgresql無法運轉

## 第一迭代，如果只單純運轉dockerfile的指令與說明：
docker裡的python版本，使用python:3.12.1-slim
然後端口因為本地卡一些其餘不知名議題，無法使用5000，改採8000
要打開本地API，應用指令`docker run -p 8000:8000 react-vercel-be-practice-v3`

## 第二迭代，導入yml以及本地的postgresql伺服器
使用終端指令：`docker compouse up`，就能開心管理跨容器的文件們了

## 第三迭代，製作全域搜尋以及技能篩選的功能
主要是借鏡老師python/2023/wkd書寫的代碼，新增了ID歸零（非必要）、ID搜尋、全域搜尋、以及技能格式化與搜尋。