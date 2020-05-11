import urllib.request,json
from .models import Quote


# Getting the quote base url
base_url = None
def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']

def get_quote():
    '''
    Function gets the JSON response to url request
    '''  

    with urllib.request.urlopen(base_url) as url:
        quote_details_data = url.read()
        quote_details_response = json.loads(quote_details_data)

        quote_object = None
        if quote_details_response:
            id = quote_details_response.get('id')
            author = quote_details_response.get('author')
            quote = quote_details_response.get('quote')
            
           

            quote_object = Quote(id,author,quote)

    return quote_object
               