#Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Makefile
#
# basic commandlines stored that execute the various pieces of the demonstration

show:
	cat README.md

createimages: condor-master condor-compute condor-submit
	@echo "createimages - done"

condor-master condor-compute condor-submit:
	@if [ -z "$$(gcloud compute images list --quiet --filter='name~^$@' --format=text)" ]; then \
	   echo "" ;\
	   echo "- building $@" ;\
	   echo ""; \
	   gcloud compute  instances create  $@-template \
	     --zone=us-east1-b \
	     --machine-type=n1-standard-1 \
	     --image=debian-9-stretch-v20210721 \
	     --image-project=debian-cloud \
	     --boot-disk-size=10GB \
	     --metadata-from-file startup-script=startup-scripts/$@.sh ; \
	   sleep 300 ;\
	   gcloud compute instances stop --zone=us-east1-b $@-template ;\
	   gcloud compute images create $@  \
	     --source-disk $@-template   \
	     --source-disk-zone us-east1-b   \
	     --family htcondor-debian ;\
	   gcloud compute instances delete --quiet --zone=us-east1-b $@-template ;\
	else \
	   echo "$@ image already exists"; \
	fi


deleteimages:
	-gcloud compute images delete --quiet condor-master
	-gcloud compute images delete --quiet condor-compute
	-gcloud compute images delete --quiet condor-submit

upload: htcondor/run.sh
ifeq ($(bucketname),)
	@echo "Need to create bucket on google cloud and run with"
	@echo "make upload bucketname=insert_bucket_name"
else 
	@echo "using ${bucketname}"
	-gsutil mb gs://${bucketname}
	gsutil cp -r data gs://${bucketname}/
	gsutil cp continue_sim.py gs://${bucketname}/
	gsutil cp htcondor/* gs://${bucketname}/htcondor/
endif

# This inserts your bucketname into the run shell script
htcondor/run.sh:
	cp htcondor/run.sh.orig htcondor/run.sh
ifneq ($(bucketname),)
	sed -i 's/YOURBUCKETNAME/${bucketname}/g' htcondor/run.sh 
endif

createcluster:
	@echo "creating a condor cluster using deployment manager scripts"
	gcloud deployment-manager deployments create condor-cluster --config deploymentmanager/condor-cluster.yaml
	
destroycluster:
	@echo "destroying the condor cluster"
	gcloud deployment-manager deployments delete condor-cluster

ssh:
ifeq ($(bucketname),)
	@echo "set the bucketname in order to copy some of the data and model files to the submit host"
	@echo "  make ssh bucketname=insert_bucket_name"
	gcloud compute ssh condor-submit
else
	@echo "using ${bucketname}"
	@echo "before sshing to the submit host, let me copy some of the files there to make"
	@echo "it easier for you."
	@echo "  - copying continue_sim.py"
	gcloud compute ssh condor-submit --command "gsutil cp gs://${bucketname}/continue_sim.py ."
	@echo "  - copying the condor submit files templates"
	gcloud compute ssh condor-submit --command "gsutil cp gs://${bucketname}/htcondor/* ."
	@echo "now just sshing"
	gcloud compute ssh condor-submit
endif

clean:
	rm link.file WIKI_PRICES*.zip WIKI_PRICES*.csv 
