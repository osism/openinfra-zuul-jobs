Sets a fact named ``zuul_log_path`` from zuul variables

The resulting log path will be based on the zuul tenant name and build
uuid. The url will then be prefixed by a portion of the build uuid.
This prefix allows for partitioning in object storage systems.
Constructing the url in this way isn't very human readable but produces
consistent url lengths which is important for database record keeping
and avoiding unexpected problems with url lengths exceeding limits.
