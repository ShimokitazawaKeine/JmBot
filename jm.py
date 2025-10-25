import jmcomic

# 创建配置对象
# option = jmcomic.create_option_by_file('option.yml')

class jm:

    def __init__(self, config_file='option.yml'):
        """
        初始化下载器实例，并加载配置。
        """
        print(f"正在加载配置: {config_file}")
        # 1. 将配置加载到实例属性 self.option 中
        self.option = jmcomic.create_option_by_file(config_file)
        print("配置加载完成。")

    def get_album(self, jm_code):
        #格式check
        if not isinstance(jm_code, str) or not jm_code.isdigit():
            raise ValueError("鹿管暗号必须是数字字符串喵")

        print(f"开始下载图集: {jm_code}")

        jmcomic.download_album(jm_code, self.option)
        return f" {jm_code}下载完成喵"


    def extract_jm_code(self, message_content):
        # 1. 以空格为分隔符，将消息内容分割成列表
        # 示例: "/jm 12345".split() 结果是 ['/jm', '12345']
        parts = message_content.split()

        # 2. 检查列表长度。命令至少需要两部分：命令本身和参数
        if len(parts) < 2:
            return None, "缺少鹿管暗号喵"

        # 3. 提取第二部分作为 jm_code
        jm_code = parts[1]

        # 4. 验证 jm_code 是否是数字
        if not jm_code.isdigit():
            return None, "鹿管暗号不对喵"

        return jm_code, None