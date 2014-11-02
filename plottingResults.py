import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab as bp

def getData(segmentNumber):
	lines=[line.strip() for line in open("./Plotting/SegmentAnalysis/SpeedInfo/speedsOfSegment"+str(segmentNumber)+".txt")]
	mylines=[]
	for i in lines:
		mylines.append(float(i))
	return mylines

for i in range(65):
	segmentNumber=i+1
	data=getData(segmentNumber)
	x=np.array(data)
	mu = x.mean()
	median = np.median(x)
	sigma = x.std()

	fig=plt.figure()
	fig.suptitle('Speed Distribution in Segment'+str(segmentNumber),fontsize=14,fontweight='bold')
	ax = fig.add_subplot(111)
	textstr = '$\mu=%.2f$\n$\mathrm{median}=%.2f$\n$\sigma=%.2f$'%(mu, median, sigma)
	props = dict(boxstyle='round', facecolor='white', alpha=0.5)
	ax.text(0.97, 0.97, textstr, transform=ax.transAxes, fontsize=14,
	        verticalalignment='top',horizontalalignment='right',bbox=props)
	ax.set_xlabel('Speed_In_Km/hr')
	ax.set_ylabel('Number_Of_Vehicles')
	num_bins = 50
	n, bins, patches = plt.hist(x, num_bins,histtype='bar',facecolor='c',rwidth=01)
	plt.axvline(x.mean(), color='g', linestyle='dashed', linewidth=2,label= 'mean')
	limits = ax.axis()
	print limits[3]
	plt.plot((median,median),(0,limits[3]),'r',linestyle='dashed',linewidth=2,label='median')
	legend = ax.legend(loc='upper left')
	bp.savefig('./Plotting/SegmentAnalysis/SpeedPlots/Speed_Distribution_Segment'+str(segmentNumber), bbox_inches='tight')
# fig = plt.figure()
# fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')

# ax = fig.add_subplot(111)
# fig.subplots_adjust(top=0.85)
# ax.set_title('axes title')

# ax.set_xlabel('xlabel')
# ax.set_ylabel('ylabel')



# ax.text(2, 6, r'an equation: $E=mc^2$', fontsize=15)

# ax.text(3, 2, unicode('unicode: Institut f\374r Festk\366rperphysik', 'latin-1'))

# ax.text(0.95, 0.01, 'colored text in axes coords',
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax.transAxes,
#         color='green', fontsize=15)


# ax.plot([2], [1], 'o')
# ax.annotate('annotate', xy=(2, 1), xytext=(3, 4),
#             arrowprops=dict(facecolor='black', shrink=0.05))

# ax.axis([0, 10, 0, 10])

# plt.show()
# mu, sigma = 200, 25
# x = mu + sigma*P.randn(10000)

# # the histogram of the data with histtype='step'
# n, bins, patches = P.hist(x, 50, normed=1, histtype='stepfilled')
# P.setp(patches, 'facecolor', 'g', 'alpha', 0.75)

# # add a line showing the expected distribution
# y = P.normpdf( bins, mu, sigma)
# l = P.plot(bins, y, 'k--', linewidth=1.5)


# # create a histogram by providing the bin edges (unequally spaced)

# P.figure()

# bins = [100,125,150,160,170,180,190,200,210,220,230,240,250,275,300]
# # the histogram of the data with histtype='step'
# n, bins, patches = P.hist(x, bins, normed=1, histtype='bar', rwidth=0.8)

# #
# # now we create a cumulative histogram of the data
# #
# P.figure()
# P.show()

# n, bins, patches = P.hist(x, 50, normed=1, histtype='step', cumulative=True)

# # add a line showing the expected distribution
# y = P.normpdf( bins, mu, sigma).cumsum()
# y /= y[-1]
# l = P.plot(bins, y, 'k--', linewidth=1.5)

# # create a second data-set with a smaller standard deviation
# sigma2 = 15.
# x = mu + sigma2*P.randn(10000)

# n, bins, patches = P.hist(x, bins=bins, normed=1, histtype='step', cumulative=True)

# # add a line showing the expected distribution
# y = P.normpdf( bins, mu, sigma2).cumsum()
# y /= y[-1]
# l = P.plot(bins, y, 'r--', linewidth=1.5)

# # finally overplot a reverted cumulative histogram
# n, bins, patches = P.hist(x, bins=bins, normed=1,
#     histtype='step', cumulative=-1)


# P.grid(True)
# P.ylim(0, 1.05)


# #
# # histogram has the ability to plot multiple data in parallel ...
# # Note the new color kwarg, used to override the default, which
# # uses the line color cycle.
# #
# P.figure()

# # create a new data-set
# x = mu + sigma*P.randn(1000,3)

# n, bins, patches = P.hist(x, 10, normed=1, histtype='bar',
#                             color=['crimson', 'burlywood', 'chartreuse'],
#                             label=['Crimson', 'Burlywood', 'Chartreuse'])
# P.legend()

# #
# # ... or we can stack the data
# #
# P.figure()

# n, bins, patches = P.hist(x, 10, normed=1, histtype='bar', stacked=True)

# P.show()

# #
# # we can also stack using the step histtype
# #

# P.figure()

# n, bins, patches = P.hist(x, 10, histtype='step', stacked=True, fill=True)

# P.show()

# #
# # finally: make a multiple-histogram of data-sets with different length
# #
# x0 = mu + sigma*P.randn(10000)
# x1 = mu + sigma*P.randn(7000)
# x2 = mu + sigma*P.randn(3000)

# # and exercise the weights option by arbitrarily giving the first half
# # of each series only half the weight of the others:

# w0 = np.ones_like(x0)
# w0[:len(x0)/2] = 0.5
# w1 = np.ones_like(x1)
# w1[:len(x1)/2] = 0.5
# w2 = np.ones_like(x2)
# w2[:len(x2)/2] = 0.5



# P.figure()

# n, bins, patches = P.hist( [x0,x1,x2], 10, weights=[w0, w1, w2], histtype='bar')

# P.show()







