#!/usr/bin/env python3
import requests
import yaml
import sys
import unittest


def main():
    authorities = load_yaml("./authorities.yml")["authorities"]

    for i, authority in enumerate(authorities):
        setattr(FeedbackUrlTest,
                f"test_feedback_url_{authority['name']}_{i}",
                generate_test(authority))

    unittest.main()


def load_yaml(path):
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)


class FeedbackUrlTest(unittest.TestCase):
    pass


def generate_test(authority):
    def test(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        try:
            r = requests.get(authority["feedbackUrl"],
                             timeout=30, headers=headers)
            self.assertEqual(r.status_code, 200)

        except requests.exceptions.ReadTimeout:
            self.fail("timeout")
        except requests.exceptions.ConnectTimeout:
            self.fail("connect timeout")
        except requests.exceptions.ConnectionError:
            self.fail("connection error")
    return test


if __name__ == "__main__":
    main()
