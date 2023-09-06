import tables as t, pylab as py, pandas as pd, os, queue as Queue
import sys

#Three arguments :
# sys.argv[1] = albedo true false
# sys.argv[2] = channel
# sys.argv[3] = number of fill


print ("Albedo correction applied: " + sys.argv[1])
print ("Channel: " , str(sys.argv[2]))

def string_to_boolean(s):
    # Define the criteria for converting the string to a boolean
    true_values = ['true', 'yes', 'on', 'enabled']
    false_values = ['false', 'no', 'off', 'disabled']

    # Convert the string to a boolean
    lowercase_s = s.lower()
    if lowercase_s in true_values:
        return True
    elif lowercase_s in false_values:
        return False
    else:
        raise ValueError(f"Cannot convert '{s}' to boolean.")


# This script takes data from the bcm1fagghist in the central hdf5 file,
# calculates the luminosity table and saves it in a separate hdf5. All parameters
# needed for the luminosity calculation can be changed.

# note to self: when reprocessing remember to CHANGE:
# - c1 to correspond with the sigvis that was used at the time of the fill
# - do_albedo_correction
# - output_path if using new channel mask
# - channel_mask if want to use new channel mask
# - the correct albedo model if using new channel mask

# --- PARAMETER ------------------
output_path = './'
#output_path = '/localdata/lfreitag/newChannels/'

outtablename = 'bcm1flumi'

# output data compression anc chunk size, normally not needed to be changed
compr_filter = t.Filters(complevel=9, complib='blosc')
chunkshape=(100,)

# process this fill
fill = int(sys.argv[3]) #7921 #8094 #7921

# lumi parameters
# channel mask counting from 1 (BRILDAQ channelid selection)
#channel_mask = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
channel_mask = [sys.argv[2]] #channel by channel analysis
# ^ original channel mask: excluded_channels_lumi 28,29,30,31,42,43
#channel_mask = [1,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,45,46,47,48]
# ^ new channel mask: new excluded channels 1,9,10,42,43

# lumi calibration, parameters as in normtag
c0 = 0          #offset
c1 = 11245/139 #/141,139   #linear term, usually 11246/sigma_vis
c2 = 0    #quadratic term to correct non-linearity
calibtag = 'TestBeam'

# Use parameter to subtract a constant noise level. This value is subtracted
# from the bxraw before the albedo correction.
avg_noise = 0 

# Albedo correction parameters
do_albedo_correction = string_to_boolean(sys.argv[1])
#str_channel_mask = str(channel_mask)
output_path = "new_albedo_"+ str(do_albedo_correction)+"_"+str(sys.argv[2]+"_")

# from 8701 2nd value HAS TO BE MODIFIED according to different channel missbehaviour 
# first_correction is an array containing channel customed first albedo corrections, 
# which are based on the analysis of fill 8701 (just ch 6 correction comes from fill 8675) 

channel_num = int(sys.argv[2])
if channel_num == 2 :
    first_correction = 0.10834692062731785
if channel_num == 6 :
    first_correction = 0.24671136952642514
elif channel_num == 9:
    first_correction = 0.06492323164987537
elif channel_num == 10:
    first_correction = 0.10515381368617652
elif channel_num == 11 :
    first_correction = 0.260303400066638
elif channel_num == 12:
    first_correction = 0.11297563114506419
elif channel_num == 13:
    first_correction = 0.0825735458894123
elif channel_num == 14:
    first_correction = 0.05640158349243794
elif channel_num == 23:
    first_correction = 0.09634750993933007
elif channel_num == 24:
    first_correction = 0.09938661844570812
elif channel_num == 25:
    first_correction = 0.234688212715379
elif channel_num == 26:
    first_correction = 0.05615333225796654
elif channel_num == 35:
    first_correction = 0.22172015989378163
elif channel_num == 36:
    first_correction = 0.04160777421079521
elif channel_num == 41:
    first_correction = 0.11494766737424068
elif channel_num == 42:
    first_correction = 0.06302585120671096
