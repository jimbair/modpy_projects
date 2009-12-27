# No she-bang required, called with mod_python.
# This is a test project for myself to get familar
# with how mod_python works. No framework required,
# just wanted a simple whois web app using python.
#
# James Bair - 2009-12-17
# v1.0 - Initial coding

import commands
import os
import re

from mod_python import apache
from mod_python import util

def preWrapCommand(string=''):
    """
    Runs the given command locally on the system.
    If any errors, False is returned. Otherwise, 
    the output is returned wrapped in pre tags.
    """

    if string == '':
        return False

    results = commands.getstatusoutput(string)
    if results[0] is not 0:
        return False

    result = '<pre>%s</pre>' % (results[1],)
    return result

def cleanUp(string=''):
    """
    Used to 'clean up' the input given to us by the
    user. Helpful for keeping away '1337 h4x0rz'.
    If bad input is given, then None is returned.
    Only accepts letters, numbers, and periods.
    """

    if string == '':
        return None

    # Check for long length
    if len(string) > 100:
        return None

    # Check for bad chars
    for i in string:
        test = re.search('\w|\.', i)
        if test is None:
            return None
    
    return string

def handler(req):
    """
    The mod_python equivalent of main().
    """
    
    # Yucky HTML variables.
    top = "<html><head /><title>Simple Whois Form</title>"
    bottom = "</html>"
    whoisForm = """<form name="input" action="%s" method="get">
    Domain:
    <input type="text" name="domain" />
    <input type="submit" value="Submit" />
    </form>""" % (os.path.basename(__file__),)

    # Basic HTML requirements
    req.content_type = 'text/html'
    req.send_http_header()
    req.write(top)

    # See if we have a domain yet
    formdata = util.FieldStorage(req)
    if 'domain' in formdata:
        domain = formdata['domain']
        # Sanity checking our input
        domain = cleanUp(domain)
    else:
        domain = None

    # Only show a form if no domain is present.
    if domain is None:
        req.write(whoisForm)
    else:
        whois = preWrapCommand('whois %s' % (domain,))
        if whois is not False:
            req.write(whois)

    req.write(bottom)
    return apache.OK
