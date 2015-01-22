#==========Parameters
HOME=/root
DCAP_BNET_DIR=$HOME/dcap_test
STARTUP_SCRIPT_DIR=$DCAP_BNET_DIR/startup
CERT=elaineh3
TYPE=m1.8core
AMI=ami-00000023
DCAP_SERVER_SCRIPT_DIR=$DCAP_BNET_DIR/dcap
DCAP_SERVER_SCRIPT=RunServer.py 
PART_HANDLER=$(readlink -f part_handler.py)
EUCA_INITIALIZE_INSTANCES_CMD=euca-run-instances 
SERVER_PORT=4444
TASKFILE='../tasks/testBnetTasks.txt'
# TASKFILE='../tasks/bnetTasks.txt'
#=====================

NUM=$1
#$1 is the first argument that is passed in to the shellscript. It is the number of instances to launch
NAME=$2

cd $DCAP_BNET_DIR

#set environment for the euca2tools
source $DCAP_BNET_DIR/ec2rc.sh #. is source, here source ec2rc script, make sure location is correct


echo "Starting Instances"
INSTANCE=$($EUCA_INITIALIZE_INSTANCES_CMD -k $CERT -n $NUM $AMI -t $TYPE  | grep i- | cut -f 2)
# set INSTANCE to return of command encapsulated by $() . Instances will be set to all ids that were started
#echo $INSTANCE


echo "Started $INSTANCE"

##################### FOR STARTING JUST NODES ########################
# exit 0
INSTANCE=$($EUCA_INITIALIZE_INSTANCES_CMD -k $CERT -n $NUM $AMI -t $TYPE  | grep i- | cut -f 2)


INSTANCE=$(euca-describe-instances $INSTANCE | grep $CERT | grep $AMI | grep -v error | grep i- | cut -f 2) #filtering out ids of instances that are in error state
echo "TERMINATING"
echo $INSTANCE
echo "Terminated $(xargs -t -a <(echo $INSTANCE) -n 1 -P 50 euca-terminate-instances | wc -l) instances" #kills nodesi

