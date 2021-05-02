import pexpect


def cmd(x): return "scp -P 10010 netlab@server.netbd.site:~/netlab_lhp/test{}_net.csv /Users/lhy/Downloads/net/test{}_net.csv".format(x, x)


passwd = "netlab"
for i in range(1, 41):
    child = pexpect.spawn(cmd(i))
    child.expect('password:')
    child.sendline(passwd)
    child.read()
