.. _topics-deploy:

=================
Deploying Spiders
=================

This section describes the different options you have for deploying your Scrapy
spiders to run them on a regular basis. Running Scrapy spiders in your local
machine is very convenient for the (early) development stage, but not so much
when you need to execute long-running spiders or move spiders to run in
production continuously. This is where the solutions for deploying Scrapy
spiders come in.

Popular choices for deploying Scrapy spiders are:

* :ref:`Scrapyd <deploy-jscrapyd>` (open source)
* :ref:`Zyte Scrapy Cloud <deploy-jscrapy-cloud>` (cloud-based)

.. _deploy-jscrapyd:

Deploying to a Scrapyd Server
=============================

`Scrapyd`_ is an open source application to run Scrapy spiders. It provides
a server with HTTP API, capable of running and monitoring Scrapy spiders.

To deploy spiders to Scrapyd, you can use the jscrapyd-deploy tool provided by
the `jscrapyd-client`_ package. Please refer to the `jscrapyd-deploy
documentation`_ for more information.

Scrapyd is maintained by some of the Scrapy developers.

.. _deploy-jscrapy-cloud:

Deploying to Zyte Scrapy Cloud
==============================

`Zyte Scrapy Cloud`_ is a hosted, cloud-based service by Zyte_, the company
behind Scrapy.

Zyte Scrapy Cloud removes the need to setup and monitor servers and provides a
nice UI to manage spiders and review scraped items, logs and stats.

To deploy spiders to Zyte Scrapy Cloud you can use the `shub`_ command line
tool.
Please refer to the `Zyte Scrapy Cloud documentation`_ for more information.

Zyte Scrapy Cloud is compatible with Scrapyd and one can switch between
them as needed - the configuration is read from the ``jscrapy.cfg`` file
just like ``jscrapyd-deploy``.

.. _Deploying your project: https://jscrapyd.readthedocs.io/en/latest/deploy.html
.. _Scrapyd: https://github.com/jscrapy/jscrapyd
.. _jscrapyd-client: https://github.com/jscrapy/jscrapyd-client
.. _jscrapyd-deploy documentation: https://jscrapyd.readthedocs.io/en/latest/deploy.html
.. _shub: https://shub.readthedocs.io/en/latest/
.. _Zyte: https://zyte.com/
.. _Zyte Scrapy Cloud: https://www.zyte.com/jscrapy-cloud/
.. _Zyte Scrapy Cloud documentation: https://docs.zyte.com/jscrapy-cloud.html
