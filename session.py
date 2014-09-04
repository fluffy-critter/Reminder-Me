import cgi
import cgitb
import os

cgitb.enable()

_form = cgi.FieldStorage()
ipAddr = os.getenv('REMOTE_ADDR')

_user = None

def form():
    """Gets the parsed CGI form values. MUST be retrieved from here."""
    global _form
    return _form

def argv():
    """ Get the page action

        argv[0] is a server-relative path to the script handler
        argv[1..n] are the REST parameters
        
        i.e. http://example.com/larry/foo.py/handleBlah/more -> ['/larry/foo.py', 'handleBlah', 'more']
    """

    argv=[os.getenv('SCRIPT_NAME')]
    path=os.getenv('PATH_INFO')
    if path:
        argv.extend(path.split('/')[1:])
    return argv

def request_server_path(uri=''):
    """Prepends the server URL to a request URI"""
    https = (os.getenv('HTTPS') == 'on')
    expectedPort = https and '443' or '80'
    actualPort = os.getenv('SERVER_PORT')
    if uri == '/':
            uri = ''
    return '%s://%s%s%s' % (https and 'https' or 'http',
                          os.getenv('SERVER_NAME'),
                          (expectedPort != actualPort) and (':%s' % actualPort) or '',
                          uri)

def request_script_dir():
    """Gets the URL to the script's directory"""
    return request_server_path(os.path.dirname(os.getenv('SCRIPT_NAME') or ''))

def request_script_path():
    """Gets the URL of the accessed script"""
    return request_server_path(os.getenv('SCRIPT_NAME') or '')
    
