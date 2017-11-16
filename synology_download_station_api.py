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
        self._error_dic={
            'SYNO.API.Auth':{
            400:'No such account or incorrect password',
            401:'Account disabled',
            402:'Permission denied',
            403:'2-step verification code required',
            404:'Failed to authenticate 2-step verification code'
            },
            'SYNO.DownloadStation.Task':{
            400:'File upload failed',
            401:'Max number of tasks reached',
            402:'Destination denied',
            403:'Destination does not exist',
            404:'Invalid task id',
            405:'Invalid task action',
            406:'No default destination',
            407:'Set destination failed',
            408:'File does not exist',
            }
        }

    def has_error(self):
        """
        return error == {}
        """
        return bool(self._error)

    def get_error_message(self):
        """
        get error code Description
        """
        result = ''
        if self.has_error():
            if self._error['code'] == 100:
                result = 'Unknown error'
            elif self._error['code'] == 101:
                result = 'Invalid parameter'
            elif self._error['code'] == 102:
                result = 'The requested API does not exist'
            elif self._error['code'] == 103:
                result = 'The requested method does not exist'
            elif self._error['code'] == 104:
                result = 'The requested version does not support the functionality'
            elif self._error['code'] == 105:
                result = 'The logged in session does not have permission'
            elif self._error['code'] == 106:
                result = 'Session timeout'
            elif self._error['code'] == 107:
                result = 'Session interrupted by duplicate login'
            else:
                result = self._error_dic[self._error['api']][self._error['code']]
        
        return result

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
            self._error = {}
        else:
            self._error = req['error']
            self._error['api'] = payload['api']
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
            self._error['api'] = payload['api']
        else:
            self._error = {}

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
            self._error['api'] = payload['api']
        else:
            self._error = {}

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
            self._error['api'] = payload['api']
        else:
            self._error = {}

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
            self._error['api'] = payload['api']
        else:
            self._error = {}

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
            self._error['api'] = payload['api']
        else:
            self._error = {}

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
            self._error['api'] = payload['api']
        else:
            self._error = {}

        return req['success']

if __name__ == "__main__":
    """
    test
    """
    sy =  SynologyDownloadStationAPI('http://myds.com:port')
    lresult = sy.login('account','passwd')
    if lresult :
        #print(cr)
        cr = sy.get_task_list()
        #cr = sy.get_config()
        #cr = sy.creat_task('nnounce&tr=http%3A%2F%2F208.67.16.113%3A8000%2Fannounce')
        #print(cr)
        print(sy.has_error())
        print(sy._error)
        print(sy.get_error_message())
        #sy.logout()
    else:
        print(sy.has_error())
        print(sy._error)
        print(sy.get_error_message())
        print('falut')