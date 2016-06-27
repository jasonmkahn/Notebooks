import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import random
class importation():
	""" The instance gives you access to .exp, which is
	a dictionary of the experiments, keyed on number (int).
	More importantly, it also gives .expcomp, which is a compilation
	(i.e. a list) of the experiment pairs - so 1 + 2 concatenated,
	3 + 4 concatenated, etc. Currently, you also get scatter_panel,
	the function I wrote to automate pyplot scatter plots for
	this dataset.
	
	Takes no arguments at the moment."""

	def __init__(self):
		self.exp = {}
		
		# We'll change each of these to numeric columns in a moment
		
		self.obcolumns = ['onset_dur',
						  'log_onset_dur',
						  'the_dur',
						  'log_the_dur',
						  'object_dur',
						  'log_object_dur',
						  'action_dur',
						  'log_action_dur'
						 ]
		
		# This will add a row to each dataset keyed to the experimental
		# condition. This is so the points in the scatter plots can be
		# represented in the RGB format that plt.scatter expects
		
		self.colordict = {'control' : 'b',
						  'identical' : 'r',
						  'related' : 'g',
						  'unrelated' : 'y'
						 }
		
		
		# This cycles through and prepares each experiment for inclusion
		# in the compilation, storing the finished experiment in self.exp
		# I toggled the output off, but it can be turned on to error-check.
		
		for x in range(1,9):
			os.chdir("G:\Praat_data\Exp%d" % x)
			#print(os.getcwd())
			file = open("dissexp%dr.txt" % x)
			pants = pd.read_table(file)
			try:
				pants['subject'] = pants['subject ']
				del(pants['subject '])
			except KeyError:
				print("This one was fine, boss")
			#Keep only the responses that were acceptable
			pants = pants[pants['exclude'] == 0]
			pants[self.obcolumns] = pants[self.obcolumns].apply(pd.to_numeric,errors = 'coerce')
			if x in [1,3,5,7]:
				pants.soa = -pants.soa
				#print("SOAs reversed for prime before target experiment %d", x)
			# This moves the x coordinate for SOA plotting a little bit, to make
			# the clusters easier to visualize
			pants['soa_jitter'] = pants.apply(lambda y : y.soa + np.random.randint(1,150),axis = 1)
			#print("Jitter applied")
			pants['condition_color'] = pants.apply(lambda z : self.colordict[z.condition],axis = 1)
			#print("Conditions RGB'd")
			#pants.columns
			#pants.dtypes
			self.exp[x] = pants
			#print(self.exp.keys())
			file.close()
		self.exp1 = pd.concat([self.exp[1],self.exp[2]])
		self.exp2 = pd.concat([self.exp[3],self.exp[4]])
		self.exp3 = pd.concat([self.exp[5],self.exp[6]])
		self.exp4 = pd.concat([self.exp[7],self.exp[8]])
		self.exp_neg = [self.exp[1],self.exp[3],self.exp[5],self.exp[7]]
		self.exp_pos = [self.exp[2],self.exp[4],self.exp[6],self.exp[8]]
		self.expcomp = [self.exp1, self.exp2, self.exp3, self.exp4]
		#print("Returning a list of concatenated experiments")
		
		# Finally, a collection of pyplot-friendly objects to feed
		# into the legend later
		red_patch = mpatches.Patch(color = 'red', label = "Identical", alpha = .5)
		yellow_patch = mpatches.Patch(color = 'yellow', label = "Unrelated", alpha = .5)
		blue_patch = mpatches.Patch(color = 'blue', label = 'Control', alpha = .5)
		green_patch = mpatches.Patch(color = 'green', label = 'Related', alpha = .5)
		self.patches = [red_patch, blue_patch, yellow_patch, green_patch]
	
	def scatter_panel(self, x, y, color = None, title = "Default Title", ylab = None, xlab = None):
		"""This produces a 2x2 panel-style graph of the various experiments
		in the dissertation, broken down by thematic pairs (i.e. 1+2)
		
		Args:
			x (str)
			y (str)
			color (str)
			title (Optional[str])
			xlab (Optional[str])
			ylab (Optional[str])"""
	# Takes two column names as strings and graphs all four experiment pairs' data for them
		self.f, self.ax = plt.subplots(2,2, sharex = True, sharey = True, figsize = (12,8))
		self.f.suptitle(title, fontsize = 20)
		self.ax[0,0].scatter(self.expcomp[0][x], self.expcomp[0][y], c = self.expcomp[0][color], alpha = .5)
		self.ax[0,0].set_title("Experiments 1 & 2", fontsize = 16)
		self.ax[0,0].set_ylabel(ylab, fontsize = 16)
		self.ax[0,0].tick_params(labelsize = 12)
		self.ax[0,1].scatter(self.expcomp[1][x], self.expcomp[1][y], c = self.expcomp[1][color], alpha = .5)
		self.ax[0,1].set_title("Experiments 3 & 4", fontsize = 16)
		self.ax[1,0].scatter(self.expcomp[2][x], self.expcomp[2][y], c = self.expcomp[2][color], alpha = .5)
		self.ax[1,0].set_ylabel(ylab, fontsize = 16)
		self.ax[1,0].set_xlabel(xlab, fontsize = 16)
		self.ax[1,0].tick_params(labelsize = 12)
		self.ax[1,0].set_title("Experiments 5 & 6", fontsize = 16)
		self.ax[1,1].scatter(self.expcomp[3][x], self.expcomp[3][y], c = self.expcomp[3][color], alpha = .5)
		self.ax[1,1].set_xlabel(xlab, fontsize = 16)
		self.ax[1,1].set_title("Experiments 7 & 8", fontsize = 16)
		self.ax[1,1].tick_params(labelsize = 12)
		plt.legend(bbox_to_anchor=(1, 1),
		   bbox_transform=plt.gcf().transFigure,
		   handles = self.patches)
		plt.show()

	def scatter_panel_soa(self, x, y, color = None, title = "Default Title", ylab = None, xlab = None):
		"""This produces a 4x2 panel-style graph of the various experiments
		in the dissertation, broken down by positive/negative SOA
		
		Args:
			x (str)
			y (str)
			color (str)
			title (Optional[str])
			xlab (Optional[str])
			ylab (Optional[str])"""
		def plotter(x,y,axis):
			m, b = np.polyfit(x,y,1)
			axis.plot(x,m*x + b, '-', color = 'r')
		self.f, self.ax = plt.subplots(2,4, sharex = True, sharey = True, figsize = (12,8))
		self.f.suptitle(title, fontsize = 20)
		self.ax[0,0].scatter(self.exp_neg[0][x], self.exp_neg[0][y], alpha = .5)
		plotter(self.exp_neg[0][x],self.exp_neg[0][y],self.ax[0,0])
		self.ax[0,0].set_title("Experiment 1 (Negative SOAs)", fontsize = 10)
		self.ax[0,0].set_ylabel(ylab, fontsize = 12)
		self.ax[0,0].tick_params(labelsize = 10)
		self.ax[0,1].scatter(self.exp_neg[1][x], self.exp_neg[1][y], alpha = .5)
		plotter(self.exp_neg[1][x],self.exp_neg[1][y],self.ax[0,1])
		self.ax[0,1].set_title("Experiment 3 (Negative SOAs)", fontsize = 10)
		self.ax[1,0].scatter(self.exp_neg[2][x], self.exp_neg[2][y], alpha = .5)
		plotter(self.exp_neg[2][x],self.exp_neg[2][y],self.ax[1,0])
		self.ax[1,0].set_title("Experiment 5 (Negative SOAs)", fontsize = 10)
		self.ax[1,0].set_ylabel(ylab, fontsize = 12)
		plt.sca(self.ax[1,0])
		plt.xticks([1,50,100],[1,50,100], rotation = 'vertical')
		self.ax[1,0].set_xlabel(xlab, fontsize = 12)
		self.ax[1,0].tick_params(labelsize = 10)
		self.ax[1,1].scatter(self.exp_neg[3][x], self.exp_neg[3][y], alpha = .5)
		plotter(self.exp_neg[3][x],self.exp_neg[3][y],self.ax[1,1])
		self.ax[1,1].set_title("Experiment 7 (Negative SOAs)", fontsize = 10)
		plt.sca(self.ax[1,1])
		plt.xticks(rotation = 'vertical')
		self.ax[1,1].set_xlabel(xlab, fontsize = 12)
		self.ax[1,1].tick_params(labelsize = 10)
		self.ax[0,2].scatter(self.exp_pos[0][x], self.exp_pos[0][y], alpha = .5)
		plotter(self.exp_pos[0][x],self.exp_pos[0][y],self.ax[0,2])
		self.ax[0,2].set_title("Experiment 2 (Positive SOAs)", fontsize = 10)
		self.ax[0,3].scatter(self.exp_pos[1][x], self.exp_pos[1][y], alpha = .5)
		plotter(self.exp_pos[1][x],self.exp_pos[1][y],self.ax[0,3])
		self.ax[0,3].set_title("Experiment 4 (Positive SOAs)", fontsize = 10)
		self.ax[1,2].scatter(self.exp_pos[2][x], self.exp_pos[2][y], alpha = .5)
		plotter(self.exp_pos[2][x],self.exp_pos[2][y],self.ax[1,2])
		self.ax[1,2].set_title("Experiment 6 (Positive SOAs)", fontsize = 10)
		plt.sca(self.ax[1,2])
		plt.xticks(rotation = 'vertical')
		self.ax[1,2].set_xlabel(xlab, fontsize = 12)
		self.ax[1,2].tick_params(labelsize = 10)
		self.ax[1,3].scatter(self.exp_pos[3][x], self.exp_pos[3][y], alpha = .5)
		plotter(self.exp_pos[3][x],self.exp_pos[3][y],self.ax[1,3])
		self.ax[1,3].set_title("Experiment 8 (Positive SOAs)", fontsize = 10)
		plt.sca(self.ax[1,3])
		plt.xticks(rotation = 'vertical')
		self.ax[1,3].set_xlabel(xlab, fontsize = 12)
		self.ax[1,3].tick_params(labelsize = 10)
		plt.show()
		
	def participant_line(self, expnum, pnum, xcolumn, ycolumn):
		"""This takes an experiment number (1-8), participant number (1-40),
		and two column names (strings), and returns a slope and intercept for
		the linearly-fitted model for those columns. That can then be used in
		the wrapper function to plot the line."""
		subset = self.exp[expnum][self.exp[expnum]['subject'] == pnum]
		x = subset[xcolumn]
		y = subset[ycolumn]
		m, b = np.polyfit(x,y,1)
		return(m,b)

	def select_participants(expnum,num_participants):
		"""There are 36 participants in each of the first four experiments,
		and 40 in each of the latter four, so there are two slightly different
		returns here for selecting a random sample among them.
		
		Although this currently allows you to select the number of participants,
		more than 6 will result in an error, because there aren't enough basic
		colors. This will have to get patched in the next version."""
		if num_participants > 6 or num_participants < 0:
			raise ValueError('Participant # has to be > 0 and <= 7')
		if expnum < 0 or expnum > 8:
			raise ValueError('Experiment # has to be > 0 and <= 8')
		if expnum < 5:
			return sorted(random.sample(range(1,36),num_participants))
		else:
			returnlist = random.sample(range(1,40),num_participants)
			# Experiment 8 doesn't have a 38th participant, for reasons that
			# aren't worth going into. This avoids selecting that number
			if expnum == 8:
				while 38 in returnlist:
					returnlist = random.sample(range(1,40),num_participants)
			return sorted(returnlist)
			
	def participant_plots(self, xcolumn = 'trial', ycolumn = 'onset_dur', title = 'Default Title', xlab = None, ylab = None):
		"""Takes an x and y column name and returns a 2x4 plot of a
		random-chosen subset of the participants in the experiments,
		complete with linear regression of y on x."""
		colors = ['b','r','g','y','c','m']
		f, ax = plt.subplots(2,4, sharex = True, sharey = True, figsize = (12,8))
		f.suptitle(title, fontsize = 20)
		for exp_num in range(1,9):
			pnums = self.select_participants(exp_num,6)
			for index, pnum in enumerate(pnums):
				m,b = self.participant_line(exp.exp,exp_num,pnum,xcolumn,ycolumn)
				x = range(100)
				f.axes[exp_num-1].plot(x,m*x + b, '-', color = colors[index], marker = '.', label = '%d' %pnum)
				f.axes[exp_num-1].set_title('Experiment %d' %exp_num)
		f.text(0.5, 0.04, xlab, ha = 'center', va = 'center', fontsize = 12)
		f.text(.06, .5, ylab, fontsize = 12, rotation = 'vertical', va = 'center')