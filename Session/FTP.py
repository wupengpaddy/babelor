# coding=utf-8
# Copyright 2018 StrTrek Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ftplib
from Message.Message import URL


class FTP:
    def __init__(self, conn: str, set_pasv=True):
        self.conn = URL(conn)
        self.set_pasv = set_pasv

    def send(self, filepath: str):
        ftp = ftplib.FTP()
        ftp.connect(self.conn.hostname, self.conn.port)     # 连接
        ftp.login(self.conn.username, self.conn.password)   # 登录
        ftp.set_pasv(self.set_pasv)                         # 被动模式
        with open(filepath, 'rb') as attachment:
            ftp.storbinary('STOR ' + filepath.split("/")[-1], attachment)  # 上传文件
        ftp.close()
