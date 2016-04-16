/**
 *   author       :   丁雪峰
 *   time         :   2016-04-15 13:07:56
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#include <linux/kernel.h>
#include <linux/kprobes.h>
#include <linux/module.h>
#include <linux/inet.h>
#include <net/tcp.h>
#include "tcp_probe_filter.h"

struct filter tcpprobe_filter = {
    .dport = 80,
};

bool tcpprobe_filter_qualified(struct sock *sk, struct sk_buff *skb)
{
	//const struct tcp_sock *tp = tcp_sk(sk);
	const struct inet_sock *inet = inet_sk(sk);

    if (tcpprobe_filter.daddr > 0 && inet->inet_daddr != tcpprobe_filter.daddr)
        return false;

    if (tcpprobe_filter.saddr > 0 && inet->inet_saddr != tcpprobe_filter.saddr)
        return false;

    if(tcpprobe_filter.sport > 0 &&
            ntohs(inet->inet_sport) != tcpprobe_filter.sport)
        return false;

    if(tcpprobe_filter.dport > 0 &&
            ntohs(inet->inet_dport) != tcpprobe_filter.dport)
        return false;

    return true;
}


static ssize_t tcpprobe_filter_write(struct file *file, const char *data,
        size_t len, loff_t *off)
{
    if (len < sizeof(tcpprobe_filter))
        return -EFAULT;

    if(copy_from_user((void *)&tcpprobe_filter, data, sizeof(tcpprobe_filter)))
        return -EFAULT;

    return len;
}

static ssize_t tcpprobe_filter_read(struct file *file, char __user *buf,
			     size_t len, loff_t *ppos)
{
    char buffer[1024];
    int cnt;
	if (!buf)
		return -EINVAL;
    if (len < sizeof(buffer))
		return -EINVAL;

    if (*ppos > 0)
        return 0;

    cnt = snprintf(buffer, sizeof(buffer),
            "tcp probe filter: %lu\n"
            "saddr: %u\n"
            "daddr: %u\n"
            "sport: %u\n"
            "dport: %u\n",
            sizeof(tcpprobe_filter),
            tcpprobe_filter.saddr,
            tcpprobe_filter.daddr,
            tcpprobe_filter.sport,
            tcpprobe_filter.dport);

    if (copy_to_user(buf, buffer,  cnt))
        return -EFAULT;

    *ppos += cnt;
    return cnt;
}

const struct file_operations tcpprobe_filter_fops = {
	.owner	 = THIS_MODULE,
	.read    = tcpprobe_filter_read,
	.write   = tcpprobe_filter_write,
};
