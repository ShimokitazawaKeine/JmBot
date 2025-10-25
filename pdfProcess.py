import os
import img2pdf


class pdfProcess:
    def __init__(self, path = "data/"):
        print("加载本地地址")
        self.base_dir = path
        self.output_path = path
        self.image_extension = ".jpg"
        self.sorted_images = []
        print("加载完成")

    def jm_code_update(self, jm_code):
        print("加载本子地址")
        self.base_image_dir = self.base_dir + jm_code + "/"
        self.output_path = self.output_path + jm_code +".pdf"
        self.jm_code = jm_code
        print("加载完成")

    def get_img_order(self):
        # 1. 获取所有图片文件的完整路径
        # os.listdir(image_dir) 获取文件名列表
        # os.path.join() 组合目录和文件名得到完整路径
        all_imgs = [os.path.join(self.base_image_dir, f) for f in os.listdir(self.base_image_dir) if f.endswith(self.image_extension)]
        self.sorted_imgs = sorted(all_imgs)

        return None

    def process_img(self):
        try:
            with open(self.output_path, "wb") as f:
                # img2pdf.convert() 接受一个图片文件路径列表
                f.write(img2pdf.convert(self.sorted_imgs))

            print(f"成功将 {len(self.sorted_imgs)} 张图片整合为 PDF: {self.output_path}")
        except Exception as e:
            print(f"转换过程中发生错误: {e}")

    def imgpdf_pipe(self):
        self.get_img_order()
        self.process_img()

        return self.output_path


# def main():
#     pdf = pdfProcess(path = "data/")
#     pdf.jm_code_update(jm_code = '1225249')
#     print(pdf.imgpdf_pipe())
#
#
# if __name__ == "__main__":
#     main()
