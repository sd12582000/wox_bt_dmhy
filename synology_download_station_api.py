"""
Synology_Download_Station_Web_API
https://global.download.synology.com/download/Document/DeveloperGuide/Synology_Download_Station_Web_API.pdf
"""
import requests
class SynologyDownloadStationAPI():
    """
    Synology_Download_Station_Web_API
    """
    def __init__(self, url):
        """
        init
        """
        self.root_path = '{}/webapi/'.format(url)
        self._sid = ''
        self._error = {}

    def login(self, account, passwd):
        """
        login get sid
        """
        payload = {'api': 'SYNO.API.Auth',
                   'version': '2',
                   'method':'login',
                   'session':'DownloadStation',
                   'format':'sid',
                   'account':account,
                   'passwd':passwd}

        url = '{}auth.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if req['success']:
            self._sid = req['data']['sid']
        else:
            self._error = req['error']
        return req['success']

    def logout(self, session='DownloadStation'):
        """
        logout
        """
        payload = {'api': 'SYNO.API.Auth',
                   'version': '1',
                   'method':'logout',
                   'session':session,
                  }
        url = '{}auth.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']

        return req['success']

    def get_info(self):
        """
        SYNO.DownloadStation.Info
        """
        payload = {'api': 'SYNO.DownloadStation.Info',
                   'version': '1',
                   'method':'getinfo',
                   '_sid':self._sid
                  }
        url = '{}DownloadStation/info.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']
        return req

    def get_config(self):
        """
        SYNO.DownloadStation.Info GetConfig
        """
        payload = {'api': 'SYNO.DownloadStation.Info',
                   'version': '1',
                   'method':'getconfig',
                   '_sid':self._sid
                  }
        url = '{}DownloadStation/info.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']
        return req

    def set_config(self, parameter):
        """
        SYNO.DownloadStation.Info SetServerConfig
        """
        payload = parameter
        payload['api'] = 'SYNO.DownloadStation.Info'
        payload['version'] = '1'
        payload['method'] = 'setserverconfig'
        payload['_sid'] = self._sid
        url = '{}DownloadStation/info.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']
        return req

    def get_task_list(self):
        """
        SYNO.DownloadStation.Task List
        """
        payload = {'api': 'SYNO.DownloadStation.Task',
                   'version': '1',
                   'method':'list',
                   '_sid':self._sid
                  }
        url = '{}DownloadStation/task.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']
        return req

    def creat_task(self, download_link):
        """
        SYNO.DownloadStation.Task Create
        """
        payload = {'api': 'SYNO.DownloadStation.Task',
                   'version': '3',
                   'method':'create',
                   'uri':download_link,
                   '_sid':self._sid
                  }
        url = '{}DownloadStation/task.cgi'.format(self.root_path)
        req = requests.get(url, params=payload).json()
        if not req['success']:
            self._error = req['error']
        return req['success']

if __name__ == "__main__":
    """
    test
    """
    sy =  SynologyDownloadStationAPI('http://myds.com:5000')
    result = sy.login('admin','12345')
    if result :
        #print(cr)
        cr = sy.get_task_list()
        #cr = sy.get_config()
        #cr = sy.creat_task('magnet:?xt=urn:btih:T2OGRBJBO6Z7GJXS6WAMKJ7HBA5TBSGG&dn=&tr=http%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=udp%3A%2F%2F104.238.198.186%3A8000%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.publicbt.com%3A80%2Fannounce&tr=http%3A%2F%2Ftracker.prq.to%2Fannounce&tr=http%3A%2F%2Fopen.acgtracker.com%3A1096%2Fannounce&tr=http%3A%2F%2Ftr.bangumi.moe%3A6969%2Fannounce&tr=https%3A%2F%2Ft-115.rhcloud.com%2Fonly_for_ylbud&tr=http%3A%2F%2Fbtfile.sdo.com%3A6961%2Fannounce&tr=http%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=https%3A%2F%2Ftr.bangumi.moe%3A9696%2Fannounce&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=http%3A%2F%2F208.67.16.113%3A8000%2Fannounce')
        print(cr)
        #sy.logout()
    else:
        print('falut')