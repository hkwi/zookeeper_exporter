prometheus exporter for zookeeper stat

Environtmnet variables
----

- ZOOKEEPER: `host[:port][,host:port][...]`, defaults to `localhost:2181`, port defaults to 2181.

Metrics
----

`zk_modes` will be exported with server mode in the quorum in metric labels. 
This is suitable for table format, which was [added in grafana 4.3](http://docs.grafana.org/guides/whats-new-in-v4-3/#prometheus-table-data-column-per-label). Value for replication_group_members is row count for now.

| mode | metric label value |
| :--: | :--: |
| leader   | 0 |
| follower | 1 |
