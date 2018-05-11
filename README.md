
# MySQL InnoDB Cluster (local sandbox environment)

In this exercise we will build and test a InnoDB Cluster locally on one server. This type of local setup should only be used for testing and development environments, for production use cases you need to have the nodes in your cluster running on separate hosts to survive host failures.

Further reading:
- https://dev.mysql.com/doc/refman/8.0/en/mysql-innodb-cluster-userguide.html
- https://dev.mysql.com/doc/refman/8.0/en/mysql-innodb-cluster-sandbox-deployment.html


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

If you want to monitor what is happening when creating your instances I would suggest you start a new screen/prompt and run:
```
bash$ watch "pgrep -fla mysql | grep -v pgrep"
```

Before we create our 3 MySQL instances using `deploy.js` lets have a quick look at the content of this file:
```
dba.deploySandboxInstance(3310,{password:'root'});
dba.deploySandboxInstance(3320,{password:'root'});
dba.deploySandboxInstance(3330,{password:'root'});
```

Lets run deploy.js using shell to create our 3 MySQL instances:
```
bash$ mysqlsh < deploy.js
```


