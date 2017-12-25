flow{
    flow1 = {
            "priority": 10,
            "timeout": 0,
            "tableId": 1,
            "isPermanent": true,
            "deviceId": "of:0000687f7429badf",
            "treatment": {
              "instructions": [
                {
                  "type": "OUTPUT",
                  "port": "2"
                }
              ]
            },
            "selector": {
              "criteria": [
                {
                  "type": "IN_PORT",
                  "port": 1
                },
                {
                  "type": "ETH_SRC",
                  "mac": "84:38:35:61:16:62"
                },
                {
                  "type": "ETH_DST",
                  "mac": "60:E3:27:9B:44:BF"
                }
              ]
            }
          }

    flow2 = {
            "priority": 10,
            "timeout": 0,
            "isPermanent": true,
            "deviceId": "of:0000687f7429badf",
            "treatment": {
              "instructions": [
                {
                  "type": "OUTPUT",
                  "port": "1"
                }
              ]
            },
            "selector": {
              "criteria": [
                {
                  "type": "IN_PORT",
                  "port": 2
                },
                {
                  "type": "ETH_SRC",
                  "mac": "60:E3:27:9B:44:BF"
                },
                {
                  "type": "ETH_DST",
                  "mac": "84:38:35:61:16:62"
                }
              ]
            }
          }

    flow3 = {
            "priority": 10,
            "timeout": 0,
            "isPermanent": true,
            "deviceId": "of:0000687f7429badf",
            "treatment": {
              "instructions": [
                {
                  "type": "TABLE",
                  "tableId": 1
                }
              ]
            },
            "selector": {
              "criteria": [
                {
                  "type": "IN_PORT",
                  "port": 1
                },
                {
                  "type": "IPV4_SRC",
                  "ip": "192.168.86.51/24"
                },
                {
                  "type": "IPV4_DST",
                  "ip": "128.59.105.24/24"
                },
                {
                  "type": "ETH_TYPE",
                  "ethType": "0x0800"
                }
              ]
            }
          }
}
