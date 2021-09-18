import os


class Config:
    """ Configuration class """
    # Type: os.urandom(24) into the command line to generate a new secret key
    SECRET_KEY = '<your secret key>'

    # When inserting service credentials, keep the speech marks eg:
    # AUTHENTICATOR_DISCOVERY = '0000000000000'

    # Insert Watson Discovery credentials here
    AUTHENTICATOR_DISCOVERY = '<your Discovery iam api key>'
    DISCOVERY_SERVICE_URL = '<your Discovery URL>'
    # Insert Watson Natural Language Understanding credentials here
    AUTHENTICATOR_NLU = '<your NLU iam api key>'
    NLU_SERVICE_URL = '<your NLU URL>'
  
  
  

  