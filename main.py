import json
import re
from typing import Any

import requests
from colorama import Fore, Back


class Bilibili:
    """
    获取评分的迭代器(每次默认20个，不超过20个)
    """

    class CommentsIter:
        def __init__(self, func, md_id: int, max_cnt: int = 20, next: int = 0):
            self.next = next
            self.func = func
            self.md_id = md_id
            self.max_cnt = max_cnt

        def __iter__(self):
            return self

        def __next__(self):
            self.next, comments = self.func(md_id, max_cnt=self.max_cnt, next=self.next)
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

        _ep_url_match = re.search("(http(s?)://)?www.bilibili.com/bangumi/play/ep(?P<episode_id>\w*)", string,
                                  re.MULTILINE)

        if _ep_url_match:
            if len(_ep_url_match.regs) > 0:
                _start, _end = _ep_url_match.regs[0]
                _ep_url = string[_start:_end]
                _ep_id: int = _ep_url_match.groupdict()['episode_id']
                return _ep_url, _ep_id

    @classmethod
    def grep_season_id(cls, string: str) -> tuple[str, str] | None:
        """
        在字符串中搜索 Season URL
        :param string: 要搜索的字符串
        :return: ss_url 和 ss_id 的 元组
        """

        _ss_url_match = re.search("(http(s?)://)?www.bilibili.com/bangumi/play/ss(?P<season_id>\w*)", string,
                                  re.MULTILINE)

        if _ss_url_match:
            if len(_ss_url_match.regs) > 0:
                _start, _end = _ss_url_match.regs[0]
                _ss_url = string[_start:_end]
                _ss_id: int = _ss_url_match.groupdict()['season_id']
                return _ss_url, _ss_id

    @classmethod
    def grep_media_id(cls, string: str) -> tuple[str, str] | None:
        """
        在字符串中搜索 Media URL
        :param string: 要搜索的字符串
        :return: md_url 和 md_id 的 元组
        """

        _md_url_match = re.search("(http(s?)://)?www.bilibili.com/bangumi/media/md(?P<media_id>\w*)", string,
                                  re.MULTILINE)

        if _md_url_match:
            if len(_md_url_match.regs) > 0:
                _start, _end = _md_url_match.regs[0]
                _md_url = string[_start:_end]
                _md_id: int = _md_url_match.groupdict()['media_id']
                return _md_url, _md_id

    @classmethod
    def query_season_status(cls, ss_id: int) -> dict | None:
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
    def query_media_meta(cls, md_id: int) -> dict | None:
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
    def query_short_comments_count(cls, md_id: int) -> int | None:
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
    def query_short_comments(cls, md_id: int, max_cnt: int = 20, next: int = 0)\
            -> tuple[int, list[dict[str, Any]]] | None:
        """
        获取短评
        :param max_cnt: 单次最大数: 20
        :param next:
        :param md_id: Media Id
        :return: 获取到的长评
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/short/list", params={
            "media_id": md_id,
            "ps": max_cnt,
            "cursor": next
        })
        data = json.loads(_resp.text)
        if data['code'] == 0:
            return data['data']['next'], data['data']['list']
        else:
            return None

    @classmethod
    def query_long_comments_count(cls, md_id: int) -> int | None:
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
    def query_long_comments(cls, md_id: int, max_cnt: int = 20, next: int = 0) -> tuple[
                                                                                      int, list[dict[str, Any]]] | None:
        """
        获取短评
        :param max_cnt: 单次最大数: 20
        :param next:
        :param md_id: Media Id
        :return: 获取到的长评
        """
        _resp = requests.get("https://api.bilibili.com/pgc/review/long/list", params={
            "media_id": md_id,
            "ps": max_cnt,
            "cursor": next
        })

        data = json.loads(_resp.text)

        if data['code'] == 0:
            return data['data']['next'], data['data']['list']
        else:
            return None

    @classmethod
    def query_episode_status(cls, ep_id: int) -> dict | None:
        """
        获取单集数据
        :param ep_id: Episode Id
        :return: 单集数据
        """
        _resp = requests.get("https://api.bilibili.com/pgc/season/episode/web/info", params={
            "ep_id": ep_id
        })
        _resp.raise_for_status()

        data = json.loads(_resp.text)

        if data['code'] == 0:
            return data['data']['stat']
        else:
            return None

    @classmethod
    def query_collective_info(cls, ss_id: int) -> dict | None:
        """
        获取番剧集合信息
        :param ss_id: Season Id
        :return: 集合信息
        """
        _resp = requests.get("https://api.bilibili.com/pgc/view/web/season", params={
            "season_id": ss_id
        })
        _resp.raise_for_status()

        data = json.loads(_resp.text)

        if data['code'] == 0:
            return data['result']
        else:
            return None


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/109.0.0.0 "
                  "Safari/537.36 Edg/109.0.1518.55"
}

if __name__ == '__main__':

    def _at_exit():
        print(Fore.RESET, Back.RESET, end='')


    import sys


    def exc_hook(exc_type, exc_value, tb):
        import traceback
        print(f"{Fore.LIGHTRED_EX}\nSomething went wrong: \n {Fore.LIGHTYELLOW_EX}<== <-- <-- · --> --> ==> {Fore.RED}")
        import time
        time.sleep(0.001)
        traceback.print_exception(exc_type, exc_value, tb)


    sys.excepthook = exc_hook

    load = False
    use_arg = (len(sys.argv) <= 1)
    URL: str = ''
    detailed_epinfo = False


    class ArgProc:
        def __init__(self):
            self.next_load = None

        def __getitem__(self, item: str):
            global load, URL, detailed_epinfo
            if item.startswith(('-', '/')):
                item = item[1:]
                match item:
                    case 'help':
                        self.next_load = 'help'
                        return True
                    case 'url':
                        self.next_load = 'load-url'
                        return True
                    case 'detail':
                        detailed_epinfo = True
                        return True
                    case 'load':
                        load = True
                        return True
                return False
            else:
                match self.next_load:
                    case 'load-url':
                        URL = item
                        print(f"{Fore.CYAN} Selected Url: {Fore.LIGHTCYAN_EX}{URL}")
                        self.next_load = None
                        return True
                self.next_load = None
                return False


    import os
    import pathlib
    import atexit

    atexit.register(_at_exit)

    print(f"{Fore.CYAN}Bangumi Score Counter - B站番剧真实评分计算")
    print(f"{Fore.CYAN}作者 Cyan_Changes UID475405591")

    parg = ArgProc()

    if use_arg:
        for arg in sys.argv[1:]:
            if not parg[arg]:
                print(f"{Fore.RED} Unknown argument {arg}")

    if parg.next_load is not None:
        if parg.next_load == 'help':
            print(f"{Fore.LIGHTMAGENTA_EX} Bangumi Score Counter 用法")
            print(f"{Fore.LIGHTYELLOW_EX} -url \t Bilibili Bangumi Page URL")
            print(f"{Fore.LIGHTYELLOW_EX} -load \t Use Stored Comments")
            print(f"{Fore.LIGHTYELLOW_EX} -help \t Show this help page")
            sys.exit(0)
        else:
            print(f"{Fore.RED} There is not enough argument to process {parg.next_load}")
            sys.exit(-1)

    if (os.path.exists(pathlib.Path("long_comments.json")) and os.path.exists(pathlib.Path("short_comments.json"))) \
            if not use_arg else load:
        if not use_arg:
            print(f"{Fore.YELLOW} 发现评分数据存档, 是否直接加载?")
            ans = input("[Y/n] ").lower()
            match ans:
                case "n":
                    load = False
                case default:
                    load = True

    long_comments = []

    shrt_comments = []

    if not load:

        if not URL or not use_arg:
            print(f"{Fore.MAGENTA} 请输入番剧主页 Url")
            print(f"{Fore.LIGHTCYAN_EX}", end='')
            URL = input(f"{Fore.LIGHTCYAN_EX}[URL] ")

        print(f"{Fore.LIGHTMAGENTA_EX} 获取番剧信息...")

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

        md_id, ss_id, ep_id = map((lambda x: 0 if not x else int(x)), (md_id, ss_id, ep_id))

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
                    ss_url = f"https://www.bilibili.com/bangumi/play/ss{ss_id}"
                    md_url = f"https://www.bilibili.com/bangumi/media/md{md_id}"
                else:
                    print(f"{Fore.RED} Media 解析失败, 请检查链接是否有误!")
                    sys.exit(-1)
            else:
                print(f"{Fore.RED} Media 解析失败, 请检查链接是否有误!")
                sys.exit(-1)

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
            else:
                print(f"{Fore.RED} Season 解析失败!")
            ss_url = f"https://www.bilibili.com/bangumi/play/ss{ss_id}"

        # Match id from page [弃用]
        """
        _resp = requests.get(URL, headers=headers)
        _resp.raise_for_status()
        _, md_id = Bilibili.grep_media_id(_resp.text)
        _, ss_id = Bilibili.grep_season_id(_resp.text)
        _, ep_id = Bilibili.grep_episode_id(_resp.text)
        """

        bangumi_meta = Bilibili.query_media_meta(md_id)
        season_stat = Bilibili.query_season_status(ss_id)
        collective_info = Bilibili.query_collective_info(ss_id)

        print(f"{Fore.CYAN} Episode Url: {ep_url}")
        print(f"{Fore.CYAN} Episode Id:  {ep_id}")
        print(f"{Fore.CYAN} Season Url:  {ss_url}")
        print(f"{Fore.CYAN} Season Id:   {ss_id}")
        print(f"{Fore.CYAN} Media Url:   {md_url}")
        print(f"{Fore.CYAN} Media Id:    {md_id}")

        print(f"{Fore.CYAN} 番剧名称: {bangumi_meta['title']}")
        print(f"{Fore.CYAN} 番剧类型: {bangumi_meta['type_name']}")
        print(f"{Fore.CYAN} 番剧集数: {bangumi_meta['new_ep']['index_show']} {collective_info['new_ep']['desc']}")
        print(f"{Fore.CYAN} 显示分数: {bangumi_meta['rating']['score']} ({bangumi_meta['rating']['count']})")
        print(
            f"{Fore.CYAN} 播放 {season_stat['views']} \t 投币 {season_stat['coins']} \t 弹幕 {season_stat['danmakus']} \n"
            f" 追番 {season_stat['follow']} \t 系列追番 {season_stat['series_follow']}")

        print(f"{Fore.LIGHTMAGENTA_EX} 正在获取剧集信息...")

        print(f"{Fore.MAGENTA} Episode Info")

        for episode in collective_info['episodes']:
            if episode['id'] == ep_id or detailed_epinfo:
                print(f"{Fore.LIGHTCYAN_EX}[{Fore.LIGHTBLUE_EX}长标题{Fore.LIGHTCYAN_EX}] "
                      f"{Fore.CYAN}{episode['long_title'] if episode['long_title'] else f'{Fore.LIGHTBLACK_EX}(无)'}"
                      f"{Fore.LIGHTBLACK_EX}({Fore.LIGHTBLUE_EX}ep{episode['id']}{Fore.LIGHTBLACK_EX}) \t\t"
                      f"{Fore.LIGHTBLACK_EX}ts:{episode['pub_time']}\n"
                      f"{Fore.LIGHTCYAN_EX}AId    \t{Fore.CYAN}{episode['aid']}\t "
                      f"{Fore.LIGHTCYAN_EX}BVId   \t{Fore.CYAN}{episode['bvid']}\n"
                      f"{Fore.LIGHTCYAN_EX}编号.   \t{Fore.CYAN}{episode['title']}\t "
                      f"{Fore.LIGHTCYAN_EX}时长    \t{Fore.CYAN}{episode['duration']}")
                episode_stat = Bilibili.query_episode_status(episode['id'])
                print(f"{Fore.LIGHTCYAN_EX}播放 {Fore.CYAN}{episode_stat['view']} \t "
                      f"{Fore.LIGHTCYAN_EX}点赞 {Fore.CYAN}{episode_stat['like']} \t "
                      f"{Fore.LIGHTCYAN_EX}投币 {Fore.CYAN}{episode_stat['coin']} \n"
                      f"{Fore.LIGHTCYAN_EX}弹幕 {Fore.CYAN}{episode_stat['dm']} \t "
                      f"{Fore.LIGHTCYAN_EX}回复 {Fore.CYAN}{episode_stat['reply']}")

        shrt_cmt_cnt = Bilibili.query_short_comments_count(md_id)

        from tqdm import tqdm

        with tqdm(total=Bilibili.query_short_comments_count(md_id), desc=f"{Fore.RED}获取短评") as pbar:
            for comments in iter(Bilibili.CommentsIter(Bilibili.query_short_comments, md_id, 100)):
                shrt_comments.extend(comments)
                pbar.update(len(comments))

        with tqdm(total=Bilibili.query_long_comments_count(md_id), desc=f"{Fore.RED}获取长评") as pbar:
            for comments in iter(Bilibili.CommentsIter(Bilibili.query_long_comments, md_id, 100)):
                long_comments.extend(comments)
                pbar.update(len(comments))

        print(f"{Fore.MAGENTA} 获取完毕! \n保存中...")

        with open('short_comments.json', 'w', encoding='utf-8') as fp:
            json.dump(shrt_comments, fp)

        with open('long_comments.json', 'w', encoding='utf-8') as fp:
            json.dump(long_comments, fp)

    else:
        print(f"{Fore.MAGENTA} 加载中...")
        with open("short_comments.json", 'r', encoding='utf-8') as fp:
            shrt_comments = json.load(fp)

        with open("long_comments.json", 'r', encoding='utf-8') as fp:
            long_comments = json.load(fp)

        print(f"{Fore.MAGENTA} 加载完毕, 共 {len(shrt_comments) + len(long_comments)} 条!")

    from tqdm import tqdm

    shrt_total = 0

    for comments in tqdm(shrt_comments, desc=f"{Fore.LIGHTRED_EX}短评分数计算"):
        shrt_total += comments['score']

    shrt_score = shrt_total / len(shrt_comments)

    print(f"{Fore.CYAN}短评平均分: \t{Fore.LIGHTCYAN_EX}{shrt_score}")

    long_total = 0

    for comments in tqdm(long_comments, desc=f"{Fore.LIGHTRED_EX}长评分数计算"):
        long_total += comments['score']

    long_score = long_total / len(long_comments)

    print(f"{Fore.CYAN}长评平均分: \t{Fore.LIGHTCYAN_EX}{long_score}")

    score = (shrt_score + long_score) / 2

    print(f"{Fore.CYAN}总平均分: \t{Fore.LIGHTCYAN_EX}{score}")

    print(f"{Fore.GREEN}All Done!")
