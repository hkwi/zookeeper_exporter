FROM python
RUN pip install git+https://github.com/hkwi/zookeeper_exporter.git
ENV FLASK_APP=zookeeper_exporter FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD ["flask", "run"]
