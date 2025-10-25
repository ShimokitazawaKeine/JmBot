## QQ bot with JmComic Crawler

> 基于qq官方的Python SDK [QQbot: Botpy](https://github.com/tencent-connect/botpy) 与禁漫爬取API [Python API for JMComic](https://github.com/hect0x7/JMComic-Crawler-Python) 简单缝合制作。感谢开源

#### 使用方法：

1. 配置qq平台的机器人相关事务。可参照对应官方文档。

2. 注册Ngrok账号，用于反向代理。

3. `./data/`文件下，使用命令 `python -m http.server 80`，运行本地http文件服务器。

4. 启动`./data/ngrok.exe`，按照ngrok官网引导要求配置密钥，启动反向代理服务。
   
   > 这时你应当可以通过访问 `http://你的ngrok地址/Hiroi.png` 查看到实例图像。

5. 将对应ngrok地址填入到 `app.py` 开始位置的 `user_url` 变量中。

6. 另外，你还需要根据 [Python API for JMComic](https://github.com/hect0x7/JMComic-Crawler-Python) 对 `option.yml` 的要求进行配置。重点是配置 `base_dir` ，如：
   
   ```yml
   dir_rule:
     base_dir: # 这里写"./data/"的绝对位置
     rule: Bd / Aid
   ```

7. 大功告成，现在运行 `app.py` 。

#### 指令：

- `/jmcover`: 获取封面。

- `/jmvid`: 获取具体内容。由于qq平台不开发pdf等文件格式，这里使用 `cv2` 将图片拼接为视频。

---

注释代码中还有一些llm api对话相关的功能，考虑反应时间过长而放弃了。
