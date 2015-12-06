
data = read.table('/tmp/_d_imgs_good.csv', head=T, sep=' ')
summary(data)
class(data)
tapply(data$blht, data$char, summary)
tapply(data$blht, data$font, summary)
rstudio::viewData(data)
tapply(data$top, data$char, summary)
tapply(data$normtop, data$char, summary)
?hist
hist(data$normtop)
hist(data$normbot)
hist(data$normwd)
hist(data$normht)
data[1:10]
data[1,1]
data[1,1,1]
data
data[data$ht < 10]
data$ht
data[[data$ht < 10]]
data[data$ht == 10]
class(data)
type(data)
subset(data, ht == 48)
data[ht == 48]
data[data$ht == 48]
subset(data, ht == 48)
subset(data$char, ht == 48)
subset(data, ht == 48)$char
table(subset(data, ht == 48)$char)
summary(data)
table(subset(data, ht ==1)$char)
subset(data, ht ==1)$char
subset(data, ht ==1)
subset(data, ht<10)
subset(data, ht<8)
subset(data, ht<3)
subset(data, wd<3)
summary(data)
subset(data, normtop>50)
subset(data, normtop<-50)
subset(data, normtop< -50)
table(subset(data, normtop< -50))
summary(subset(data, normtop< -50))
summary(subset(data, normbot>150))
hist(log(data$aspt))
hist((data$aspt))
log(10)
log(10,10)
log10(10)
hist(log2(data$aspt/100))
summary(data$wd)
summary(data$normwd)
summary(data$normwd>162)
summary(subset(data, data$normwd>162))
table(subset(data, data$normwd>162))
man tapply
?tapply
table(subset(data, data$normwd>162), data$char, summary)
class(subset(data, data$normwd>162))
fat_data = subset(data, data$normwd>200)
tapply(fat_data, fat_data$char, summary)
length(fat_data)
savehistory('/tmp/hist.R')
