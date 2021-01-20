# README

## 环境依赖

- 操作系统：centos 8.2
- Python 3.8
    - flask
    - pymongo

版本详情见requirements.txt

### 环境安装

```shell
conda create -n myFlask python=3.8
conda activate myFlask
pip install -r requirements.txt
```

## 运行

```shell
sh run.sh
```

run.sh中将flask在后台运行，注意更改app.py中的全局参数
- app.config['rootPath']：上传文件以及生成文件的存储路径
- host、username、password：数据库ip，账号，密码
- 在controllers的pdf.py的runModel函数中，其中需要运行脚本，此路径注意修改

## API说明

### 测试路由

#### URL

- /pdf/test

#### Method

- GET/POST

#### 解释

- 用于测试



### 上传并运行模型路由

#### URL

- /pdf/upload

#### Method

- POST

#### 解释

- 上传pdf并运行模型进行表格识别，返回pdf的表格识别信息，并存入数据库

### 下载识别表格路由

#### URL

/downloadXLSX/<path:filename>/<pageNum>

#### Method

- GET

#### Parameters

- filename：文档名称
- pageNum：指定页码的指定表格 如 17a

#### 解释

- 获取pdf某一页所识别的表格xlsx


### 下载结果路由

#### URL

/downloadResult/<path:filename>

#### Method

- GET

#### Parameters

- filename：文档名称


#### 解释

- 获取文档识别的所有表格压缩包


### 预览结果路由

#### URL

/getTable/<pdfName>/<pageNum>

#### Method

- GET

#### Parameters

- filename：文档名称
- pageNum：指定页码的指定表格 如 17a

#### 解释

- 在线预览表格识别结果，返回html形式表格
