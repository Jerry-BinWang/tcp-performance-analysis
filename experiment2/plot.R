setwd('~/Projects/tcppa/experiment2/')
results <- read.csv('result.csv')

levels(results$cbr_bandwidth) <- list('1mb'=1, '2mb'=2, '3mb'=3, '4mb'=4, '5mb'=5, '6mb'=6, '7mb'=7, '8mb'=8, '9mb'=9, '10mb'=10)
results$cbr_bandwidth <- as.numeric(results$cbr_bandwidth)
results$rtt_1 <- results$rtt_1 * 1000
results$rtt_2 <- results$rtt_2 * 1000

library(ggplot2)
library(grid)
library(gridExtra)

plot_rtt <- function(series, title, TCP_1, TCP_2) {
  return(ggplot() +
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=rtt_1, color = paste(TCP_1, '(N1 to N4)', sep=' '))) + 
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=rtt_2, color = paste(TCP_2, '(N5 to N6)', sep=' '))) + 
           xlab('CBR bandwidth (Mbps)') + ylab('rtt (ms)') +
           scale_x_continuous(breaks = seq(1, 10)) +
           ggtitle(title) +
           theme(legend.justification = c(0, 0), legend.position = c(0, 0), legend.title = element_blank()))
}

plot_throughput <- function(series, title, TCP_1, TCP_2) {
  return(ggplot() +
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=throughput_1, color = paste(TCP_1, '(N1 to N4)', sep=' '))) + 
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=throughput_2, color = paste(TCP_2, '(N5 to N6)', sep=' '))) + 
           xlab('CBR bandwidth (Mbps)') + ylab('throughput (Mbps)') +
           scale_x_continuous(breaks = seq(1, 10)) +
           ggtitle(title) +
           theme(legend.justification = c(1, 1), legend.position = c(1, 1), legend.title = element_blank()))
}

plot_latency <- function(series, title, TCP_1, TCP_2) {
  return(ggplot() +
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=latency_1, color = paste(TCP_1, '(N1 to N4)', sep=' '))) + 
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=latency_2, color = paste(TCP_2, '(N5 to N6)', sep=' '))) + 
           geom_line(data=series[series$tcp_1 == TCP_1 & series$tcp_2 == TCP_2,], aes(x=cbr_bandwidth, y=latency_2, color = paste(TCP_2, '(N5 to N6)', sep=' '))) + 
           xlab('CBR bandwidth (Mbps)') + ylab('rtt (ms)') +
           scale_x_continuous(breaks = seq(1, 10)) +
           ggtitle(title) +
           theme(legend.justification = c(0, 1), legend.position = c(0, 1), legend.title = element_blank()))
}


series_1 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == -1,
                   select=c(tcp_1, tcp_2, cbr_bandwidth, throughput_1, throughput_2, drop_rate_1, drop_rate_2, rtt_1, rtt_2))

series_2 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == 0.1,
                   select=c(tcp_1, tcp_2, cbr_bandwidth, throughput_1, throughput_2, drop_rate_1, drop_rate_2, rtt_1, rtt_2))


series_3 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == 1,
                   select=c(tcp_1, tcp_2, cbr_bandwidth, throughput_1, throughput_2, drop_rate_1, drop_rate_2, rtt_1, rtt_2))


series_4 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == 5,
                   select=c(tcp_1, tcp_2, cbr_bandwidth, throughput_1, throughput_2, drop_rate_1, drop_rate_2, rtt_1, rtt_2))


series_5 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == 10,
                   select=c(tcp_1, tcp_2, cbr_bandwidth, throughput_1, throughput_2, drop_rate_1, drop_rate_2, rtt_1, rtt_2))


plot_1 <- plot_rtt(series_3, title="Newreno vs Vegas", TCP_1 = 'Newreno', TCP_2 = 'Vegas')
plot_2 <- plot_rtt(series_3, title="Vegas vs Vegas", TCP_1 = 'Vegas', TCP_2 = 'Vegas')
p <- grid.arrange(plot_1, plot_2, ncol = 2)
ggsave('Newreno_vegas.pdf', p, width = 33, height = 16, units = 'cm')

plot_1 <- plot_throughput(series_1, title="CBR before TCP: 1s", TCP_1 = 'Newreno', TCP_2 = 'Reno')
plot_2 <- plot_throughput(series_1, title='CBR after TCP: 0.1s', TCP_1 = 'Newreno', TCP_2 = 'Reno')
plot_3 <- plot_throughput(series_3, title="CBR after TCP: 1s", TCP_1 = 'Newreno', TCP_2 = 'Reno')
plot_4 <- plot_throughput(series_4, title='CBR after TCP: 5s', TCP_1 = 'Newreno', TCP_2 = 'Reno')
plot_5 <- plot_throughput(series_5, title="CBR after TCP: 10s", TCP_1 = 'Newreno', TCP_2 = 'Reno')

p <- grid.arrange(plot_1, plot_2, plot_3, plot_4, plot_5, ncol = 3)
ggsave('Newreno_reno.pdf', p, width = 33, height = 16, units = 'cm')

plot_1 <- plot_throughput(series_1, title="Reno vs Reno", TCP_1 = 'Reno', TCP_2 = 'Reno')
plot_2 <- plot_throughput(series_1, title='NewReno vs Reno', TCP_1 = 'Newreno', TCP_2 = 'Reno')
plot_3 <- plot_throughput(series_1, title="Vegas vs Vegas", TCP_1 = 'Vegas', TCP_2 = 'Vegas')
plot_4 <- plot_throughput(series_1, title='NewReno vs Vegas', TCP_1 = 'Newreno', TCP_2 = 'Vegas')

p <- grid.arrange(plot_1, plot_2, plot_3, plot_4, ncol = 4)
ggsave('Newreno_vegas_throughput.pdf', p, width = 45, height = 8, units = 'cm')
