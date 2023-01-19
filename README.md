# Bilibili-BangumiScoreCounter
获取 真实的 B站番剧评分

## 使用方法  
### 下载
#### 方法一
    git clone https://github.com/Chinese-Cyq20100313/Bilibili-BangumiScoreCounter.git sc_counter
    cd sc_counter
    ./main.py

#### 方法二
下载 [main.py](main.py) 直接使用

### 使用

#### 无参数直接运行
如果提示已有评分数据(项目自带异化版三体存档)  
![image](https://user-images.githubusercontent.com/68551684/213120402-0caa1565-7236-435d-a66e-a43b9435cff8.png)  
并且你想要直接统计这个数据的评分，请输入Y并回车  
![image](https://user-images.githubusercontent.com/68551684/213120817-0181df13-af33-4aee-821a-4127b15ddd7a.png)  
如果你想要获取最新数据，请输入n并回车  
如果没有提示，可以打开要统计的番剧，复制链接，粘贴，回车，等待获取结果。
![image](https://user-images.githubusercontent.com/68551684/213110498-c72a9aa0-0376-4eb3-8e3e-b55b589b7fba.png)

#### 使用参数
参数加载番剧Url
    ./main.py -url [番剧URL]
参数使用保存的数据
    ./main.py -load
获取帮助 (特性 只有help在最后才可以生效)
    ./main.py -help
番剧全部剧集信息
    ./main.py -detail
Example
    ./main.py -detail -url https://www.bilibili.com/bangumi/play/ep704479?from_spmid=666.25.episode.0&from_outer_spmid=666.19.0.0

#### 作者B站账号: Cyan_Changes UID475405591

## Update Log
23/1/19: 
1. 更新了最新的 异化三体 评分数据(5.22>5.21)
2. 命令行参数优化
3.  - 支持使用参数设置url
4.  - 支持使用参数加载存档
5.  - 可以获取帮助
6.  - 通过 -detail 获取详细信息
7.  - 更新了相关文档
8. 文档
9.  - 添加 Update Log 信息
10. 显示:
11.  - 支持显示 所有番剧 剧集状态
12.  - 如果传入了Episode Id可以显示此集的信息
13.  - 优化颜色和缩进, 增强可读性
14.  - 显示更多信息
15. 其他:
16.  - 修复无法自动生成 Season Url 的问题
17.  - 修复自动生成的 Url 不包含 'https://' 的问题
18.  - 支持解析http(s)和未设置的链接
19. 画饼:
20.  - 支持保存剧集信息
21.  - 支持保存分数历史