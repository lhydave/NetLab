# analyze every trial by the methods from time series analysis
# import some packages
library(data.table)
library(purrr)
library(fUnitRoots)
library(forecast)
library(tsoutliers)
library(ggplot2)
library(magrittr)
library(zoo)

p_bound = 0.05 # p value upper bound to reject the null hypothesis

# Part 1: data processing     
# read data
#TODO: read all data
read_test = function(idx, prefix = "") {
  net_name = paste(c(prefix, "test", as.character(idx), "_net.csv"), collapse = "")
  video_name = paste(c(prefix, "test", as.character(idx), "_video.csv"), collapse = "")
  net = setDT(read.csv(net_name))
  video = setDT(read.csv(video_name))
  return(list(net, video))
}

test = read_test(1)
test.net = test[[1]]
test.video = test[[2]]

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
smooth_frame = function(x, width = 5) {
  f = function(name) {
    temp = data.frame(x[[name]])
    if (name != "timestamp")
      temp = data.frame(ma(x[[name]], width))
    colnames(temp) = name
    return(temp)
  }
  return(setDT(na.omit(names(x) %>% map(f) %>% reduce(cbind.data.frame))))
}
aggr_net = aggr(test.net)
aggr_smooth_net = smooth_frame(aggr_net)
test.video = smooth_frame(test.video)
#matplot(c(0:74), cbind(aggr_net$CapLen, aggr_smooth_net$CapLen), type = "l", lty = 1, lwd = 2, col = c("red", "blue"))

# Part 2: single analysis
# test stationarity - using p-value of Augmented Dickey–Fuller Test
adf_p = function(x) { return(adfTest(x)@test$p.value) }

# test white noise - using p-value of Ljung-Box Test
LBox_p = function(x) { return(Box.test(x, type = "Ljung-Box")$p.value) }

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

#print(plot_with_outliers(plot_with_outliers(NULL, aggr_net$CapLen / 5), test.video$freeze, 3))

# Part 3: correlation analysis
# all pearson correlation
pearson_all = function(x, y) {
  return(cor(x, y))
}
#print(pearson_all(aggr_smooth_net$CapLen, test.video$blur))
print(pearson_all(test.video$freeze, test.video$blur))

# pearson correlation concerning rolling windows
pearson_rolling = function(x, y, rolln = 20) {
  temp = data.frame(x, y)
  return(rollapply(temp, width = rolln, function(x) cor(x[, 1], x[, 2]), by.column = FALSE))
}

#plot(pearson_rolling(aggr_smooth_net$CapLen, test.video$freeze), type = "l")
#matplot(c(1:length(aggr_smooth_net$CapNum)), 
#cbind(pearson_rolling(aggr_smooth_net$CapLen, aggr_smooth_net$CapNum), 
#aggr_smooth_net$CapNum / 500),
#type = "l", col = c("blue", "red"), lty = 1, lwd = 2)
