from Access_articles import *
from db_connect import MySQLHelper


if __name__=="__main__":
    app = ArticleDetail()
    print('默认存储路径为：' + app.root_path)
    screen_text = '''请输入数字功能键！
        数字键1：获取公众号主页链接（输入公众号下任意一篇已发布的文章链接（只是文章链接）即可）
        数字键2：获取公众号下文章列表（每页约有文章几十篇,时间可能会很长）
        数字键3：下载文章内容，自动下载文章列表中所有文章内容
        数字键4：同功能3，下载文章内容，包括单个文章的文本内容 + 阅读量 + 点赞数等信息
                （请注意请求间隔，若请求太多太快可能会触发封禁！！）
        数字键5：查看已存储公众号表及统计信息
    输入其他任意字符退出！'''
    print('欢迎使用，' + screen_text)
    while True:
        text = str(input('请输入功能数字：'))

        if text == '1':
            random_url = (input('（默认公众号主页链接为“研招网资讯”，按回车键使用）\n请输入公众号下任意一篇已发布的文章链接：') or
                          'https://mp.weixin.qq.com/s/4r_LKJu0mOeUc70ZZXK9LA')
            app.get_article_link(random_url)
            print('\n' + screen_text)

        elif text == '2':
            access_token = input('\n以下内容需要用到fiddler工具     ！！！！！\n（1）在微信客户端打开步骤1获取到的链接，\n'
                  '（2）在fiddler中查看——主机地址为https://mp.weixin.qq.com，URL地址为：/mp/profile_ext?acti\n'
                  '（3）选中此项后按快捷键：Ctrl+V，复制此网址到剪贴板\n（4）将该内容粘贴到此处 (づ￣ 3￣)づ\n请输入复制的链接：')
            pages = input('\n########## 默认获取第 1 页文章（约15篇）。如需公众号下全部文章，请输入：0 ##########\n'
                          '请估算后输入需要下载的最新发布文章的页数(例：1)：') or 1
            app.access_origin_list(access_token, int(pages))
            print('\n' + screen_text)

        elif text == '3':   # 该功能不需要token
            text_names3 = input('请输入 已下载文章列表的公众号名称 或 公众号的一篇文章链接(例如：泰山风景名胜区)：')
            save_img = input('是否保存图片？是(输入任意值)，否(默认，直接按回车跳过)') or False
            app.get_list_article(text_names3, save_img)
            print('\n' + screen_text)

        elif text == '4':
            access_token = input('\n以下内容需要用到fiddler工具！！！！！\n（1）在微信客户端打开步骤1获取到的链接，\n'
                          '（2）在fiddler中查看——主机地址为https://mp.weixin.qq.com，URL地址为：/mp/profile_ext?acti\n'
                          '（3）选中此项后按快捷键：Ctrl+U，复制此网址到剪贴板\n（4）将该内容粘贴到此处 (づ￣ 3￣)づ\n请输入复制的链接：')
            app.get_detail_list(access_token)
            print('\n未成功获取的链接已保存到本地。' + '\n' + screen_text)

        # elif text == '5':
        #     db = MySQLHelper()
        #     tables = db.get_all_public_account_tables(prefix='articles_')
        #     print(f'\n当前已爬取公众号数量：{len(tables)}')
        #     print(f'{"公众号名称":<16} {"表名":<28} {"文章数量":<8}')
        #     for t in tables:
        #         count = db.get_table_article_count(t)
        #         pub_name = t[len('articles_'):] if t.startswith('articles_') else t
        #         print(f'{pub_name:<16} {t:<28} {count:<8}')
        #     db.close()
        #     print('\n' + screen_text)
        elif text == '5':
            db = MySQLHelper()
            tables = db.get_all_public_account_tables(prefix='articles_')
            print(f'\n当前已爬取公众号数量：{len(tables)}')

            # 定义列宽（可根据实际最长内容调整）
            name_width = 16  # 公众号名称列宽
            table_width = 28  # 表名列宽
            count_width = 8  # 文章数量列宽

            # 打印表头（用短横线分隔，与列宽匹配）
            print(f'{"公众号名称":<{name_width}} {"表名":<{table_width}} {"文章数量":<{count_width}}')
            print('-' * (name_width + table_width + count_width + 2))  # 分隔线（+2 是空格间隔）

            for t in tables:
                count = db.get_table_article_count(t)
                pub_name = t[len('articles_'):] if t.startswith('articles_') else t

                # 格式化输出：左对齐，不足补空格
                print(f'{pub_name:<{name_width}} {t:<{table_width}} {str(count):<{count_width}}')

            db.close()
            print('\n' + screen_text)


        else:
            print('\n已成功退出！')
            break


