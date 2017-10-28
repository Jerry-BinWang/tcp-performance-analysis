setwd('~/Projects/tcppa/experiment1/')
results <- read.csv('result.csv')

levels(results$cbr_bandwidth) <- list('1mb'=1, '2mb'=2, '3mb'=3, '4mb'=4, '5mb'=5, '6mb'=6, '7mb'=7, '8mb'=8, '9mb'=9, '10mb'=10)
results$cbr_bandwidth <- as.numeric(results$cbr_bandwidth)
results$rtt <- results$rtt * 1000
names(results)[2] <- 'TCP'

library(ggplot2)
library(grid)
library(gridExtra)

plot_throughtput <- function(series, title) {
  return(ggplot(data=series, aes(x=cbr_bandwidth, y=throughput, colour=TCP)) +
          geom_line() + 
          scale_x_continuous(breaks = seq(1, 10)) +
          scale_y_continuous(breaks = seq(0, 8, 2)) +
          xlab('CBR bandwidth (Mbps)') + ylab('throughput (Mbps)') +
          ggtitle(title))
}


plot_drop_rate <- function(series, title) {
  return(ggplot(data=series, aes(x=cbr_bandwidth, y=drop_rate, colour=TCP)) +
           geom_line() + xlab('CBR bandwidth (Mbps)') + ylab('drop rate (%)') +
           scale_x_continuous(breaks = seq(1, 10)) +
           ggtitle(title))
}

plot_rtt <- function(series, title) {
  return(ggplot(data=series, aes(x=cbr_bandwidth, y=rtt, colour=TCP)) +
           geom_line() + xlab('CBR bandwidth (Mbps)') + ylab('rtt (ms)') +
           scale_x_continuous(breaks = seq(1, 10)) +
           ggtitle(title))
}

series_1 <- subset(results, latency =='1ms' & cbr_packet_size == 100 & start_time_diff == -1,
                         select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))
        
series_2 <- subset(results, latency =='1ms' & cbr_packet_size == 200 & start_time_diff == -1,
                  select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_3 <- subset(results, latency =='1ms' & cbr_packet_size == 500 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_4 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

plot_1 <- plot_throughtput(series_1, title = 'CBR packet size = 100')
plot_2 <- plot_throughtput(series_2, title = 'CBR packet size = 200')
plot_3 <- plot_throughtput(series_3, title = 'CBR packet size = 500')
plot_4 <- plot_throughtput(series_4, title = 'CBR packet size = 1000')

plot_1 <- plot_1 + theme(legend.justification = c(1,1), legend.position = c(1,1), legend.title = element_blank())
plot_2 <- plot_2 + theme(legend.justification = c(1,1), legend.position = c(1,1), legend.title = element_blank())
plot_3 <- plot_3 + theme(legend.justification = c(1,1), legend.position = c(1,1), legend.title = element_blank())
plot_4 <- plot_4 + theme(legend.justification = c(1,1), legend.position = c(1,1), legend.title = element_blank())

p <- grid.arrange(plot_1, plot_2, plot_3, plot_4, ncol = 4)
ggsave('throughput.pdf', p, width = 45, height = 8, units = 'cm')


plot_1 <- plot_rtt(series_1, title = 'CBR packet size = 100')
plot_2 <- plot_rtt(series_2, title = 'CBR packet size = 200')
plot_3 <- plot_rtt(series_3, title = 'CBR packet size = 500')
plot_4 <- plot_rtt(series_4, title = 'CBR packet size = 1000')

p <- grid.arrange(plot_1, plot_2, plot_3, plot_4, ncol = 4)
ggsave('rtt_over_packet_size.pdf', p, width = 45, height = 8, units = 'cm')



series_1 <- subset(results, latency =='1ms' & cbr_packet_size == 200 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_2 <- subset(results, latency =='1ms' & cbr_packet_size == 200 & start_time_diff == 0.1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_3 <- subset(results, latency =='1ms' & cbr_packet_size == 200 & start_time_diff == 1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_4 <- subset(results, latency =='1ms' & cbr_packet_size == 200 & start_time_diff == 5,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

plot_1 <- plot_drop_rate(series_1, title = 'CBR starts before TCP: 1s')
plot_2 <- plot_drop_rate(series_2, title = 'CBR starts after TCP: 0.1s')
plot_3 <- plot_drop_rate(series_3, title = 'CBR starts after TCP: 1s')
plot_4 <- plot_drop_rate(series_4, title = 'CBR starts after TCP: 5s')

plot_1 <- plot_1 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())
plot_2 <- plot_2 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())
plot_3 <- plot_3 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())
plot_4 <- plot_4 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())

p <- grid.arrange(plot_1, plot_2, plot_3, plot_4, ncol = 4)
ggsave('drop_rate.pdf', p, width = 45, height = 8, units = 'cm')

series_1 <- subset(results, latency =='1ms' & cbr_packet_size == 1000 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_2 <- subset(results, latency =='10ms' & cbr_packet_size == 1000 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))

series_3 <- subset(results, latency =='100ms' & cbr_packet_size == 1000 & start_time_diff == -1,
                   select=c(TCP, cbr_bandwidth, throughput, drop_rate, rtt))


plot_1 <- plot_rtt(series_1, title = 'link latency = 1ms')
plot_2 <- plot_rtt(series_2, title = 'link latency = 10ms')
plot_3 <- plot_rtt(series_3, title = 'link latency = 100ms')

plot_1 <- plot_1 + theme(legend.position = 'none')
plot_2 <- plot_2 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())
plot_3 <- plot_3 + theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())

p <- grid.arrange(plot_1, plot_2, plot_3, ncol = 3)
ggsave('rtt.pdf', p, width = 33, height = 8, units = 'cm')