elif channel_num == 43:
    first_correction = 0.10627944874471304
elif channel_num == 45:
    first_correction = 0.08553508072374447
elif channel_num == 47:
    first_correction = 0.04786022438847107
elif channel_num == 48:
    first_correction = 0.11045565377131461
else:
    first_correction = 0.022410375592529844
    
albedo_model = [1.0, first_correction, 0.0023920368925298427, 0.0007854522325298428, 0.00030464839252984286]



calculate_albedo_every = 7 # in 4 nibbles (~1.4s), BRILDAQ processor it's 10 seconds
albedo_queue_length = 150 # number of histograms, in BRILDAQ processor it's 150
#noise calculation window, in units of BX (only active with albedo correction)
noise_calc_start = 3480  # BRILDAQ processor uses: 3480
noise_calc_end = 3530  # BRILDAQ processor uses: 3530



# --- START SCRIPT ----------------
if fill<5633:
	raise ValueError('Fill number too small, this script only works with 2017 and 2018 data')
elif fill<6540:
	year = 17
elif fill<7920:
	year = 18
else :
    year = 23

class Lumitable(t.IsDescription):
	fillnum = t.UInt32Col(shape=(), dflt=0, pos=0)
	runnum = t.UInt32Col(shape=(), dflt=0, pos=1)
	lsnum = t.UInt32Col(shape=(), dflt=0, pos=2)
	nbnum = t.UInt32Col(shape=(), dflt=0, pos=3)
	timestampsec = t.UInt32Col(shape=(), dflt=0, pos=4)
	timestampmsec = t.UInt32Col(shape=(), dflt=0, pos=5)
	totsize = t.UInt32Col(shape=(), dflt=0, pos=6)
	publishnnb = t.UInt8Col(shape=(), dflt=0, pos=7)
	datasourceid = t.UInt8Col(shape=(), dflt=0, pos=8)
	algoid = t.UInt8Col(shape=(), dflt=0, pos=9)
	channelid = t.UInt8Col(shape=(), dflt=0, pos=10)
	payloadtype = t.UInt8Col(shape=(), dflt=0, pos=11)
	calibtag = t.StringCol(itemsize=32, shape=(), dflt='', pos=12)
	avgraw = t.Float32Col(shape=(), dflt=0.0, pos=13)
	avg = t.Float32Col(shape=(), dflt=0.0, pos=14)
	bxraw = t.Float32Col(shape=(3564,), dflt=0.0, pos=15)
	bx = t.Float32Col(shape=(3564,), dflt=0.0, pos=16)
	maskhigh = t.UInt32Col(shape=(), dflt=0, pos=17)
	masklow = t.UInt32Col(shape=(), dflt=0, pos=18)

albedo_model_full = py.zeros(3564)
albedo_model_full[1:len(albedo_model)] += albedo_model[1:]

output_path += str(year)
if not os.path.exists(output_path):
	os.makedirs(output_path)
output_path += '/'+str(fill)+'/'
if not os.path.exists(output_path):
	os.makedirs(output_path)

input_path = '/brildata/23/'+str(fill)+'/'
files = os.listdir(input_path)


# create data query condition
query = ''.join(['(channelid == '+str(ch)+ ') | ' for ch in channel_mask])
query = '('+query[:-3]+') & (algoid == 1)' # in 2017 some data was saved under algoid==2

# get bunch mask from last file (likely the one with collisions)
h5 = t.open_file(input_path+files[-1],mode='r')
bxmask = h5.root.beam[0]['collidable']
h5.close()

#prepare albedo queue
albedo_queue = Queue.Queue()
calc_counter = 0
albedo_fraction = py.ones(3564)
noise = 0

