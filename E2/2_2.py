import matplotlib.pyplot as mplt, numpy, pylab


filehandle = open('applesOranges.csv')
filelines = filehandle.readlines()[1:]
dataread = numpy.array([[float(entry[0]),float(entry[1]),int(entry[2])] for entry in [line.strip().split(",") for line in filelines]])
data = dataread[:,:-1].T
classifications = dataread[:,-1:][:,0]
#print "data", data.shape, "\n", data
#print "classifications", classifications.shape, "\n", classifications
#print "classifications ones", (classifications==1).shape, "\n", (classifications==1)
#print "data ones", data[:,classifications==1].shape, "\n", data[:,classifications==1]
#print "data zeros", data[:,classifications==0].shape, "\n", data[:,classifications==0]


#a
#(a) Plot the data in a scatter plot (x.1 vs. x.2). Use color to indicate the type of each object.
mplt.scatter( data[:,classifications==0][0], data[:,classifications==0][1], color='goldenrod' )
mplt.scatter( data[:,classifications==1][0], data[:,classifications==1][1], color='deepskyblue' )
pylab.savefig('2_2_a.png', bbox_inches='tight')
#print data[:,classifications==0][0]

#b
#(b) Set theta = 0. 
#Create a set of 19 equally spaced weight vectors w = [w1,w2] on the circle centered on (0, 0) with radius 1. I.e. if a denotes the angle between the weight vector and the x-asis, for each weight ||w|| = 1 and a1 = 0,a2 = 10,...,a19 = 180 such that w1 member [-1, 1], w2 member [0, 1]. 
degreeangles = numpy.array(range(0, 181, 10))
weights = numpy.array([[numpy.cos(degreeangle*numpy.pi/180.0), numpy.sin(degreeangle*numpy.pi/180.0)] for degreeangle in degreeangles]).T
#print "weights", weights.shape, "\n", weights
mplt.scatter( weights[0], weights[1], color='hotpink' )
pylab.savefig('2_2_ab.png', bbox_inches='tight')
mplt.clf()



#For each weight vector w determine the classification performance p (% correct classifications) of the corresponding neuron and 
#make a matrix number_of_weights x number_of_datapoints where each entry has the desired sign (data comes as 0 and 1 so subtract .5 to get + and -)
#this is the same row repeated number_of_weights times
#bxa . axc = bxc
#19x200 = 19xa . ax200
#classifications = 1x200
classificationsigns = (numpy.dot(numpy.ones((19,1)), classifications.reshape((1,len(classifications))))-.5)
#print "classificationsigns", classificationsigns.shape, "\n", classificationsigns


#make a matrix of classifications, then sum all datapoints for each weight, (and then divide by number_of_datapoints)
wtx = numpy.dot(weights.T, data)
#print "wtx", wtx.shape, "\n", wtx
#classifiedcorrectly = (numpy.sign(wtx)==numpy.sign(classificationsigns))
#print "classifiedcorrectly", classifiedcorrectly.shape, "\n", classifiedcorrectly
classificationperformances = numpy.sum((numpy.sign(wtx)==numpy.sign(classificationsigns))>0, axis=1)/200.0
#print "classificationperformances", classificationperformances.shape, "\n", classificationperformances


#plot a curve showing a vs. p.
mplt.plot(degreeangles, classificationperformances)
pylab.savefig('2_2_b.png', bbox_inches='tight')
mplt.clf()





#c
#(c) From these weights, pick the weight vector yielding best performance.
bestweight = 0
for weightnumber in range(len(classificationperformances)):
   if classificationperformances[bestweight] < classificationperformances[weightnumber]:
      bestweight = weightnumber
print "weights[bestweight] =",weights[:,bestweight],"value =",classificationperformances[bestweight]
#print "wtx", wtx[bestweight].shape, "\n", wtx[bestweight]

#Now vary theta member [-3,3] and pick the value of theta giving the best performance.
#create all the thresholds
maxpositivethreshold = 3.0
maxnegativethreshold = -3.0
numberofsamplethresholds = 999
thresholds = numpy.linspace(maxnegativethreshold, maxpositivethreshold, numberofsamplethresholds)
#print thresholds

#find the best threshold
bestthreshold = 0
mostclassifiedcorrectly = 0
for threshold in thresholds:
   numberclassifiedcorrectly = numpy.sum((numpy.sign(wtx[bestweight] + threshold)==numpy.sign(classifications-.5))>0)
   #print "wtx[bestweight] +", threshold, " (correct:", numberclassifiedcorrectly, ")\n", #wtx[bestweight] + threshold
   if numberclassifiedcorrectly > mostclassifiedcorrectly:
      bestthreshold = threshold
      mostclassifiedcorrectly = numberclassifiedcorrectly

#print "bestthreshold",bestthreshold,"mostcorrect:",mostclassifiedcorrectly


#d
#(d) Plot the datapoints, colored according to the classification corresponding to these parameter values. Plot the weight vector w in the same plot. 
#with the best weight and best threshold, find which entries are correctly classified and which not
bestclassifieds = (numpy.sign(wtx[bestweight] + bestthreshold) == numpy.sign(classifications-.5))
#print "bestclassifieds", bestclassifieds.shape, "\n", bestclassifieds
#print "data[:,bestclassifieds==False]", data[:,bestclassifieds==False].shape, "\n", data[:,bestclassifieds==False]

mplt.scatter( data[:,bestclassifieds==False][0], data[:,bestclassifieds==False][1], color='goldenrod' )
mplt.scatter( data[:,bestclassifieds==True][0], data[:,bestclassifieds==True][1], color='deepskyblue' )
#print "weights", weights.shape, "\n", weights
mplt.scatter( weights[0,bestweight], weights[1,bestweight], color='hotpink' )
pylab.savefig('2_2_d.png', bbox_inches='tight')


#How do you interpret your results?


#(e) Find the best combination of w and theta by exploring all combinations of a and theta.
