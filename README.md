# WHUTdormElectricityInquiry
脚本查询WHUT学生公寓剩余电量。

可以用来做LED监控屏

## Prerequisites
* `requests`
* `pytesseract`

## Usage
可以参见main.py里的说明。
建立userdata.py，按格式填写学号、缴费平台密码和寝室信息即可。

## 获取寝室信息
[浏览器F12看这里](https://github.com/AsterisMono/WHUTdormElectricityInquiry/blob/master/dormdata.png)

## 训练模型
参见`num.traineddata`。

下载并放置到Tesseract-OCR/tessdata文件夹。
