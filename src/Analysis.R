# analyze every trial by the methods from time series analysis
# import some packages
library(data.table)
library(purrr)
library(fUnitRoots)
library(forecast)
library(tsoutliers)
library(ggplot2)
library(ggthemes)
library(magrittr)
library(zoo)

p_bound = 0.05 # p value upper bound to reject the null hypothesis
DATA_PATH="../Data/"

# Part 1: data processing
# read data
read_test = function(idx, prefix = "") {
  net_name = paste(c(prefix, "test", as.character(idx), "_net.csv"), collapse = "")
  video_name = paste(c(prefix, "test", as.character(idx), "_video.csv"), collapse = "")
  net = setDT(read.csv(net_name))
  video = setDT(read.csv(video_name))
  return(list(net, video))
}

# read all data
read_all = function(total, prefix = "") {
  temp = (c(1:total) %>% map(~read_test(., prefix)) %>% c)
  net = temp %>% map(~.[[1]]) %>% c
  video = temp %>% map(~.[[2]]) %>% c
  return(list(net, video))
}

# function to aggregate the network data into 75 points
aggr = function(x, every = 4) {
  # calculate inner loop
  cal_every = function(y) {
    return(data.frame(
        timestamp = y$timestamp[1] %/% every,
        CapNum = sum(y$CapNum),
        CapLen = mean(y$CapLen)
    ))
  }
  temp = as.data.table(x)
  temp[, time := temp$timestamp %/% every]
  return(setDT(temp %>%
            split(temp$time)
             %>% map(cal_every) %>% reduce(rbind.data.frame)))
}

# function to smooth the curve
smooth_frame = function(x, width = 3) {
  f = function(name) {
    temp = data.frame(x[[name]])
    if (name != "timestamp")
      temp = data.frame(ma(x[[name]], width))
    colnames(temp) = name
    return(temp)
  }
  return(setDT(na.omit(names(x) %>% map(f) %>% reduce(cbind.data.frame))))
}

# Part 2: single analysis
# test stationarity - using p-value of Augmented Dickey–Fuller Test
is_stat = function(x) { return(adfTest(x)@test$p.value < p_bound) }

# test white noise - using p-value of Ljung-Box Test
is_white_noise = function(x) {
  return(Box.test(x, type = "Ljung-Box",
          lag = log(length(x) + 1))$p.value > p_bound)
}

# give the type of the time series
net_type = function(x) {
  if(!is_stat(x))
    return('NS')
  if(!is_white_noise(x))
    return('S')
  return('W')
}

# detect outliers for time series x
yield_outliers = function(x) {
  # build ARIMA model by automatic methods
  fit = auto.arima(x)
  # calculate residuals and parameters
  resid = residuals(fit)
  pars = coefs2poly(fit)
  # yields outliers 
  otypes = c("AO", "TC", "LS")
  mo0 = locate.outliers(resid, pars, types = otypes)
  mo1 = locate.outliers.iloop(resid, pars, types = otypes)
  mo2 = locate.outliers.oloop(x, fit, types = otypes)
  return(mo2$outliers$ind)
}

# plot a curve with outliers
plot_with_outliers = function(priv, d, cid = 1) {
  idx = yield_outliers(d)
  temp = data.frame(time = c(1:length(d)), out = d)
  p = priv
  if (is.null(priv)) {
    p = ggplot(temp, aes(time, out))
  }
  p = p + geom_line(data = temp, aes(x = time, y = out), colour = cid)
  temp = data.frame(time = idx, out = d[idx])
  p = p + geom_point(data = temp, aes(x = time, y = out), colour = cid + 1, size = 3)
  return(p)
}

# Part 3: correlation analysis
# all correlation - using kendall method 
cor_all = function(x, y) {
  return(cor(x, y, method = 'kendall'))
}

# test whether x and y are correlated - using kendall method
is_cor = function(x, y) {
  return(cor.test(x, y, method = 'kendall')$p.value < p_bound)
}

# correlation concerning rolling windows
cor_rolling = function(x, y, rolln = 10) {
  temp = data.frame(x, y)
  return(rollapply(temp, width = rolln, function(x) cor_all(x[, 1], x[, 2]), by.column = FALSE))
}

# test whether x and y are correlated concerning rolling windows
is_cor_rolling = function(x, y, rolln = 10, thres=0.75) {
  temp = cor_rolling(x, y, rolln)
  posi = length(temp[temp > 0.2])
  nega = length(temp[temp < -0.2])
  return((posi + nega) / length(temp) > thres)
}

