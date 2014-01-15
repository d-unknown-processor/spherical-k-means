#!/usr/bin/env python3

################################################################################
# A Python implementation of the Spherical K-Means clustering algorithm.	
#
# The SPK-Means algorithm is used to create K clusters into which it sorts
# given documents containing text data. These clusters are generated as a
# means of finding patterns in large amounts of data.
# The number of clusters, K, is provided as a parameter.
#
# Implementation by Richard Teammco
# teammco@cs.utexas.edu
#
# Tested with Python version 3.1.3
################################################################################


# import Reader module
from reader import Reader
from vector import Vector


################################################################################
# SPKMeans class
class SPKMeans():
	"""Docs"""
	
	
	def __init__(self, reader):
		"""Set up the reader and call it to read all of the documents."""
		self.reader = reader
		self.doc_vecs = self.reader.read()
		self.num_docs = len(self.doc_vecs)
		self.reader.report()
		

	def cluster(self, k):
		"""Run the full SPKMeans algorithm, and return the partitions."""
		# k must be at least 2 (otherwise meaningless)
		if k < 2:
			print("Warning: must use at least 2 partitions. Stopping.")
			return
		
		print("Running SPKMeans clustering: {} partitions.".format(k))
		
		# TODO - txn scheme
		
		# create first partition set and concept vectors
		partitions = self.randomize_partitions(k)
		concepts = self.get_concepts(partitions)
		
		while True: # while delta_quality < q_threshold:
			partitions = [[]] * k
			
			for i in range(self.num_docs): # for each document
				#find closest doc vector of cosine similarity
				closest = -1
				closest_val = 0
				for cv_index in range(k):
					scrap = concepts[cv_index]
					dot_p = self.doc_vecs[i].dot(concepts[cv_index])
					if closest == -1 or dot_p < closest_val:
						closest = cv_index
						closest_val = dot_p
						
				# put the document Vector into the partition associated
				#	with the closest concept Vector
				partitions[closest].append(self.doc_vecs[i])
				
			# recalculate concept vectors
			concepts = self.get_concepts(partitions)
			return 123 # TODO - remove
			
			#
			# NOTE: If a partition ends up being empty, there can be no
			#	concept vector for it (norm of 0 vector is undefined)...
			#	Can an empty partition happen? If so, how to deal with it?
			#
		
		print(concepts)
		return 0
	
	
	def get_concepts(self, partitions):
		"""Returns a set of concept Vectors, one for each partition."""
		concepts = []
		for p in partitions:
			concepts.append(self.compute_concept(p))
		return concepts
	
	
	def compute_concept(self, p):
		"""
		Computes the Concept Vector of given partition p, and returns said
		Concept Vector. Parameter p must be a list containing at least one
		document Vector.
		"""
		# computer sum of all vectors in partition p
		cv = Vector(len(self.reader.word_list))
		for doc_v in p:
			cv += doc_v
			
		# compute the mean vector for partition using the sum vector
		cv *= (1/len(p))
		
		# computer the norm of the mean vector
		cv = cv.norm()
		
		return cv
	
	
	def randomize_partitions(self, k):
		"""
		Create a set of k partitions with the documents randomly
		distributed to a cluster. Maintains as much distribution equality
		between the partitions as possible.
		Returns the set of partitions.
		TODO: not random; splits up by order docs were scanned in
		"""
		partitions = []
		num_per_partition = int(self.num_docs / k)
		for pindex in range(k):
			partition_vecs = []
			partition_size = num_per_partition
			if pindex == k-1:
				partition_size = partition_size + (self.num_docs % k)
			for num in range(partition_size):
				num += (pindex * (k-1))
				partition_vecs.append(self.doc_vecs[num])
			partitions.append(partition_vecs)
		
		return partitions
################################################################################


# define documents to be used and number of clusters
# TODO - docs and number of clusters as parameters
NUM_CLUSTERS = 2
docs = ['one.txt', 'x', 'two.txt', 'three.txt']
		#'long1.txt', 'long2.txt', 'long3.txt']

# start here
if __name__ == "__main__":
	reader = Reader(docs)
	clusters = SPKMeans(reader).cluster(NUM_CLUSTERS)
	print(clusters)
	

#	(1) Start with arbitrary partitioning 0: {ℼ(0)j}kj=1.
#		{c(0)j}kj=1 denotes concept vectors associated with given partitioning 0.
#		Set t = 0 (index of iteration).
#	(2) ∀xi (1 to n), find concept vector closest in cosine similarity to xi.
#		Compute new partitioning {ℼ(t+1)j}kj=1 induced by old concept vectors {c(t)j}kj=1.
#		“ℼ(t+1)j is the set of all document vectors closest to the concept vector c(t)j.”
#		- if doc vector closest to more than one, assign it randomly to one of the clusters.
#	(3) Compute new concept vectors for (t+1):
#		c(t+1)j = m(t+1)j / || m(t+1)j ||, 1 ≤ j ≤ k.						( 8 )
#		m(t+1)j = centroid or mean of document vectors in cluster ℼ(t+1)j.
#	(4) 	If stopping criterion met: set ℼ*j = ℼ(t+1)j and c*j = c(t+1)j (for all 1 ≤ j ≤ k). EXIT.
#		Else: t++; GOTO step_2.
#		stopping criterion may be difference in Q at t and t+1 <= threshold.