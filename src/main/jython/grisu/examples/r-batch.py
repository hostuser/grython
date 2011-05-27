'''
Created on 25/05/2011

@author: Markus Binsteiner
'''
from grisu.frontend.control.login import LoginManager
from grisu.frontend.model.job import JobObject, BatchJobObject
from grisu.model import UserEnvironmentManager, GrisuRegistry, \
    GrisuRegistryManager
from grisu.jcommons.constants import Constants


# constants
#backend = 'Local'
backend = 'BeSTGRID-DEV'
#backend = 'BeSTGRID'

walltime = 1800
email = 'm.binsteiner@auckland.ac.nz'
basename = 'r-batch'

inputdir = '/home/markus/Desktop/R/'
#inputfilename = 'Evaluation_Markov-ADF-Test-2011-05-09-mc50.r'
inputfilename = 'Evaluation_Markov-ADF-Test-2011-05-09-mc50-test.r'

print 'logging in...'
si = LoginManager.loginCommandline(backend)
uem = GrisuRegistryManager.getDefault(si).getUserEnvironmentManager()
print 'starting job creation...'
gen_jobs = 200
batch_nr = 1

group = '/nz/nesi'

#sub_loc = 'route@er171.ceres.auckland.ac.nz:ng2.auckland.ac.nz'

batch_job_name = uem.calculateUniqueJobname(basename)

batch_job = BatchJobObject(si, batch_job_name, group, 'R', Constants.NO_VERSION_INDICATOR_STRING)

inputFile = batch_job.pathToInputFiles()+inputfilename

print "Relative path to inputfile: "+inputFile

for i in range(1,gen_jobs):
    print 'generating job '+str(i)
    job = JobObject(si)
    job.setJobname(batch_job_name+"_"+str(i))
    job.setForce_single(True)
    job.setEmail_address(email)
    job.setEmail_on_job_finish(True)
    #job.setSubmissionLocation(sub_loc)

    job.setCommandline('R --no-readline --no-restore --no-save -f '+inputFile)

    batch_job.addJob(job)
    
batch_job.addInputFile('/home/markus/Desktop/R/'+inputfilename)
batch_job.setDefaultNoCpus(1)
batch_job.setDefaultWalltimeInSeconds(walltime)

print 'preparing jobs on backend...'
batch_job.prepareAndCreateJobs(False)

print 'submitting jobs to grid...'
batch_job.submit(True)

print 'submission finished...'




    
    
    

