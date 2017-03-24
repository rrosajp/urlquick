import unittest
import urlquick
import types


class TestPy2Functions(unittest.TestCase):
    def test_quote(self):
        pass

    def test_unquote(self):
        pass

    def test_parse_qsl(self):
        pass

    def test_urlencode(self):
        pass


class TestCaseInsensitiveDict(unittest.TestCase):
    def test_setter(self):
        pass


class TestRequest(unittest.TestCase):
    def test_mehtod_upper(self):
        req = urlquick.Request("get", "https://httpbin.org/get", urlquick.CaseInsensitiveDict())
        self.assertTrue(req.method == "GET")

    def test_with_host(self):
        headers = urlquick.CaseInsensitiveDict()
        headers["host"] = "httpbin.org"
        req = urlquick.Request("get", "https://httpbin.org/get", headers)
        self.assertTrue("host" in req.headers)

    def test_without_host(self):
        req = urlquick.Request("get", "https://httpbin.org/get", urlquick.CaseInsensitiveDict())
        self.assertTrue("host" in req.headers)

    def test_url(self):
        req = urlquick.Request("get", "https://httpbin.org/get", urlquick.CaseInsensitiveDict())
        self.assertTrue(req.url == "https://httpbin.org/get")

    def test_url_params(self):
        req = urlquick.Request("get", "https://httpbin.org/get", urlquick.CaseInsensitiveDict(), params={"test":"yes"})
        self.assertTrue(req.url == "https://httpbin.org/get?test=yes")

    def test_url_referer(self):
        req = urlquick.Request("get", "/get", urlquick.CaseInsensitiveDict(), referer="https://httpbin.org")
        self.assertTrue(req.url == "https://httpbin.org/get")


class TestFromResponse(unittest.TestCase):
    start_time = urlquick.datetime.utcnow()
    class Request(object):
        def __init__(self):
            self.url = "https://httpbin.org/get"

    class Response(object):
        def __init__(self):
            self.status = 200
            self.reason = "OK"

        @staticmethod
        def getheaders():
            return {"conection": "close"}

        @staticmethod
        def read():
            return "data"

        def close(self):
            pass

    def test_from_cache(self):
        org_request = self.Request()
        response_data = {u"body": "data", u"headers": {"conection": "close"}, u"status": 200, u"reason": "OK"}
        resp = urlquick.Response.from_cache(response_data, org_request, self.start_time, [])
        self.assertTrue(resp.ok)

    def test_from_httplib(self):
        org_request = self.Request()
        response_data = self.Response()
        resp = urlquick.Response.from_httplib(response_data, org_request, self.start_time, [])
        self.assertTrue(resp.ok)


class TestResponse(unittest.TestCase):
    resp = None

    @classmethod
    def setUpClass(cls):
        urlquick.cache_cleanup(0)
        cls.resp = urlquick.request("GET", "https://httpbin.org/get")

    def test_ok(self):
        self.assertTrue(self.resp.ok)

    def test_content(self):
        data = self.resp.content
        self.assertTrue(data)

    def test_text(self):
        data = self.resp.text
        self.assertTrue(data)

    def test_json(self):
        data = self.resp.json()
        self.assertTrue(isinstance(data, dict))

    def test_cookies(self):
        is_dict = isinstance(self.resp.cookies, dict)
        self.assertTrue(is_dict)

    def test_headers(self):
        is_dict = isinstance(self.resp.headers, urlquick.CaseInsensitiveDict)
        print(self.resp.headers)
        self.assertTrue(is_dict)

    def test_is_redirect(self):
        self.assertFalse(self.resp.is_redirect)

    def test_is_permanent_redirect(self):
        self.assertFalse(self.resp.is_permanent_redirect)

    def test_iter_content(self):
        data = self.resp.iter_content(decode_unicode=False)
        self.assertTrue(isinstance(data, types.GeneratorType))
        list(data)

    def test_iter_content_unicode(self):
        data = self.resp.iter_content(decode_unicode=True)
        self.assertTrue(isinstance(data, types.GeneratorType))
        list(data)

    def test_iter_lines(self):
        data = self.resp.iter_lines(decode_unicode=False)
        self.assertTrue(isinstance(data, types.GeneratorType))
        list(data)

    def test_iter_lines_unicode(self):
        data = self.resp.iter_lines(decode_unicode=True)
        self.assertTrue(isinstance(data, types.GeneratorType))
        list(data)

    def test_bool(self):
        self.assertTrue(bool(self.resp))

    def test_coverage(self):
        list(self.resp)
        repr(self.resp)

    @classmethod
    def tearDownClass(cls):
        cls.resp.close()


class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = urlquick.Session()

    def setUp(self):
        urlquick.cache_cleanup(0)

    def tearDown(self):
        self.setUp()

    def test_request(self):
        resp = self.session.request("GET", "https://httpbin.org/get")
        self.assertTrue(resp.ok)

    def test_get(self):
        resp = self.session.get("https://httpbin.org/get")
        self.assertTrue(resp.ok)

    def test_head(self):
        resp = self.session.head("https://httpbin.org/get")
        self.assertTrue(resp.ok)




#def test_urlquick():
#    _url = u"https://en.wikipedia.org/wiki/\u0278"
#    ret = urlquick.get(_url, allow_redirects=True)
#    print("Status =", ret.status_code)
#    print("Reason =", ret.reason)
#    print("Encoding =", ret.encoding)
#    print("Elapsed =", ret.elapsed)
#    print("Data =", repr(ret.text[:200]))
#    print("Data Len", len(ret.text))
#    print("Cookie =", ret.cookies)
#    print("===")
#
#    for i in ret.headers.items():
#        print(i)
