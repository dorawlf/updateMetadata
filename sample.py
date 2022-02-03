from http import client
from zeep import Client, Settings

class SoapAPIClient:
    def login(
        self,
        username: str,
        password: str
    ):
        client = Client('enterprise.wsdl')
        service = client.create_service(
            '{urn:enterprise.soap.sforce.com}SoapBinding',
            'https://login.salesforce.com/services/Soap/c/52.0'
        )
        
        login_result = service.login(username,password)

        return login_result

class MetadataAPIClient:    
    session_id = None
    metadata_server = None

    def getservice(self):
        client = Client('metadata.wsdl')
        client._default_soapheaders = {
            'SessionHeader':{"sessionId" : self.session_id}
        }
        service = client.create_service(
            '{http://soap.sforce.com/2006/04/metadata}MetadataBinding',
            self.metadata_server
        )

        return service     

def test():
    _sfdcclient_ = SoapAPIClient
    _metadataclient_ = MetadataAPIClient
    login_result = _sfdcclient_.login(_sfdcclient_,'xxxx@xxx.com','xxxxx')
    _metadataclient_.session_id = login_result.sessionId
    _metadataclient_.metadata_server = login_result.metadataServerUrl
    myservice = _metadataclient_.getservice(_metadataclient_)
    client = Client('metadata.wsdl')
    cf_type = client.get_type('ns0:CustomField')
    _targetmeta_ = cf_type(fullName='MyCloud__c.testdata__c',label='TestField',type='Number',precision=8,scale=2,trackHistory=True)
    print(_targetmeta_)
    
    updateresult  = myservice.updateMetadata([_targetmeta_])
    print(updateresult)

test()
