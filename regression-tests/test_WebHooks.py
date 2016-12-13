import requests
import mmap
import re
import time
import os
from test_helper import ApiTestCase

class TestWebHooks(ApiTestCase):

    def test_webhooks(self):
        self.writeCmdToConsole("addWebHook(events, ck)")
        self.reportFunc('webhooktest', '1.4.3.1', '1234', False); 
        self.allowFunc('webhooktest', '1.4.3.2', '1234'); 
        self.resetFunc('webhooktest', '1.4.3.3'); 
        self.addBLEntryLogin('webhooktest', 10, 'This is not a reason'); 
        time.sleep(11)
        self.addBLEntryLogin('webhooktest', 10, 'This is not a reason'); 
        self.delBLEntryLogin('webhooktest');
        time.sleep(5)
        logfile = open('/tmp/webhook-server.log', 'r')
        s = mmap.mmap(logfile.fileno(), 0, access=mmap.ACCESS_READ)
        for event in [ 'report', 'allow', 'reset', 'addbl', 'delbl', 'expirebl' ]:
            regex = r"digest_match=True, event=" + re.escape(event)
            result = re.search(regex, s);
            self.assertNotEquals(result, None)