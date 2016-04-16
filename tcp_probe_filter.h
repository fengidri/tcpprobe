/**
 *   author       :   丁雪峰
 *   time         :   2016-04-15 13:32:02
 *   email        :   fengidri@yeah.net
 *   version      :   1.0.1
 *   description  :
 */
#ifndef  __TCP_PROBE_FILTER_H__
#define __TCP_PROBE_FILTER_H__
struct filter{
    unsigned int saddr;
    unsigned int daddr;
    unsigned int sport;
    unsigned int dport;
};
bool tcpprobe_filter_qualified(struct sock *sk, struct sk_buff *skb);
extern const struct file_operations tcpprobe_filter_fops;
#endif


