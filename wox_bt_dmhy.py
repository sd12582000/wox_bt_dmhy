#encoding=utf8

#Your class must inherit from Wox base class https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#The wox class here did some works to simplify the communication between Wox and python plugin.

from wox import Wox,WoxAPI
from dmhy_helper import DMHYHelper
from synology_download_station_api import SynologyDownloadStationAPI
import pyperclip
class Wox_BT_DMHY(Wox):
    def __init__(self):
        super().__init__()
    from os.path import abspath, join, dirname
    from json import load
    file_path = join(abspath(dirname(__file__)), "config.json")
    config = {}
    with open(file_path, 'r',encoding='utf-8') as json_file:
        config = load(json_file)

    if config['use_synology_download_station']:
        download_station = SynologyDownloadStationAPI(config['synology_myds_url'])
        res = download_station.login(config['synology_account'], config['synology_passwd'])

    helper = DMHYHelper(config['use_filter'], config['allow_sort'])

    def onclick_event(self, magnet_link):
        """
        user click resource
        """
        if self.config['use_synology_download_station']:
            self.download_magnet(magnet_link)
        else:
            self.copy_link(magnet_link)

    def download_magnet(self, magnet_link):
        """
        Creat download magnet task
        """
        self.download_station.creat_task(magnet_link)

    def copy_link(self, magnet_link):
        """
        copy magnet_link into clipboard
        """
        pyperclip.copy(magnet_link)

    def get_wox_result(self, req_data):
        """
        paser req_data to wox_option
        """
        results = []
        for data in req_data:
            results.append({
                "Title":data['title'],
                "SubTitle":data['time'],
                "IcoPath":"magnet.png",
                "JsonRPCAction":{"method": "onclick_event", "parameters": [data['magnet']]},
                "dontHideAfterAction":True
                })
        return results

    def query(self, query):
        """
        search resource
        """
        results = []
        if self.config['use_synology_download_station'] and self.download_station.has_error():
            error_message = self.download_station.get_error_message()
            results.append({
                "Title":'SynologyDownloadStation Error',
                "SubTitle":error_message,
                "IcoPath":"magnet.png",
                "JsonRPCAction":{"method": "copy_link", "parameters": [error_message]},
                "dontHideAfterAction":True
                })
            return results

        query = query.strip()
        req_data = []
        if query:
            if query == 'all':
                req_data = self.helper.get_all_resource()
            else:
                req_data = self.helper.search_resource(query)
            return self.get_wox_result(req_data)
        else:
            if self.config['default_all']:
                req_data = self.helper.get_all_resource()
                return self.get_wox_result(req_data)
            else:
                for defult_key in self.config['default_key']:
                    results.append({
                        "Title":defult_key['Name'],
                        "SubTitle": defult_key['Key'],
                        "IcoPath":"magnet.png",
                        "JsonRPCAction":{"method": "Wox.ChangeQuery"
                                                , "parameters": ['dmhy {}'.format(defult_key['Key'])
                                                                    , True]},
                        "dontHideAfterAction":True
                        })
        return results

#Following statement is necessary
if __name__ == "__main__":
    Wox_BT_DMHY()
