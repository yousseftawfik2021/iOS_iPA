#!/usr/bin/env python

import unittest

from you_get.extractors import (
    youtube
)


class YouGetTests(unittest.TestCase):
   

    def test_youtube(self):
      
        #youtube.download('http://youtu.be/pzKerr0JIPA', info_only=True)
        #youtube.download(
        #    'http://www.youtube.com/attribution_link?u=/watch?v%3DldAKIzq7bvs%26feature%3Dshare',  # noqa
        #    info_only=True
        #)
        youtube.download(
            'https://www.youtube.com/watch?v=oRdxUFDoQe0', info_only=True
        )

if __name__ == '__main__':
    unittest.main()
