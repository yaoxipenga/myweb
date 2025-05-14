import pymysql

# 数据库连接配置
db_config = {
    'host': '10.32.176.36',  # 你的数据库 IP
    'user': 'site',
    'password': '123456',
    'database': 'movie_db',
    'charset': 'utf8mb4'  # 确保支持中文字符
}

# 资源数据
site_data = [
    {'title': '注视影视', 'url': 'https://gaze.run/', 'description': '知名免费影视站'},
    {'title': '老地方影视', 'url': 'https://www.laodifang.tv/', 'description': '免费无广告影视站'},
    {'title': '搜片', 'url': 'https://soupian.pro/?utm_source=iui.su', 'description': '全网影视搜索引擎'},
    {'title': 'OK 影视', 'url': 'https://www.freeok.la/', 'description': '免费在线蓝光影院'},
    {'title': 'JOJO 影视', 'url': 'https://kimivod.com/', 'description': '优质追剧网更新快'},
    {'title': '低端影视', 'url': 'https://ddys.pro/', 'description': '知名 1080p 影视站'},
    {'title': '安卓影视 app', 'url': 'https://iui.su/458/', 'description': '安卓免费多线路影视 APP'},
    {'title': '片库', 'url': 'https://www.qn63.com/', 'description': '提供在线播放 + 下载'},
    {'title': '4k 论坛', 'url': 'https://www.4khdr.cn/', 'description': '提供 4k 影视资源下载'},
    {'title': '网盘资源', 'url': 'https://iui.su/3700/', 'description': '提供网盘资源下载'},
    {'title': '迅雷电影天堂', 'url': 'https://dalao.ru/link?target=https://xunlei8.cc/?iui.su', 'description': '提供迅雷网盘 + 百度网盘'},
    {'title': '美剧天堂', 'url': 'https://dalao.ru/link?target=https://mjtt.tv/', 'description': '提供百度 + 阿里 + 在线播放'}
]

try:
    # 建立数据库连接
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 插入数据
    for site in site_data:
        sql = """
            INSERT INTO movie_sites (title, url, description)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (
            site['title'],
            site['url'],
            site['description']
        ))

    conn.commit()
    print("✅ 网站资源数据插入成功！")

except pymysql.MySQLError as e:
    print("❌ 插入失败:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
