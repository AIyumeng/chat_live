# chat_live
哔哩哔哩直播弹幕互动chatbot


## Introduction

本项目完成一个最简单的的哔哩哔哩直播弹幕互动机器人

## Start

### step 1 拉取项目


```shell
git clone https://github.com/AIyumeng/chat_live.git
cd chat_live
```

### step 2 环境配置

```shell
conda create --name myenv python=3.9
conda activate myenv
pip install -r requirements.txt
```

### step 3 修改config

设置api

    1. 将config.json文件中的api_keys更换为你的api

    2. 其中api_proxy用于填入第三方中转OpenAI API的地址,如果没有则在on属性填入false即可。

    3. proxy则为代理地址（http代理）,如果不需要则在on属性填入false即可。

设置直播开放平台信息

    1. 在bilibili创作者服务中心实名认证通过后,获得ACCESS_KEY_ID,ACCESS_KEY_SECRET
    2. 创建应用,获得APP_ID
    3. 在主播直播间获得ROOM_OWNER_AUTH_CODE

### step 4 RUN
```python
python bilibili.py
```

## 写在最后
项目参考：
> [https://github.com/xfgryujk/blivedm](https://github.com/xfgryujk/blivedm)

> [https://github.com/SwaggyMacro/BarrageGPT](https://github.com/SwaggyMacro/BarrageGPT)

