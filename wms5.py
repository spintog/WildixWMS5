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