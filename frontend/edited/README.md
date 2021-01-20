# PDF_tool
 PDF tool

## 技术架构
1. 前端架构：Express
2. pdf嵌入：PDFObject
3. 将本地文件夹提供http访问：
（windows环境下，unix略有区别）
    ```shell
    npm install -g serve
    (然后在目标文件夹下进入cmd)
    serve -p 8080
    ```
    随后可以在http://localhost:8080/访问到该文件夹

## 前端的启动：
（windows环境下，unix略有区别）
```
npm install
set NODE_ENV=production
node app.js
```