import jwt
import time
import hashlib
import requests
from urllib.parse import quote

class Client():
    """
    A class used connect and interact with Wildix WMS5 API.

    ...

    Attributes
    ----------
    secret : str
        secret generated on WMS admin panel
    app_id : str
        the ID of the app generated on WMS admin panel
    app_name : str
        the name of the app generated on WMS admin panel
    host : srt
        the name of the PBX

    Methods
    -------
    get
        create a GET query
    post
        create a POST query
    __generate_request_string
        generate strint used to create JWT
    __generate_jwt
        generate JWT using request string and class attributes
    __encode_url
        encode API URL used on get or post query
    """
    
    def __init__(self, config):
        """
        Constructor with config parametres received in a dictionary
        
        ...
        Config parameters
        -----------------
        config["pbx_secret_key"]
            secret generated on WMS admin panel
        config["x_app_id"]
            ID generated on WMS admin panel
        config["app_name"]
            App's name generated on WMS admin panel
        config["pbx_host"]
            PBX host name
        """
        self.secret = config["pbx_secret_key"]
        self.app_id = config["app_id"]
        self.app_name = config["app_name"]
        self.host = config["pbx_host"]
    
    @property
    def secret(self):
        return self._secret
    
    @secret.setter
    def secret(self, pbx_secret_key):
        if pbx_secret_key:
            self._secret = pbx_secret_key
        else:
            raise ValueError("Secret key not found. Verify config parameters")

    @property
    def app_id(self):
        return self._app_id
    
    @app_id.setter
    def app_id(self, app_id):
        if app_id:
            self._app_id = app_id
        else:
            raise ValueError("APP ID not found. Verify config parameters")

    @property
    def app_name(self):
        return self._app_name
    
    @app_name.setter
    def app_name(self, app_name):
        if app_name:
            self._app_name = app_name
        else:
            raise ValueError("APP Name not found. Verify config parameters")

    @property
    def pbx_host(self):
        return self._pbx_host
    
    @pbx_host.setter
    def pbx_host(self, pbx_host):
        if pbx_host:
            self._pbx_host = pbx_host
        else:
            raise ValueError("APP Name not found. Verify config parameters")

    def __generate_request_string(self, options):
        """
        Method to generate request string. Used on JWT creation.

        Order parmaters is important on request estring generation
        """

        # Check if "url" parameter is in options. If not, script finishes
        if "url" in options.keys():
            request_string = "{}{}host:{};x-app-id:{};".format(
                    self.__method,
                    options["url"],
                    self.host,
                    self.app_id,
                )
        else:
            raise ValueError("Query URL not found")

        # Check if "count" parameter is in options to add on request string
        if "count" in options.keys() and options["count"]:
            request_string += "count:{};".format(options["count"])
        
        # Check if "field" parameter is in options to add on request string
        if "fields" in options.keys():
                request_string += "fields:{};".format(options["fields"])
        
        # Check if "start" parameter is in options to add on request string
        if "start" in options.keys() and options["start"]:
            request_string += "start:{};".format(options["start"])

        return request_string
    
    def __generate_jwt(self, request_string):
        """
        Method to create Jason Web Tocken to authenticate with Wildix PBX
        """

        hash_string = hashlib.sha256(request_string.encode())
        timestamp = round(time.time())
        expire = 1*60

        payload = {
            'iss': self.app_name,
            'iat': timestamp,
            'exp': timestamp + expire,
            'sign': {
                'alg': 'sha256',
                'headers': {
                        '0': 'Host',
                        '1': 'X-APP-ID',
                },
                'hash': hash_string.hexdigest(),
            },
        }

        encoded_jwt = jwt.encode(payload, self.secret, algorithm='HS256')
        return encoded_jwt
    
    def __encode_url(self, options):
        """
        Method to create the URL that will send to PBX.
        """
        url = "https://" + self.host + options["url"] + "?"
        if "count" in options.keys() and options["count"]:
            url += "count={}".format(options["count"])
        
        if options["fields"]:
            url += "&fields=" + options["fields"]
        
        if "start" in options.keys() and options["start"]:
            url += "&start={}".format(options["start"])

        return url

    def query_get(self, options):
        """
        Method to query WMS API through GET method.
        """
        self.__method = "GET"
        request_string = self.__generate_request_string(options)
        jwt = self.__generate_jwt(request_string).decode()
        head = {'Host': self.host, 'X-APP-ID': self.app_id, 'Authorization': 'Bearer {}'.format(jwt)}
        url = self.__encode_url(options)
        return requests.get(url, headers = head)