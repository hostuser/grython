Grisu Jython
===========

The *Grisu Jython wrapper* is a Java package that contains both the [Grisu client library](https://github.com/grisu/grisu/wiki/Grisu-client-library) and a version of the [Jython](http://jython.org/) interpreter. Basically, it allows you to access all the convenience (Java) methods and objects of the *Grisu client library* via Python syntax. 

Beware, you can't run this package in a native Python environment. So, if you want to write a python script that relies on 3rd party modules which don't run in Jython (for example because they are written in C), you're (most likely) out of luck.


Prerequisites
---------------------

* Sun Java (version >= 6)
* the [Grisu jython package]
  * stable: http://code.ceres.auckland.ac.nz/downloads/grisu-jython.jar or
  * dev: http://code.ceres.auckland.ac.nz/snapshot-downloads/grisu-jython-dev.jar


Documentation / Examples
---------------------------

* Javadoc for the Grisu client library whose classes/methods can be used from jython: http://grisu.github.com/grisu/javadoc/
* Script examples can be found here: https://github.com/grisu/grisu-jython/tree/develop/src/main/jython/grisu/examples
* More examples (but pure Java): https://github.com/grisu/examples
* Grisu wiki: https://github.com/grisu/grisu/wiki

Usage
----------

*grisu-jython* is started like so:

    java -jar grisu-jython.jar <script-name>.py

Here's a very simple example of how to submit a job using the *Grisu Jython wrapper*:

    from grisu.frontend.control.login import LoginManager
    from grisu.frontend.model.job import JobObject
    import sys

    si = LoginManager.loginCommandline()

    

    print 'Creating job...'
    # create the job object

    job = JobObject(si);
    # set a unique jobname
    job.setUniqueJobname("echo_job1")
    print 'Set jobname to: '+ job.getJobname()
    # set the name of the application like it is published in mds. "generic" means not to use mds for the lookup.
    job.setApplication("generic")
    # since we are using a "generic" job, we need to specify a submission location. I'll make that easier later on...
    job.setSubmissionLocation("dque@edda-m:ng2.vpac.org")

    
    # set the commandline that needs to be executed
    job.setCommandline("echo \"Hello World\"")
    
    # create the job on the backend and specify the VO to use
    job.createJob("/ARCS/NGAdmin")
    print 'Submitting job...'
    # submit the job
    job.submitJob()
    
    print 'Waiting for the job to finish...'
    # this waits until the job is finished. Checks every 10 seconds (which would be too often for a real job)
    finished = job.waitForJobToFinish(10)
    
    if not finished:
            print "not finished yet."
            # kill the job on the backend anyway
            job.kill(True);
    else:
            print 'Job finished. Status: '+job.getStatusString(False)
            # download and cache the jobs' stdout and display it's content
            print "Stdout: " + job.getStdOutContent()
            # download and cache the jobs' stderr and display it's content
            print "Stderr: " + job.getStdErrContent()
            # kill and clean the job on the backend
            job.kill(True)
    
    # don't forget to exit properly. this cleans up possible existing threads/executors
    sys.exit()

