import re
import json
import requests
def music(name):
    url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=62115878671550904&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w={name}&g_tk=5381&jsonpCallback=MusicJsonCallback2806001545440244&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    json_list = requests.get(url).text
    # print(type(json_list))
    res = re.compile(r"MusicJsonCallback.*?{(.*)}", re.S)
    content = re.findall(res, json_list)
    # print(type(content))
    content_1 = '{'+content[0]+'}'
    dict_content = json.loads(content_1)
    # print(dict_content)
    keyword = dict_content["data"]["keyword"]
    # print(keyword)
    list_all = dict_content["data"]["song"]["list"]
    # print(list_all)
    mid_list = []
    music_title_list = []
    for index, for_dict in enumerate(list_all):
        print('_' * 100)
        # 专辑名
        album_name = for_dict["album"]["title"]
        # new url
        mid_list.append(for_dict["mid"])
        # 歌名
        music_title = for_dict["title"]
        music_title_list.append(music_title)
        # 歌手
        singer_name = for_dict["singer"][0]["title"]
        print(" ", index + 1, ">>>", music_title, "          ", singer_name, "               ", album_name)
    number = int(input("要下载第第几首歌（根据序号）\n"))

    down_music(mid_list=mid_list, number=number, music_title_list=music_title_list)

def down_music(mid_list, number, music_title_list):
    url = f"https://u.y.qq.com/cgi-bin/musicu.fcg?callback=getplaysongvkey12314283393950355&g_tk=5381&jsonpCallback=getplaysongvkey12314283393950355&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data=%7B%22req_0%22:%7B%22module%22:%22vkey.GetVkeyServer%22,%22method%22:%22CgiGetVkey%22,%22param%22:%7B%22guid%22:%224357915898%22,%22songmid%22:[%22{mid_list[number-1]}%22],%22songtype%22:[0],%22uin%22:%220%22,%22loginflag%22:1,%22platform%22:%2220%22%7D%7D,%22comm%22:%7B%22uin%22:0,%22format%22:%22json%22,%22ct%22:20,%22cv%22:0%7D%7D"

    join_url = requests.get(url).text
    res = re.compile(r"getplaysongvkey.*?{(.*)}", re.S)
    url_content = re.findall(res, join_url)
    char_url = "{" + url_content[0] + "}"
    dict_url = json.loads(char_url)
    finally_url = "http://183.60.23.13/amobile.music.tc.qq.com/" + dict_url["req_0"]["data"]["midurlinfo"][0]["purl"]
    name_cd = music_title_list[number - 1]
    print(name_cd)
    
    with open(name_cd + ".mp3", "wb")as fp:
        fp.write(requests.get(finally_url).content)
    print("歌曲已下载完成！")


if __name__ == "__main__":
    print('*' * 49)
    print("-"*16+"音乐下载器"+"-"*16)
    print('*' * 49)
    name = input("请输入要下载的歌名\n>>> ")
    music(name=name)
