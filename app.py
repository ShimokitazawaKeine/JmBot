from jm import jm
from pdfProcess import pdfProcess
from img2vid import ImageToVideoConverter

# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

user_url = "" # 须配置ngrok url
BASE_PATH = 'data/'

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        print(message.content)
        print(message.id)

        if "/jmcover" in message.content:

            jm_code, error = jm.extract_jm_code(message.content)
            if error:
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=error)
                _log.info(messageResult)

            else:
                rep = jm.get_album(jm_code)

                await asyncio.sleep(3)

                file_url = user_url + jm_code + "/00001.jpg"  # 这里需要填写上传的资源Url
                print(file_url)

                uploadMedia = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=1,  # 文件类型要对应上，具体支持的类型见方法说明
                    url=file_url  # 文件Url
                )

                # 资源上传后，会得到Media，用于发送消息
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,  # 7表示富媒体类型
                    msg_id=message.id,
                    media=uploadMedia
                )

        elif "/jmvid" in message.content:

            jm_code, error = jm.extract_jm_code(message.content)
            if error:
                messageResult = await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=0,
                    msg_id=message.id,
                    content=error)
                _log.info(messageResult)

            else:
                rep = jm.get_album(jm_code)

                # img to pdf
                pdf.jm_code_update(jm_code)
                print(pdf.imgpdf_pipe())

                # img to mp4
                converter.set_job_context(job_code=jm_code)
                output_video_path = converter.run_conversion_pipeline()

                await asyncio.sleep(3)



                file_url = user_url + jm_code + ".mp4"  # 这里需要填写上传的资源Url
                print(file_url)

                uploadMedia = await message._api.post_group_file(
                    group_openid=message.group_openid,
                    file_type=2,  # 文件类型要对应上，具体支持的类型见方法说明
                    url=file_url  # 文件Url
                )

                # 资源上传后，会得到Media，用于发送消息
                await message._api.post_group_message(
                    group_openid=message.group_openid,
                    msg_type=7,  # 7表示富媒体类型
                    msg_id=message.id,
                    media=uploadMedia
                )

        else:
            # print("调用openai中")
            # prompt = build_prompt(message.content)
            # answer = generate_answer(prompt)
            # print("调用成功")
            # reply = answer.output[1].content[0].text
            # print(reply)

            # file_url = "https://martial-overtightly-foster.ngrok-free.dev/1225249.mp4"
            #
            # uploadMedia = await message._api.post_group_file(
            #     group_openid=message.group_openid,
            #     file_type=2,  # 文件类型要对应上，具体支持的类型见方法说明
            #     url=file_url  # 文件Url
            # )
            #
            # # 资源上传后，会得到Media，用于发送消息
            # await message._api.post_group_message(
            #     group_openid=message.group_openid,
            #     msg_type=7,  # 7表示富媒体类型
            #     msg_id=message.id,
            #     media=uploadMedia
            # )

            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                  msg_type=0,
                  msg_id=message.id,
                  content="请严肃鹿管..."
            )
            _log.info(messageResult)


if __name__ == "__main__":

    jm = jm(config_file = 'option.yml')

    pdf = pdfProcess(path = BASE_PATH)
    # 1. 实例化转换器
    # 传入 BASE_PATH 作为图片的根目录
    converter = ImageToVideoConverter(base_path=BASE_PATH)

    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])














# 初始化 FastAPI 实例
# app = FastAPI(title="JiBang")

# 允许跨域请求（如前端使用 React/Streamlit 等调用）
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# 加载向量索引（假设已经 build 好）

# store = VectorStore.load("data/index.faiss", "data/passages.json", dim=EMBED_DIM, metric="cosine")

# @app.post("/ask")
# def ask_question(question: str = Form(...)):
#     # 向量化问题
#     query_vec = embed([question])[0]
#     query_vec = np.array(query_vec).astype("float32")
#
#     # 检索最相关的段落（Top-3）
#     top_passages = store.search(query_vec, top_k=3)
#
#     # 构造 prompt
#     prompt = build_prompt(contexts=top_passages, question=question)
#
#     # print(prompt)
#     print(prompt)
#
#     # 调用本地 Qwen 模型生成回答
#     answer = generate_answer(prompt)
#     # answer = generate_answer(question)  # 测试prompt, 更方便调试。
#
#     print(answer)
#
#     # answer = answer["choices"][0]["text"].strip() # 此为本地部署的输出处理
#     answer = answer.output[1].content[0].text
#
#     # 返回结果
#     return {
#         "question": question,
#         "prompt": prompt,
#         "answer": answer
#         # "retrieved": top_passages
#     }
