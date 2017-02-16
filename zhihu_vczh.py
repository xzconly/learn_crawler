import requests
import json
import os
import time


class Model(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ('{} = ({})'.format(k, v)
                      for k, v in self.__dict__.items())
        return '\n<{}:\n {}\n>'.format(classname, '\n'.join(properties))


class Answer(Model):
    def __init__(self):
        self.question = ''
        self.question_time = 0
        self.answer = ''
        self.author = ''
        self.vote_num = 0
        self.update_time = ''


def log(*args, **kwargs):
    with open('vczh_answers.txt', 'a', encoding='utf-8') as f:
        print(*args, file=f, **kwargs)


def get_dt(int_time):
    value = time.localtime(int_time)
    fmt = '%Y/%m/%d %H:%M:%S'
    dt = time.strftime(fmt, value)
    return dt


def set_headers():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    authorization = 'Bearer Mi4wQUFEQTduTXRBQUFBUUVDMnNmeWhDUmNBQUFCaEFsVk5LemUtV0FEMUg3WFhwVjZZWThKYTE4NE5fVXg0WXQxR01R|1487138297|e0cd80d2bdf0f56e4f1aa9ddac3571b7a2d59eb2'
    x_udid = 'AEBAtrH8oQmPTkCdrrgCju7b4l0YiBLq-9E='
    headers = {
        'User-Agent': user_agent,
        'authorization': authorization,
        'x-udid': x_udid,
    }
    return headers


def cached_url(url, filename):
    path = os.path.join('cached_vczh', filename)
    if os.path.exists(path):
        with open(path, 'r') as f:
            s = f.read()
            return json.loads(s)
    else:
        headers = set_headers()
        r = requests.get(url, headers=headers, verify=False)
        with open(path, 'w') as f:
            f.write(r.text)
        return r.json()


def answer_from_data(data):
    answer = Answer()
    answer.question = data['question']['title']
    answer.question_time = get_dt(data['question']['updated_time'])
    answer.answer = data['excerpt']
    answer.author = data['author']['name']
    answer.vote_num = data['voteup_count']
    answer.update_time = get_dt(data['updated_time'])
    return answer


def answer_from_url(url, filename):
    datas = cached_url(url, filename)
    answers = [answer_from_data(data) for data in datas['data']]
    return answers


def main():
    for i in range(713):
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/answers?include=data%5B*%5D.is_normal%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.voting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20&sort_by=created'.format(i*20)
        filename = str(i) + '.html'
        ans = answer_from_url(url, filename)
        log(ans)


if __name__ == '__main__':
    main()
