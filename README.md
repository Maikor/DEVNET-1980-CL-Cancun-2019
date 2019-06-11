# devwks-1980


Welcome to the Workshop! 

### Step 1. Get the image & Run the container

```
cisco@cisco-desktop:~$ docker pull golang
Using default tag: latest
latest: Pulling from library/golang
c5e155d5a1d1: Pull complete
221d80d00ae9: Pull complete
4250b3117dca: Pull complete
3b7ca19181b2: Pull complete
aa24759e848f: Pull complete
927e9eaeed19: Pull complete
66293f4dacbd: Pull complete
Digest: sha256:cf0b9f69ad1edd652a7f74a1586080b15bf6f688c545044407e28805066ef2cb
Status: Downloaded newer image for golang:latest
cisco@cisco-desktop:~$ docker images | grep golang
golang                               latest              7ced090ee82e        4 weeks ago         774MB
cisco@cisco-desktop:~$ docker run -it --rm --name my-telemetry-collector --network host golang
root@cisco-desktop:/go#
```

### Step 2. Clone the repo & Deal with dependencies

```
root@cisco-desktop:/go# go get -d github.com/ios-xr/telemetry-go-collector
package github.com/ios-xr/telemetry-go-collector: no Go files in /go/src/github.com/ios-xr/telemetry-go-collector
root@cisco-desktop:/go#
root@cisco-desktop:/go/src/github.com# cd /go/src/github.com/ios-xr/telemetry-go-collector
root@cisco-desktop:/go/src/github.com/ios-xr/telemetry-go-collector# ls
Dialout-collector-howto.md  bin   mdt_grpc_dialin   telemetry			telemetry_dialout_collector
README.md		    docs  mdt_grpc_dialout  telemetry_dialin_collector
root@cisco-desktop:~# go get -u github.com/golang/protobuf/protoc-gen-go**
root@cisco-desktop:~#
root@cisco-desktop:~# go get -u google.golang.org/grpc
root@cisco-desktop:~#
root@cisco-desktop:/go#go build -o bin/telemetry_dialin_collector github.com/ios-xr/telemetry-go-collector/telemetry_dialin_collector
root@cisco-desktop:/go#
root@cisco-desktop:/go# ls bin/
protoc-gen-go  telemetry_dialin_collector
```


### Step 3. Run The Collector! 

```
root@cisco-desktop:/go# ./telemetry_dialin_collector -server "host_ip:57751" -subscription cdp -oper subscribe -username vagrant -password vagrant
mdtSubscribe: Dialin Reqid 30196 subscription [cdp]
{
	"node_id_str": "rtr1",
	"subscription_id_str": "cdp",
	"encoding_path": "Cisco-IOS-XR-telemetry-model-driven-oper:telemetry-model-driven/destinations/destination",
	"collection_id": 1,
	"collection_start_time": 1560229527690,
	"msg_timestamp": 1560229527692,
	"data_json": [
		{
			"timestamp": 1560229527691,
			"keys": {
				"destination-id": "XRDOCS"
			},
			"content": {
				"id": "XRDOCS",
				"configured": 1,
```
