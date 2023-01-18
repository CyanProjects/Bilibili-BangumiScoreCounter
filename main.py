import sys
from typing import Any

from colorama import Fore, Back
import requests

import re

import json


class Bilibili:

    class CommentsIter:
        def __init__(self, func, md_id: str, next: int = 0):
            self.next = next
            self.func = func
            self.md_id = md_id

        def __iter__(self):
            return self

        def __next__(self):
            self.next, comments = self.func(md_id, self.next)
            if not comments:
                raise StopIteration
            return comments

    @classmethod
    def grep_episode_id(cls, string: str) -> tuple[str, str] | None:
        """
        在字符串中搜索 Episode URL
        :param string: 要搜索的字符串
        :return: ep_url 和 ep_id 的 元组
        """

        _ep_url_match = re.search("www.bilibili.com/bangumi/play/ep(?P<episode_id>\w*)", string, re.MULTILINE)

        if _ep_url_match:
            if len(_ep_url_match.regs) > 0:
                _start, _end = _ep_url_match.regs[0]
                _ep_url = string[_start:_end]
                _ep_id: str = _ep_url_match.groupdict()['episode_id']
                return _ep_url, _ep_id

    @classmethod
    def grep_season_id(cls, string: str) -> tuple[str, str] | None:
        """
        在字符串中搜索 Season URL
        :param string: 要搜索的字符串
        :return: ss_url 和 ss_id 的 元组
        """

        _ss_url_match = re.search("www.bilibili.com/bangumi/play/ss(?P<season_id>\w*)", string, re.MULTILINE)

        if _ss_url_match:
            if len(_ss_url_match.regs) > 0:
                _start, _end = _ss_url_match.regs[0]
                _ss_url = string[_start:_end]
                _ss_id: str = _ss_url_match.groupdict()['season_id']
                return _ss_url, _ss_id

    @classmethod
    def grep_media_id(cls, string: str) -> tuple[str, str] | None:
        """
        在字符串中搜索 Media URL
        :param string: 要搜索的字符串
        :return: md_url 和 md_id 的 元组
        """

        _md_url_match = re.search("www.bilibili.com/bangumi/media/md(?P<media_id>\w*)", string, re.MULTILINE)

        if _md_url_match:
            if len(_md_url_match.regs) > 0:
                _start, _end = _md_url_match.regs[0]
                _md_url = string[_start:_end]
                _md_id: str = _md_url_match.groupdict()['media_id']
                return _md_url, _md_id

    @classmethod
    def get_season_status(cls, ss_id: str) -> dict | None:
        """
        获取 Season 状态
        :param ss_id: Season Id
        :return: 状态
        """
        _resp = requests.get("https://api.bilibili.com/pgc/web/season/stat", params={
            "season_id": ss_id
        })
        _resp.raise_for_status()

        data = json.loads(_resp.text)

        if data['code'] == 0:
            return data['result']
        else:
            return None


    @classmethod
    def get_media_meta(cls, md_id: str) -> dict | None:
        """
        获取 Media 元数据
        :param md_id: Media Id
        :return: 元数据
        """

        _resp = requests.get("https://api.bilibili.com/pgc/review/user", params={
            "media_id": md_id
        })
        
        _resp.raise_for_status()
        data = json.loads(_resp.text)
        
        if data['code'] == 0:
            return data['result']['media']
        else:
            return None

    @classmethod
    def query_short_comments_count(cls, md_id: str) -> int | None:
        """
        获取短评数
        :param md_id: Media Id
        :return: 短评数
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/short/list", params={
            "media_id": md_id,
            "ps": 0
        })
        data = json.loads(_resp.text)
        if data['code'] == 0:
            return data['data']['total']
        else:
            return None

    @classmethod
    def query_short_comments(cls, md_id: str, next: int = 0) -> tuple[int, list[dict[str, Any]]] | None:
        """
        获取短评
        :param next:
        :param md_id: Media Id
        :return: 获取到的长评
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/short/list", params={
            "media_id": md_id,
            "ps": 20,
            "cursor": next
        })
        data = json.loads(_resp.text)
        if data['code'] == 0:
            return data['data']['next'], data['data']['list']
        else:
            return None

    @classmethod
    def query_long_comments_count(cls, md_id: str) -> int | None:
        """
        获取长评数
        :param md_id: Media Id
        :return: 长评数
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/long/list", params={
            "media_id": md_id,
            "ps": 0
        })
        data = json.loads(_resp.text)
        if data['code'] == 0:
            return data['data']['total']
        else:
            return None

    @classmethod
    def query_long_comments(cls, md_id: str, next: int = 0) -> tuple[int, list[dict[str, Any]]] | None:
        """
        获取短评
        :param next:
        :param md_id: Media Id
        :return: 获取到的长评
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/long/list", params={
            "media_id": md_id,
            "ps": 20,
            "cursor": next
        })

        data = json.loads(_resp.text)

        if data['code'] == 0:
            return data['data']['next'], data['data']['list']
        else:
            return None


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/109.0.0.0 "
                  "Safari/537.36 Edg/109.0.1518.55"
}

print(f"{Fore.MAGENTA} 请输入番剧主页 Url")
print(f"{Fore.LIGHTCYAN_EX}", end='')
URL: str = input(f"{Fore.LIGHTCYAN_EX}[URL] ")

print(f"{Fore.LIGHTMAGENTA_EX} 获取视频信息...")

md_id, ss_id, ep_id = (None,) * 3
md_url, ss_url, ep_url = (None,) * 3

