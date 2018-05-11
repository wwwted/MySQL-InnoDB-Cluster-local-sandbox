
# MySQL InnoDB Cluster (local sandbox environment)

In this exercise we will build and test a InnoDB Cluster locally on one server. This type of local setup should only be used for testing and development environments, for production use cases you need to have the nodes in your cluster running on separate hosts to survive host failures.

Further reading:
- https://dev.mysql.com/doc/refman/8.0/en/mysql-innodb-cluster-userguide.html
- https://dev.mysql.com/doc/refman/8.0/en/mysql-innodb-cluster-sandbox-deployment.html

This demo works for both MySQL 5.7 as well as for MySQL 8, there are some small differences that will be highlighted later on. Note that MySQL Router 8 and MySQL Shell 8 works for MySQL also and I highly recomend using latest versions of MySQL Shell and MySQL Router.

### Setup environment

First step is to download this repository:
```
bash$ git clone https://github.com/wwwted/MySQL-InnoDB-Cluster-local-sandbox.git
```
or download zipfile manually direct from github and extract content.

Go to into folder:
```
bash$ cd MySQL-InnoDB-Cluster-local-sandbox
```
Now you need to download all binaries need to run InnoDB Cluster, that is MySQL Server, MySQL Shell and MySQL Router.
If you already have downloaded the software you can now create softlinks to targets (server,router,shell) like:
```
bash$ ln -s /path/to/binaries/mysql-server server
bash$ ln -s /path/to/binaries/mysql-shell shell
bash$ ln -s /path/to/binaries/mysql-router router
```
If you have not dowloaded the software you can run:
```
./scripts/download.sh
```
and you will get latest versions of the software (per 2019-05-11) dowloaded, if you want latest versions simply edit the dowload script with correct minor version numbers.

Extract binaries from tar packages:
```
bash$ tar xzf mysql-8.0.11-linux-glibc2.12-x86_64.tar.gz
bash$ tar xzf mysql-shell-8.0.11-linux-glibc2.12-x86-64bit.tar.gz
bash$ tar xzf mysql-router-8.0.11-linux-glibc2.12-x86-64bit.tar.gz
```

Remove binary packages:
```
bash$ rm -fr mysql-8.0.11-linux-glibc2.12-x86_64.tar.gz
bash$ rm -fr mysql-shell-8.0.11-linux-glibc2.12-x86-64bit.tar.gz
bash$ rm -fr mysql-router-8.0.11-linux-glibc2.12-x86-64bit.tar.gz
```

Create softlinks to binaries:
```
bash$ ln -s mysql-8.0.11-linux-glibc2.12-x86_64 server
bash$ ln -s mysql-shell-8.0.11-linux-glibc2.12-x86-64bit shell
bash$ ln -s ln -s mysql-router-8.0.11-linux-glibc2.12-x86-64bit router
```

Last step in the preparations before we can start creating or cluster is to set the correct paths in our shell, this need to done in all windows/command line tools that you use to run commands in:
```
bash$ . ./setenv
```

Verify that all steps above have worked by running:
```
bash$ which mysql
bash$ which mysqlsh
bash$ which mysqlrouter
``` 
Output should be paths to your installed binaies.

You can now also try to start MySQL Shell and verify that it works:
```
bash$ mysqlsh
```
Take a look at commands available by running:
```
mysqlsh>dba.help();
```

### Create a InnoDB Cluster

In this exercise when you use the sandbox commands for creating our cluster we can leverage that MySQL Shell can also create, configure and start our MySQL instances. These instances will be created underneith ~home/mysql-sandboxes and named by the port number you specify when creating your instances (in our case this will be 3310, 3320 and 3330).

If you want to monitor your instances during initial create and failover test later on I would suggest you start a new screen/prompt and run:
```
bash$ watch "pgrep -fla mysql | grep -v pgrep"
```

Before we create our 3 MySQL instances using `deploy.js` lets have a quick look at the content of this file:
```
dba.deploySandboxInstance(3310,{password:'root'});
dba.deploySandboxInstance(3320,{password:'root'});
dba.deploySandboxInstance(3330,{password:'root'});
```
The dba.deploySandboxInstance will fire up a local MySQL instance, only mandatory argument is a port number, you can provide more informaion via a second argument being a JSON document, in this case we are specifying the password for the root account.

Lets run deploy.js using shell to create our 3 MySQL instances:
```
bash$ mysqlsh < ./scripts/deploy.js
```

You should now have 3 MySQL instances up and running and you should see 3 folders (3310,3320 and 3330) in folder ~$HOME/mysql-sandboxes.
You can find the MySQL configuration file (my.cnf) under each folder, have a look at this file before we move on.

Next step is to create our cluster by running the `create.js` script, before we run this lets have a loot at the content of this file:
```
cluster=dba.createCluster("mycluster");
cluster.addInstance("root@127.0.0.1:3320",{password:'root'});
cluster.addInstance("root@127.0.0.1:3330",{password:'root'});
print (cluster.status());
```
The first command we use to create our cluster, this will be done on the MySQL we connect to when executing this script. Next we add the two other MySQL instances to our cluster using the addInstance command, before we exit we print the status of the cluster.  

Lets run ths `create.js` and have a look at output from the commands:
```
bash$ mysqlsh -uroot -proot -h127.0.0.1 -P3310 < scripts/create.js

A new InnoDB cluster will be created on instance 'root@127.0.0.1:3310'.

Validating instance at 127.0.0.1:3310...
Instance detected as a sandbox.
Please note that sandbox instances are only suitable for deploying test clusters for use within the same host.
...
            "127.0.0.1:3330": {
                "address": "127.0.0.1:3330", 
                "mode": "R/O", 
                "readReplicas": {}, 
                "role": "HA", 
                "status": "RECOVERING"
            }
        }
    },
```

Hmmm, looks like the last node of the cluster was still in state `RECOVERING` when we looked at status of the cluster, lets connect to our cluster and investigate this:
```
bash$ mysqlsh -uroot -proot -h127.0.0.1 -P3330
```
When loged into shell run:
```
cluster = dba.getCluster();
cluster.status();
```
State of last node should now be `ONLINE`

Next step depends on what version of MySQL you are testing, if you are running MySQL 5.7 or MySQL 8.0.4 (or earlier) you need to make sure configuration changes made by create cluster commands are persisted. If you are on a late MySQL 8 version this step is not needed as MySQL 8 support `SET PERSISTS` and will update the MySQL configuration automatically instead of the using the `dba.configureLocalInstance` command.

Make sure configuration changes are persisted if you are running any MySQL version prior to 8.0.4:
```
mysqlsh -uroot -proot -h127.0.0.1 -P3310 < scripts/persist-config.js
``` 
You can run above command on later versions of MySQL 8 also but you will then get message like:
```
Calling this function on a cluster member is only required for MySQL versions 8.0.4 or earlier.
```