# plot function for histogram
plot_hist=function(x, name, title, bin=8, color="steelblue"){
  temp = data.frame(x)
  p = ggplot(temp, aes(x=x))
  p = p + geom_histogram(
        fill = color, color="black", bins = bin)
  p = p + xlab(name) + ylab("Count") 
  p = p + ggtitle(title)
  p = p + theme_stata()+theme(plot.title = element_text(hjust = 0.5, size=20),
              axis.title.x = element_text(size=14),
              axis.title.y = element_text(size=14),
              axis.text.x = element_text(size=12),
              axis.text.y = element_text(size=12))
  filename = paste(c("../Plots/", title, ".pdf"), collapse="")
  ggsave(filename, p, width=10, height=8)
}

# plot function for scatter
plot_points=function(x, y, namex, namey, title, color="#CC6600"){
  temp = data.frame(x, y)
  p = ggplot(temp, aes(x=x, y=y))
  p = p + geom_point(color=color, alpha=0.7, size=4)
  p = p + xlab(namex) + ylab(namey) 
  p = p + ggtitle(title)
  p = p + theme_stata()+theme(plot.title = element_text(hjust = 0.5, size=20),
              axis.title.x = element_text(size=14),
              axis.title.y = element_text(size=14),
              axis.text.x = element_text(size=12),
              axis.text.y = element_text(size=12))
  filename = paste(c("../Plots/", title, ".pdf"), collapse="")
  ggsave(filename, p, width=10, height=8)
}


# Part 4: complete analysis
sink("../result.txt", split=TRUE)
file_n = 40
tests = read_all(file_n, prefix = DATA_PATH)
tests.net = tests[[1]]
tests.video = tests[[2]]
#print(tests.net)
#print(tests.video)

# Subpart 1 - analyze correlation between caplen and capnum

# analyze all correlation
is_cor_cnt = tests.net %>%
              map(~is_cor(.$CapLen, .$CapNum)) %>% unlist %>% table
print(is_cor_cnt)
cor.all.data.net = (tests.net %>%
                map_dbl(~cor_all(.$CapLen, .$CapNum)))
print(summary(cor.all.data.net))
plot_hist(cor.all.data.net, "Correlations", 
      "Correlations between Packet Average Length and Packet Numbers")
# analyze rolling correlation of smoothed data
tests.net.smoothed = tests.net %>% map(smooth_frame)
cor.roll.data.net = (tests.net.smoothed %>%
              map(~cor_rolling(.$CapLen, .$CapNum)) %>% unlist)
print(summary(cor.roll.data.net))
plot_hist(cor.roll.data.net, "Correlations per 10s",
      "Rolling Correlations between Packet Average Length and Packet Numbers")

# Subpart 2 - analyze the relationship between net and video quality

# aggregate the net data and smooth all data
tests.net.aggr = (tests.net %>% map(aggr))
tests.net.aggr.smoothed = (tests.net.aggr %>% map(smooth_frame))
tests.video.smoothed = (tests.video %>% map(smooth_frame))

# analyze all correlation
# freeze
is_cor_freeze = c(1:length(tests.video)) %>%
                    map(~is_cor(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$freeze)) %>% 
                    unlist
print(is_cor_freeze)
print(table(is_cor_freeze))

cor.all.data.freeze = rep(NA, each = length(tests.video))
cor.all.data.freeze[is_cor_freeze == TRUE] = which(is_cor_freeze == TRUE) %>%
                    map(~cor_all(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$freeze)) %>% 
                    unlist
print(summary(cor.all.data.freeze))
plot_hist(cor.all.data.freeze[is_cor_freeze == TRUE], "Correlations",
      "Correlations between Packet Average Length and Freeze")
is_posi_cor_freeze = which(cor.all.data.freeze > 0.2)
is_neg_cor_freeze = which(cor.all.data.freeze < -0.2)

# noise
is_cor_noise = c(1:length(tests.video)) %>%
                    map(~is_cor(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$noise)) %>% 
                    unlist
print(is_cor_noise)
print(table(is_cor_noise))

cor.all.data.noise = rep(NA, each = length(tests.video))
cor.all.data.noise[is_cor_noise == TRUE] = which(is_cor_noise == TRUE) %>%
                    map(~cor_all(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$noise)) %>% 
                    unlist
print(summary(cor.all.data.noise))
plot_hist(cor.all.data.noise[is_cor_noise == TRUE], "Correlations",
      "Correlations between Packet Average Length and Noise")
is_posi_cor_noise = which(cor.all.data.noise > 0.2)
is_neg_cor_noise = which(cor.all.data.noise < -0.2)

