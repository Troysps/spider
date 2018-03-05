README

项目流程：

抓取索引页内容——利用requests请求目标站点，得到索引网页HTML代码，返回结果

代理设置——如果遇到302状态，则证明被封，切换代理重试

分析详情页内容——请求详情页，分析得到目标数据

将数据保存至数据库——将结构化数据保存到MongoDB

技术工具：requests BeautifulSoup os pymongo 
