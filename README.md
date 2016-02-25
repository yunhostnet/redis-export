#VERSON

1.0.0

# redis-export

Redis导入导出工具（json格式）

#INSTALL MODEL

pip install progressbar
pip install redis
pip install optparse 

#

Usage: redis_export.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -H HOST, --host=HOST  Server hostname (default: 127.0.0.1).
  -P PORT, --port=PORT  Server port (default: 6379).
  -p PASSWD, --passwd=PASSWD
                        Password to use when connecting to the server.
  -f FILE, --file=FILE  import and export file.
  -t TYPE, --type=TYPE  import or export or count type.
  -d DB, --db=DB        Database number (default: 0).

#
注意：

暂只支持(string,hash,set(有序的))数据类型，也是常用的。