for file in files:
	print("============================================",file)
	#input file
	h5in = t.open_file(input_path+file,mode='r')
	intable = h5in.root.bcm1fagghist

	#output file
	h5out = t.open_file(output_path+file,mode='w')
	outtable = h5out.create_table('/',outtablename,Lumitable,filters=compr_filter,chunkshape=chunkshape)
	rownew = outtable.row


	lastnb = -1
	table_len = len(list(intable.where(query))) #if size ok for memory to make into list?
	for i, rowin in enumerate(intable.where(query)):
		#if file == '8088_356718_2208032336_2208040054.hd5': print(lastnb,rowin['nbnum'])
		if lastnb == -1:
			lastrun = rowin['runnum']
			lastls = rowin['lsnum']
			lastnb = rowin['nbnum']
			lasttime = rowin['timestampsec']
			lasttimems = rowin['timestampmsec']
			chcount = 0
			agghist = py.zeros(3564)

		if lastnb != rowin['nbnum'] or i == table_len-1:
			# process lumi now
			r0 = 1-(agghist/chcount/2**14)
			r0[r0<0] = 0
			bxraw = -py.log(r0)

#			albedo correction every histogram
			#for i,m in enumerate(bxmask):
			#	if m:
			#		bxraw -= bxraw[i]*py.roll(albedo_model_full,i)
			#bxraw -= bxraw[noise_calc_start:noise_calc_end].mean()

#			bxraw -= avg_noise

#			bxraw -= bxraw[noise_calc_start:noise_calc_end].mean()

			# albedo correction
			if do_albedo_correction:
				# put data in albedo queue
				albedo_queue.put(bxraw)
				calc_counter +=1
				if calc_counter>calculate_albedo_every:
					calc_counter = 0
					# average everything in albedo queue
					uncorrected = py.zeros(3564)
					queuesize = albedo_queue.qsize()
					for i in range(queuesize):
						tmp = albedo_queue.get()
						uncorrected +=tmp
						if albedo_queue.qsize() < albedo_queue_length:
							albedo_queue.put(tmp)
					uncorrected/=queuesize
					# calculate albedo
					corrected = uncorrected.copy()
					for i,m in enumerate(bxmask):
						if m:
							corrected -= corrected[i]*py.roll(albedo_model_full,i)

					# make fractions
					albedo_fraction[uncorrected!=0] = corrected[uncorrected!=0]/uncorrected[uncorrected!=0]

					# noise to subtract
					noise = corrected[noise_calc_start:noise_calc_end].mean()

				bxraw = bxraw*albedo_fraction - noise




			# calibrate and sum up for total
			bx = c1*bxraw + c2*bxraw**2 +c0
			avgraw = (bxmask * bxraw).sum() # needs channel mask
			avg = (bxmask * bx).sum() # needs channel mask

			#write out data
			rownew['fillnum'] = fill
			rownew['runnum'] = lastrun
			rownew['lsnum'] = lastls
			rownew['nbnum'] = lastnb
			rownew['timestampsec'] = lasttime
			rownew['timestampmsec'] = lasttimems
			rownew['totsize'] =  28596 # probably wrong, but does anyone care?
			rownew['publishnnb'] =  4
			rownew['datasourceid'] = 14 # I think...
			rownew['algoid'] = 0 # I think...
			rownew['channelid'] = 0
			rownew['payloadtype'] = 11 # no idea why, or if correct
			rownew['calibtag'] = calibtag
			rownew['avgraw'] = avgraw
			rownew['avg'] = avg
			rownew['bxraw'] = bxraw
			rownew['bx'] = bx
			rownew['maskhigh'] = 0 # need to create this from channel mask
			rownew['masklow'] = 0 # need to create this from channel mask
			rownew.append()

			#reinitialize
			lastrun = rowin['runnum']
			lastls = rowin['lsnum']
			lastnb = rowin['nbnum']
			lasttime = rowin['timestampsec']
			lasttimems = rowin['timestampmsec']
			chcount = 0
			agghist = py.zeros(3564)
			#if file == '8088_356718_2208032336_2208040054.hd5': print("===",lastls,lastnb, rowin['nbnum'])

			if lastls % 100 ==0: print(lastrun, lastls)

		#sum the agg hist and count the channels
		chcount += 1
		agghist += rowin['data']
		
	

	outtable.flush()
	h5in.close()
	h5out.close()
	
