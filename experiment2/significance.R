setwd('~/Projects/tcppa/experiment2/')
results1 <- read.csv('significance_1.out', header = FALSE)
results2 <- read.csv('Newreno_vegas.out', header = FALSE)


library(ggplot2)

plot_1 <- ggplot() +
            geom_histogram(data = results1[results1$V1 == 'Reno/Reno',], binwidth = 0.1, aes(x = V2, fill=V1), alpha=I(0.5)) +
            geom_histogram(data = results1[results1$V1 == 'Newreno/Reno',], binwidth = 0.1, aes(x = V2, fill=V1), alpha= I(0.5)) +
            # geom_density(data = results1[results1$V1 == 'Reno/Reno',], aes(x = V2, y = ..scaled.., color=V1)) + 
            # geom_density(data = results2[results2$V1 == 'Newreno/Reno',], aes(x = V2, y = ..scaled.., color=V1)) + 
            xlab('Throughput ratio') + 
            theme(legend.justification = c(1,1), legend.position = c(1,1), legend.title = element_blank())

ggsave('trhoughput_ratio.pdf', plot_1, width = 10, height = 8, units = 'cm')            

print(t.test(results1[results1$V1 == 'Reno/Reno',]$V2, results1[results1$V1 == 'Newreno/Reno',]$V2))

plot_2 <- ggplot() +
  geom_histogram(data = results2[results2$V1 == 'Vegas/Vegas',], binwidth = 0.1, aes(V2, fill=V1), alpha = I(0.5)) +
  geom_histogram(data = results2[results2$V1 == 'Newreno/Vegas',], binwidth = 0.1, aes(V2, fill=V1), alpha = I(0.5)) +
  xlab('throughput ratio (N1 to N4)/(N5 to N6)') + 
  theme(legend.justification = c(0,1), legend.position = c(0,1), legend.title = element_blank())


print(plot_1)
        