try:
    md_url, md_id = Bilibili.grep_media_id(URL)
    ss_url, ss_id = Bilibili.grep_season_id(URL)
    ep_url, ep_id = Bilibili.grep_episode_id(URL)
except TypeError:
    try:
        ss_url, ss_id = Bilibili.grep_season_id(URL)
        ep_url, ep_id = Bilibili.grep_episode_id(URL)
    except TypeError:
        try:
            ep_url, ep_id = Bilibili.grep_episode_id(URL)
        except TypeError:
            if (md_id or ss_id or ep_id) is None:
                print(f"{Fore.RED} URL 解析失败, 请检查链接是否有误!")
                sys.exit(-1)

md_id, ss_id, ep_id = map((lambda x: 0 if not x else x), (md_id, ss_id, ep_id))

# request other id from api
if not md_id:
    if ep_id or ss_id:
        _resp = requests.get("https://api.bilibili.com/pgc/view/web/season", headers=headers, params={
            "season_id": ss_id,
            "ep_id": ep_id
        })
        _resp.raise_for_status()
        data = json.loads(_resp.text)
        if data['code'] == 0:
            md_id = data['result']['media_id']
            ss_id = data['result']['season_id']
        else:
            print(f"{Fore.RED} Media 解析失败, 请检查链接是否有误!")
            sys.exit(-1)

    md_url = f"https://www.bilibili.com/bangumi/media/md{md_id}"

if not ss_id:
    if md_id:
        _resp = requests.get("https://api.bilibili.com/pgc/review/user", headers=headers, params={
            "media_id": md_id,
        })
        _resp.raise_for_status()
        data = json.loads(_resp.text)
        if data['code'] == 0:
            md_id = data['result']['media']['media_id']
        else:
            print(f"{Fore.RED} Season 解析失败!")
    elif ep_id:
        _resp = requests.get("https://api.bilibili.com/pgc/view/web/season", headers=headers, params={
            "ep_id": ep_id,
        })
        _resp.raise_for_status()
        data = json.loads(_resp.text)
        if data['code'] == 0:
            md_id = data['result']['season_id']
        else:
            print(f"{Fore.RED} Season 解析失败!")

    ss_url = f"https://www.bilibili.com/bangumi/play/ss{ss_id}"

# Match id from page
"""
_resp = requests.get(URL, headers=headers)
_resp.raise_for_status()
_, md_id = Bilibili.grep_media_id(_resp.text)
_, ss_id = Bilibili.grep_season_id(_resp.text)
_, ep_id = Bilibili.grep_episode_id(_resp.text)
"""

bangumi_meta = Bilibili.get_media_meta(md_id)
season_stat = Bilibili.get_season_status(ss_id)

print(f"{Fore.CYAN} 番剧名称: {bangumi_meta['title']}")
print(f"{Fore.CYAN} 番剧类型: {bangumi_meta['type_name']}")
print(f"{Fore.CYAN} 番剧集数: {bangumi_meta['new_ep']['index_show']}")
print(f"{Fore.CYAN} 显示分数: {bangumi_meta['rating']['score']} ({bangumi_meta['rating']['count']})")
print(f"{Fore.CYAN} 投币 {season_stat['coins']} \t 弹幕 {season_stat['danmakus']} \n"
      f" 追番 {season_stat['follow']} \t 系列追番 {season_stat['series_follow']} \n"
      f" 播放 {season_stat['views']}")

print(f"{Fore.CYAN} Episode Url: {ep_url}")
print(f"{Fore.CYAN} Episode Id:  {ep_id}")
print(f"{Fore.CYAN} Season Url:  {ss_url}")
print(f"{Fore.CYAN} Season Id:   {ss_id}")
print(f"{Fore.CYAN} Media Url:   {md_url}")
print(f"{Fore.CYAN} Media Id:    {md_id}")

shrt_cmt_cnt = Bilibili.query_short_comments_count(md_id)

from tqdm import tqdm

shrt_comments = []

with tqdm(total=Bilibili.query_short_comments_count(md_id)) as pbar:
    pbar.set_description("获取短评")
    for comments in iter(Bilibili.CommentsIter(Bilibili.query_short_comments, md_id)):
        shrt_comments.extend(comments)
        pbar.update(len(comments))

long_comments = []

with tqdm(total=Bilibili.query_long_comments_count(md_id)) as pbar:
    pbar.set_description("获取长评")
    for comments in iter(Bilibili.CommentsIter(Bilibili.query_long_comments, md_id)):
        long_comments.extend(comments)
        pbar.update(len(comments))


print(f"{Fore.MAGENTA} 获取完毕! 保存中...")

with open('short_comments.json', 'w', encoding='utf-8') as fp:
    json.dump(shrt_comments, fp)

with open('long_comments.json', 'w', encoding='utf-8') as fp:
    json.dump(long_comments, fp)

shrt_total = 0

for comments in tqdm(shrt_comments, desc=f"{Fore.LIGHTRED_EX}短评分数计算"):
    shrt_total += comments['score']

shrt_score = shrt_total / len(shrt_comments)

print(f"{Fore.CYAN}短评平均分: {shrt_score}")

long_total = 0

for comments in tqdm(long_comments, desc=f"{Fore.LIGHTRED_EX}长评分数计算"):
    long_total += comments['score']

long_score = long_total / len(long_comments)

print(f"{Fore.CYAN}长评平均分: {long_score}")

score = (shrt_score + long_score) / 2

print(f"{Fore.CYAN}总平均分: {score}")


print(f"{Fore.GREEN}All Done!")