# blur
is_cor_blur = c(1:length(tests.video)) %>%
                    map(~is_cor(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$blur)) %>% 
                    unlist
print(is_cor_blur)
print(table(is_cor_blur))

cor.all.data.blur = rep(NA, each = length(tests.video))
cor.all.data.blur[is_cor_blur == TRUE] = which(is_cor_blur == TRUE) %>%
                    map(~cor_all(tests.net.aggr.smoothed[[.]]$CapLen, tests.video.smoothed[[.]]$blur)) %>% 
                    unlist
print(summary(cor.all.data.blur))
plot_hist(cor.all.data.blur[is_cor_blur == TRUE], "Correlations",
      "Correlations between Packet Average Length and Blur")
is_posi_cor_blur = which(cor.all.data.blur > 0.2)
is_neg_cor_blur = which(cor.all.data.blur < -0.2)

# contingency table analysis
cont.data.freeze = rep('NC', each=length(tests.video))
cont.data.freeze[is_posi_cor_freeze] = 'P'
cont.data.freeze[is_neg_cor_freeze] = 'N'
cont.data.freeze = factor(cont.data.freeze, levels=c("NC", "P", "N"))

cont.data.noise = rep('NC', each=length(tests.video))
cont.data.noise[is_posi_cor_noise] = 'P'
cont.data.noise[is_neg_cor_noise] = 'N'
cont.data.noise = factor(cont.data.noise, levels=c("NC", "P", "N"))

cont.data.blur = rep('NC', each=length(tests.video))
cont.data.blur[is_posi_cor_blur] = 'P'
cont.data.blur[is_neg_cor_blur] = 'N'
cont.data.blur = factor(cont.data.blur, levels=c("NC", "P", "N"))

cont.table = table(cont.data.noise, cont.data.blur, cont.data.freeze)
print(cont.table)

# independency test - using pearson chi^2 test
print(chisq.test(cont.data.noise, cont.data.blur))
print(chisq.test(cont.data.noise, cont.data.freeze))
print(chisq.test(cont.data.blur, cont.data.freeze))
print(chisq.test(table(cont.data.blur[cont.data.freeze=="N"])))
print(chisq.test(cont.data.noise[cont.data.freeze=="NC"], cont.data.blur[cont.data.freeze=="NC"]))

# Subpart 3 - analyze network environment

# test stationarity
tests.net.CapNum.type = tests.net %>% map(~net_type(.$CapNum)) %>% unlist
print(table(tests.net.CapNum.type))
print(which(tests.net.CapNum.type == "S"))

tests.net.CapLen.type = tests.net %>% map(~net_type(.$CapLen)) %>% unlist
print(table(tests.net.CapLen.type))

# test outliers
tests.net.CapNum.outliern = tests.net %>%
                map(~yield_outliers(.$CapNum)) %>% map(length) %>% unlist
print(summary(tests.net.CapNum.outliern))
tests.net.CapLen.outliern = tests.net %>%
                map(~yield_outliers(.$CapLen)) %>% map(length) %>% unlist
print(summary(tests.net.CapLen.outliern))
plot_points(tests.net.CapLen.outliern, tests.net.CapNum.outliern,
      "Number of Outliers in Packet Average Lengths",
      "Number of Outliers in Packet Numbers",
      "Scatters of Two Parameters of Packets")

# discuss the relationship between basic speed and performance
test.env = read.csv(paste(c(DATA_PATH, "fileinfo.csv"), collapse = ""))
test.env$netspeed = test.env$netspeed * 1000/8
tests.net.avg_num = tests.net %>% map(~ .$CapNum) %>% map(mean) %>% unlist
tests.net.avg_speed = tests.net %>% map(~ .$CapLen * .$CapNum/1000) %>% map(mean) %>% unlist
print(cor_all(test.env$netspeed, tests.net.avg_num))
print(cor_all(test.env$netspeed, tests.net.avg_speed))
print(cor_all(test.env$netspeed, tests.net.CapNum.outliern))
plot_points(test.env$netspeed, tests.net.avg_num,
      "Network Speed Baseline/KBps",
      "Average Packet Numbers",
      "Scatters of Packet Numbers and Baseline")
plot_points(test.env$netspeed, tests.net.avg_speed,
      "Network Speed Baseline/KBps",
      "Average Receiving Speed/KBps",
      "Scatters of Receiving Speed and Baseline")
plot_points(test.env$netspeed, tests.net.CapNum.outliern,
      "Network Speed Baseline/KBps",
      "Number of Outliers in Packet Numbers",
      "Scatters of Outlier Numbers of Packet Numbers and Baseline")