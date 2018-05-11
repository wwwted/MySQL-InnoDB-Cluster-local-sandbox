cluster=dba.createCluster("mycluster");
cluster.addInstance("root@127.0.0.1:3320",{password:'root'});
cluster.addInstance("root@127.0.0.1:3330",{password:'root'});
print (cluster.status());

