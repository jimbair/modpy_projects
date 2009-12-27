# No she-bang required, called with mod_python.
# This is a test project for myself to get familar
# with how mod_python works. No framework required,
# just wanted a simple whois web app using python.
#
# v1.0 - Initial coding - 2009-12-27
#
# Copyright (C) 2009  James Bair <james.d.bair@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import commands
import os

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
