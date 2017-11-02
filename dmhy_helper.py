class DMHYHelper:
    """
    Process Dhmy rss resource
    """
    def __init__(self, use_filter=True, allow_sort=['sort-2']):
        self.headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        self.url_format = "https://share.dmhy.org/topics/list?keyword={}"
        self.url_all = "https://share.dmhy.org/topics/list/page/1"
        self.allow_sort = allow_sort
        self.use_filter = use_filter

    def get_raw_title(self, item):
        '''
        filter title string
        '''
        title_tag = item.find('td', class_='title')
        raw_title = title_tag.find('a', target="_blank").text
        return str(raw_title).strip()

    def get_post_time(self, item):
        '''
        get resource post time
        '''
        return str(item.find('span').text).strip()

    def get_sort_type(self, item):
        '''
        get sort types array
        "sort-2" title="動畫"
        "sort-31" title="季度全集"
        "sort-3" title="漫畫"
        "sort-41" title="港台原版"
        "sort-42" title="日文原版"
        "sort-4" title="音樂"
        "sort-43" title="動漫音樂"
        "sort-44" title="同人音樂"
        "sort-15" title="流行音樂"
        "sort-6" title="日劇"
        "sort-7" title="ＲＡＷ"
        "sort-9" title="遊戲"
        "sort-17" title="電腦遊戲"
        "sort-18" title="電視遊戲"
        "sort-19" title="掌機遊戲"
        "sort-20" title="網絡遊戲"
        "sort-21" title="遊戲周邊"
        "sort-12" title="特攝"
        "sort-1" title="其他"
        '''
        return item.find('a')['class']

    def get_magnet_link(self, item):
        '''
        get download link
        '''
        return item.find('a', class_='download-arrow arrow-magnet')['href']

    def reconstruct_item(self, item):
        '''
        tranfer html tag to raw data
        '''
        result = {'title':'', 'sort':'None', 'magnet':'None', 'time':'None'}
        result['time'] = self.get_post_time(item)
        result['sort'] = self.get_sort_type(item)
        result['title'] = self.get_raw_title(item)
        result['magnet'] = self.get_magnet_link(item)
        return result

    def judge_resource(self, resource_sort):
        """
        judge sort type need
        """
        if not self.use_filter:
            return True
        for ac_sort in self.allow_sort:
            if ac_sort in resource_sort:
                return True
        return False

    def get_request_result(self, search_url):
        '''
        get http result
        '''
        import requests
        from bs4 import BeautifulSoup
        req = requests.get(search_url, headers=self.headers)
        soup = BeautifulSoup(req.text, "html5lib")
        original_list = soup.find('tbody')
        tr_items = original_list.find_all('tr', class_='')
        result = []
        for item in tr_items:
            pro_item = self.reconstruct_item(item)
            if self.judge_resource(pro_item['sort']):
                result.append(pro_item)
        return result

    def get_all_resource(self):
        """
        get all resource
        """

        return self.get_request_result(self.url_all)

    def search_resource(self, search_key):
        """
        search target key resource
        """

        return self.get_request_result(self.url_format.format(search_key))

if __name__ == '__main__':
    from os.path import abspath, join, dirname
    from json import load
    file_path = join(abspath(dirname(__file__)), "config.json")
    config = {}
    with open(file_path, 'r',encoding='utf-8') as json_file:
        config = load(json_file)
    print(config['use_filter'])
    print(config['use_filter']==True)
    print(config['use_filter']==False)
    #print(config['allow_sort'])
    #print(config['default_key'][:2])
    
    #print('ccc')
    #helper = DMHYHelper()
    #temp = helper.get_all_resource()
    #temp = helper.search_resource('%E8%AA%BF%E6%95%99%E5%92%96')
    #for item in temp:
    #    print(item['title'])
