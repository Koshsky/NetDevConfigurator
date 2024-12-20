


templates = [
  {
    "name": "AudioPcPort",  # orig: Порт подключения миниПК-клиентов цифрового звука
    "type": "interface",
    "role": "or",
    "text": """interface {INTERFACE_ID}   
  switchport general allowed vlan add 30
  switchport general allowed vlan add 3 untagged
  switchport forbidden default-vlan
  switchport general pvid 3
  qos trust cos-dscp
!""",  # не забудь восклицательный знак там где он нужен!
  },
  {
    "name": "AudioPcPort",  # orig: Порт подключения миниПК-клиентов цифрового звука
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport general allowed vlan add 30
  switchport general allowed vlan add 3 untagged
  switchport forbidden default-vlan
  switchport general pvid 3
  qos trust cos-dscp
!""",  # не забудь восклицательный знак там где он нужен!
  },
  {
    "name": "DataAccessPort",  # orig: Порт подключения клиентов сети данных
    "type": "interface",
    "role": "data",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 3
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataAccessPort",  # orig: Порт подключения клиентов сети данных
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 3
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataAccessPort",  # orig: Порт подключения клиентов сети данных
    "type": "interface",
    "role": "or",
    "text": """interface {INTERFACE_ID}  
  switchport mode access
  switchport access vlan 3
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtAccessPort",  # orig: Порт подключения клиентов сети управления
    "type": "interface",
    "role": "data",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 4
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtAccessPort",  # orig: Порт подключения клиентов сети управления
    "type": "interface",
    "role": "video",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 4
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtAccessPort",  # orig: Порт подключения клиентов сети управления
    "type": "interface",
    "role": "ipmi",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 4
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtAccessPort",  # orig: Порт подключения клиентов сети управления
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 4
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtAccessPort",  # orig: Порт подключения клиентов сети управления
    "type": "interface",
    "role": "or",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 4
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataTrunkPort",  # orig: Аплинк сети данных до маршрутизатора
    "type": "interface",
    "role": "data",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 3
  no switchport general pvid
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtTrunkPort",  # orig: Аплинк сети управления до маршрутизатора
    "type": "interface",
    "role": "data",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 4
  no switchport general pvid
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "MgmtTrunkPort",  # orig: Аплинк сети управления до маршрутизатора
    "type": "interface",
    "role": "ipmi",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 4
  no switchport general pvid
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataMgmtTrunkPort",  # orig: Транковый порт сети управления и сети данных
    "type": "interface",
    "role": "data",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 3,4
  no switchport general pvid
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataMgmtTrunkPort",  # orig: Транковый порт сети управления и сети данных
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 3,4
  no switchport general pvid
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "DataMgmtTrunkPort",  # orig: Транковый порт сети управления и сети данных
    "type": "interface",
    "role": "or",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 3,4
  no switchport general pvid
  qos trust cos-dscp
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "VideoAccessPort",  # orig: Порт подключения клиентов сети видео
    "type": "interface",
    "role": "video",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport access vlan 2
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "VideoTrunkPort",  # orig: Транковый порт клиентов сети видео
    "type": "interface",
    "role": "video",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 2
  no switchport general pvid
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "VideoTrunkPort",  # orig: Транковый порт клиентов сети видео
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 2
  no switchport general pvid
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "GersPort",  # orig: Порт для подключения ГЕРС
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID} 
  switchport mode general  
  switchport general allowed vlan add 2
  switchport general allowed vlan add 3 untagged
  switchport forbidden default-vlan
  switchport general pvid 3
!""",  
  },
  {
    "name": "AudioClientPort",  # orig: Порт подключения клиентов цифрового звука
    "type": "interface",
    "role": "tsh",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport forbidden default-vlan
  switchport access vlan 30
  qos trust cos-dscp
!""",  
  },
  {
    "name": "AudioClientPort",  # orig: Порт подключения клиентов цифрового звука
    "type": "interface",
    "role": "or",
    "text": """interface {INTERFACE_ID}   
  switchport mode access
  switchport forbidden default-vlan
  switchport access vlan 30
  qos trust cos-dscp
!""",  
  },
  {
    "name": "RaisAccessPort",  # orig: Порт подключения РАИС
    "type": "interface",
    "role": "raisa_agr",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 5
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "RaisAccessPort",  # orig: Порт подключения РАИС
    "type": "interface",
    "role": "raisa_or",
    "text": """interface {INTERFACE_ID}   
  switchport mode general
  switchport general allowed vlan add 5
  switchport forbidden default-vlan
!""",  
  },
  {
    "name": "Gateway",  
    "type": "GW",
    "role": "common",
    "text": """ip route 0.0.0.0  0.0.0.0 10.4.0.254
!""",  
  },
  {
    "name": "SpanningTree",  
    "type": "STP",
    "role": "common",
    "text": """no spanning-tree
!""",  
  },
  {
    "name": "AAA",  
    "type": "credentials",
    "role": "common",
    "text": """username mvsadmin password encrypted zbICg2SPBsvT1IfFwRpH3Q== privilege 15
username admin_rec password encrypted Ts6Wa2/X/ebD/HnwyJC5NQ== privilege 15
!""",  
  },
  {
    "name": "ZTP",  
    "type": "ZTP",
    "role": "common",
    "text": """ztp disable
!""",  
  },
  {
    "name": "CosAudio",  
    "type": "priority",
    "role": "tsh",
    "text": """mac access-list extended 1030
  permit any any vlan 30
!
class-map 30
  match access-group mac-access-list 1030
  set class 30
!
policy-map 30
  set policy class 30 default-priority-type ipDscp 46
!""",  
  },
  {
    "name": "CosAudio",  
    "type": "priority",
    "role": "or",
    "text": """mac access-list extended 1030
  permit any any vlan 30
!
class-map 30
  match access-group mac-access-list 1030
  set class 30
!
policy-map 30
  set policy class 30 default-priority-type ipDscp 46
!""",  
  },
  {
    "name": "CosMgmt",  
    "type": "priority",
    "role": "common",
    "text": """mac access-list extended 1004
  permit any any vlan 4
!
class-map 4 
  match access-group mac-access-list 1004
  set class 4
!
policy-map 4
  set policy class 4 default-priority-type ipDscp 48
!""",  
  },
  {
    "name": "TypeCommutation",  
    "type": "type-commutation",
    "role": "common",
    "text": """switching-mode cut-through
!""",  
  },
  {
    "name": "Header",  
    "type": "header",
    "role": "common",
    "text": """#Building configuration...
#ISS config ver. 9; SW ver. 10.3.4 (c6313afa) for MES2424 rev.B. Do not remove or edit this line
!""",  
  },
  {
    "name": "JumboFrame",  
    "type": "jumbo",
    "role": "common",
    "text": """port jumbo-frame
!""",  
  },
  {
    "name": "VlansData",  
    "type": "VLAN",
    "role": "data",
    "text": """vlan 3-4
  vlan active
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansVideo",  
    "type": "VLAN",
    "role": "video",
    "text": """vlan 2-4
  vlan active
!
vlan 2
  name "VIDEO"
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansVideoOob",  
    "type": "VLAN",
    "role": "video",
    "text": """vlan 2
  vlan active
!
vlan 2
  name "VIDEO"
!""",  
  },
  {
    "name": "VlansMgmt",  
    "type": "VLAN",
    "role": "ipmi",
    "text": """vlan 4
  vlan active
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansTsh",  
    "type": "VLAN",
    "role": "tsh",
    "text": """vlan 2-4
  vlan active
!
vlan 2
  name "VIDEO"
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansTshAudio",  
    "type": "VLAN",
    "role": "tsh",
    "text": """vlan 2-4,30
  vlan active
!
vlan 2
  name "VIDEO"
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!
vlan 30
  name "SOUND"
!""",  
  },
  {
    "name": "VlansOr",  
    "type": "VLAN",
    "role": "or",
    "text": """vlan 3-4
  vlan active
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansOrAudio",  
    "type": "VLAN",
    "role": "or",
    "text": """vlan 3-4,30
  vlan active
!
vlan 3
  name "DATA"
!
vlan 4
  name "MGMT"
!
vlan 30
  name "SOUND"
!""",  
  },
  {
    "name": "VlansRais",  
    "type": "VLAN",
    "role": "raisa_agr",
    "text": """vlan 5
  vlan active
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "VlansRais",  
    "type": "VLAN",
    "role": "raisa_or",
    "text": """vlan 5
  vlan active
!
vlan 4
  name "MGMT"
!""",  
  },
  {
    "name": "AddrData",  
    "type": "addr-set",
    "role": "data",
    "text": """interface vlan 4
  ip address 10.4.0.3 255.255.0.0
!""",  
  },
  {
    "name": "AddrVideo",  
    "type": "addr-set",
    "role": "video",
    "text": """interface vlan 4
  ip address 10.4.0.2 255.255.0.0
!""",  
  },
  {
    "name": "AddrVideoOob",  
    "type": "addr-set",
    "role": "video",
    "text": """interface oob
 ip address 10.4.0.2 255.255.0.0
 no ip address dhcp
!""",  
  },
  {
    "name": "AddrMgmt",  
    "type": "addr-set",
    "role": "mgmt",
    "text": """interface vlan 4
  ip address 10.4.0.4 255.255.0.0
!""",  
  },
  {
    "name": "AddrTsh",  
    "type": "addr-set",
    "role": "tsh",
    "text": """interface vlan 4
  ip address 10.4.{OR}.11 255.255.0.0
!""",  
  },
  {
    "name": "AddrOr",  
    "type": "addr-set",
    "role": "or",
    "text": """interface vlan 4
  ip address 10.4.{OR}.12 255.255.0.0
!""",  
  },
  {
    "name": "AddrRais",  
    "type": "addr-set",
    "role": "rais-adr",
    "text": """interface vlan 4
  ip address 10.5.0.5 255.255.0.0
!""",  
  },
  {
    "name": "AddrRaisOr",  
    "type": "addr-set",
    "role": "rais-or",
    "text": """interface vlan 5
  ip address 10.5.{OR}.11 255.255.0.0
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "data",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "video",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "ipmi",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "rais-agr",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "tsh",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}{OR}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "or",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}{OR}"
!""",  
  },
  {
    "name": "Hostname",  
    "type": "hostname",
    "role": "rais-or",
    "text": """hostname "{CERT}-{MODEL}-{ROLE}{OR}"
!""",  
  },
  {
    "name": "SSH",  
    "type": "ssh",
    "role": "common",
    "text": """ip ssh server
!
ip ssh cipher aes256
!""",  
  },
  {
    "name": "SNMP",  
    "type": "SNMP",
    "role": "common",
    "text": """snmp user mvssnmp auth sha encrypted UWLMnO+/80icwaXNHjbOrg==  priv DES encrypted zbICg2SPBsvGHi1qfemifg==
snmp group mvssnmpgroup user mvssnmp security-model v3
snmp access mvssnmpgroup v3 priv read iso write iso notify iso
snmp view iso 1 included
!""",  
  },
]



