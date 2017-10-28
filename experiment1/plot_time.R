setwd('~/Projects/tcppa/experiment1/')

series_1 <- read.csv('time/1ms_Newreno_200_1mb_-1_20.csv')
series_2 <- read.csv('time/1ms_Reno_200_1mb_-1_20.csv')
series_3 <- read.csv('time/1ms_TCP_200_1mb_-1_20.csv')
series_4 <- read.csv('time/1ms_Vegas_200_1mb_-1_20.csv')



p <- ggplot() + 
  geom_line(data=series_1[series_1$metric == 'cwnd',], aes(x=time, y=value), color = 'red') +
  geom_line(data=series_2[series_3$metric == 'cwnd',], aes(x=time, y=value), color = 'yellow') +
  geom_line(data=series_3[series_3$metric == 'cwnd',], aes(x=time, y=value), color = 'green') +
  geom_line(data=series_4[series_4$metric == 'cwnd',], aes(x=time, y=value), color = 'blue')
  
print(p)