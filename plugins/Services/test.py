###
# Copyright (c) 2002-2004, Jeremiah Fincher
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

from supybot.test import *

class ServicesTestCase(PluginTestCase):
    plugins = ('Services', 'Config')
    config = {
        'plugins.Services.NickServ': 'NickServ',
        'plugins.Services.ChanServ': 'ChanServ',
        }

    def testPasswordAndIdentify(self):
        self.assertNotError('services password foo bar')
        self.assertError('services identify') # Don't have a password.
        self.assertNotError('services password %s baz' % self.nick)
        m = self.assertNotError('services identify')
        self.failUnless(m.args[0] == 'NickServ')
        self.failUnless(m.args[1].lower() == 'identify baz')
        self.assertNotError('services password %s biff' % self.nick)
        m = self.assertNotError('services identify')
        self.failUnless(m.args[0] == 'NickServ')
        self.failUnless(m.args[1].lower() == 'identify biff')

    def testPasswordConfg(self):
        self.assertNotError('config plugins.Services.nicks ""')
        self.assertNotError('config network plugins.Services.nicks ""')

        self.assertNotError('services password %s bar' % self.nick)

        self.assertResponse(
            'config plugins.Services.nicks',
            'Global:  ; test: %s' % self.nick)
        self.assertResponse(
            'config plugins.Services.nickserv.password.%s' % self.nick,
            'Global: bar; test: bar')

        self.assertNotError(
            'config network plugins.Services.nickserv.password.%s bar2'
            % self.nick)
        self.assertResponse(
            'config plugins.Services.nickserv.password.%s' % self.nick,
            'Global: bar; test: bar2')
        self.assertResponse(
            'config plugins.Services.nickserv.password.%s' % self.nick,
            'Global: bar; test: bar2')

        m = self.assertNotError('services identify')
        self.failUnless(m.args[0] == 'NickServ')
        self.failUnless(m.args[1].lower() == 'identify bar2')


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

