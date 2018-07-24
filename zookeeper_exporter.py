import os
import io
import flask
import socket
import concurrent.futures

servers=os.environ.get("ZOOKEEPER", "localhost:2181").split(",")

def query(hostport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hp = hostport.split(":", 1)
	try:
		s.settimeout(3)
		if len(hp)==2:
			s.connect((hp[0], int(hp[1])))
		else:
			s.connect((hp[0], 2181))
		
		s.send(b"srvr")
		return s.recv(4096).decode("UTF-8")
	except Exception as e:
		return "Error: %s" % e
	finally:
		s.close()

def safe_label(name):
	return name.replace("-","_").replace(".","_")

def collect():
	ex = concurrent.futures.ThreadPoolExecutor(max_workers=3)
	mresult = ex.map(query, servers)
	
	values = ""
	modes = {}
	for server,data in zip(servers, mresult):
		for line in io.StringIO(data):
			k,v = [v.strip() for v in line.split(":", 1)]
			
			if k == "Mode":
				modes[server] = v
			if k in ["Received", "Sent", "Connections", "Outstanding", "Node count"]:
				values += 'zk_%s{server="%s"} %s\r\n' % (
					k.lower().replace(" ","_"),
					server,
					v)
			if k == "Error":
				values += 'zk_%s{server="%s",message="%s"} 1\r\n' % (
					k.lower().replace(" ","_"),
					server,
					v)
	lut = ["leader", "follower"]
	params = ",".join(['%s="%s"' % (safe_label(k), lut.index(v)) for k,v in modes.items()])
	values += "zk_modes{%s} 1\r\n" % params
	return values

app = flask.Flask(__name__)

@app.route("/metrics", methods=["GET"])
def metrics():
	return collect()

def cli():
	print(collect())

if __name__=="__main__":
	cli()
